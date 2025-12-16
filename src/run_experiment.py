import os
import json
import openai
from tenacity import retry, wait_exponential, stop_after_attempt
import time
import re

# --- Configuration ---
# Assuming OPENAI_API_KEY is set as an environment variable
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
# Using a powerful model as discussed in the plan
MODEL_NAME = "gpt-4o"

# --- Debugging ---
print(f"Using API Key: {API_KEY[:8]}...")
# -----------------

INPUT_ARTICLES_PATH = "artifacts/selected_articles.json"
GENERATED_ARTIFACTS_PATH = "results/generated_artifacts.json"
EVALUATION_RESULTS_PATH = "results/evaluation_results.json"

# --- LLM Client Setup ---
openai.api_key = API_KEY
client = openai.OpenAI()


@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def get_completion(prompt, model_name=MODEL_NAME, json_mode=False):
    """Generic function to get a completion from the specified model."""
    print(f"--- Calling LLM ({model_name}) ---")
    try:
        response = client.chat.completions.create(
            model=model_name,
            response_format={"type": "json_object"} if json_mode else None,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Your responses should be clear, concise, and directly address the user's request in the specified format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2, # Low temperature for consistent evaluation
        )
        result = response.choices[0].message.content
        print("--- LLM call successful ---")
        return result.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def clean_json_string(s):
    """Cleans a string that might contain a JSON object wrapped in markdown."""
    match = re.search(r'```json\s*(\{.*?\})\s*```', s, re.DOTALL)
    if match:
        return match.group(1)
    return s # Return original string if no markdown found

# --- Generation Functions (from previous step, now unused if artifacts are loaded) ---
# ... (generation functions can be kept for completeness but are not run again)

# --- Evaluation Functions ---

def generate_ground_truth_qa(article_text):
    """Generates a set of 10 ground truth Q&A pairs from the article."""
    print("Generating ground truth Q&A...")
    prompt = f"""
    Based on the following article, please generate a list of 10 diverse and non-trivial question-answer pairs that cover the main points of the text.
    The output must be a JSON object with a single key "qa_pairs" which is a list of 10 objects, each with a "question" and "answer" key.
    The answers should be detailed and directly extracted or synthesized from the article.

    ARTICLE:
    ---
    {article_text}
    ---
    """
    qa_str = get_completion(prompt, json_mode=True)
    return json.loads(qa_str)["qa_pairs"]

def get_simulated_user_answers(artifact_name, artifact_content, questions):
    """Simulates a user trying to answer questions with a given artifact."""
    print(f"Simulating user for artifact: {artifact_name}")

    # For hierarchical and Q&A, we simulate a two-step interaction
    if artifact_name == "hierarchical":
        # First, show the top-level info
        tldr = artifact_content.get('tldr', '')
        headlines = [n['headline'] for n in artifact_content.get('nuggets', [])]
        initial_info = f"TLDR: {tldr}\n\nKey Topics:\n" + "\n".join(f"- {h}" for h in headlines)
        
        # Second, the user "fetches" the details needed
        full_details = "\n\n".join([f"Headline: {n['headline']}\nDetail: {n['detail']}" for n in artifact_content.get('nuggets', [])])
        context = f"You have been provided with a hierarchical summary.\n\nINITIAL VIEW:\n{initial_info}\n\nFULL DETAILS:\n{full_details}"

    elif artifact_name == "qa_interface":
        # The user has a list of questions they can "ask".
        # We provide the full Q&A list as the context.
        context = "You have been provided with a Q&A interface. Here are the available questions and their answers:\n\n"
        context += "\n\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in artifact_content.get('questions_and_answers', [])])

    else: # Dense summary
        context = f"You have been provided with the following summary:\n\n{artifact_content}"

    question_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
    prompt = f"""
    You are a junior analyst. Your task is to answer the following questions based *only* on the information provided below.
    Do not use any prior knowledge. If the information is not available, state that clearly.
    For each question, provide a direct and concise answer.

    --- INFORMATION PROVIDED ---
    {context}
    ---

    --- QUESTIONS ---
    {question_text}
    ---

    Please provide your answers in a JSON object with a single key "answers", which is a list of strings.
    The list should contain your answer for each question in order.
    """
    answers_str = get_completion(prompt, model_name="gpt-3.5-turbo", json_mode=True) # Use a cheaper model for the "user"
    return json.loads(answers_str)["answers"]

def score_answers(questions, ground_truth_answers, simulated_answers):
    """Uses an LLM to score the simulated user's answers against the ground truth."""
    print("Scoring simulated answers...")
    scores = []
    for i, q in enumerate(questions):
        prompt = f"""
        You are an evaluator. Your task is to determine if the "Simulated Answer" is correct, based on the "Ground Truth Answer".
        The answer is correct if it contains the same essential information, even if worded differently.

        Question: "{q}"
        Ground Truth Answer: "{ground_truth_answers[i]}"
        Simulated Answer: "{simulated_answers[i]}"

        Is the simulated answer correct? Respond with a JSON object containing a single key "is_correct" which is a boolean value (true or false).
        """
        score_str = get_completion(prompt, model_name="gpt-3.5-turbo", json_mode=True)
        try:
            is_correct = json.loads(score_str)["is_correct"]
            scores.append(1 if is_correct else 0)
        except (json.JSONDecodeError, KeyError):
            scores.append(0) # Penalize for incorrect format
        time.sleep(1) # Avoid hitting rate limits on the scoring calls
    
    accuracy = sum(scores) / len(scores) if scores else 0
    return accuracy, scores

def get_simulated_preference(article_text, artifacts):
    """Asks an LLM to rank the artifacts for clarity and efficiency."""
    print("Getting simulated user preference...")
    prompt = f"""
    You are a user who was just trying to understand a news article. You were presented with three different summary formats.
    
    Article Content: "{article_text[:1000]}..." # Snippet for context

    Format A (Dense Summary): {artifacts['dense'][:500]}...
    Format B (Hierarchical Summary): TLDR: {artifacts['hierarchical'].get('tldr', '')} - with expandable sections.
    Format C (Q&A Interface): A list of questions and answers about the article.

    Please rank these three formats (A, B, C) from best to worst for helping you understand the article's key information quickly and accurately.
    Your output must be a JSON object with a single key "ranking", which is a list of strings (e.g., ["B", "C", "A"])
    """""
    ranking_str = get_completion(prompt, json_mode=True)
    return json.loads(ranking_str)["ranking"]

# --- Main Orchestration ---

def main():
    # Check if artifacts exist, if not, generate them (implement generation logic here if needed)
    if not os.path.exists(GENERATED_ARTIFACTS_PATH):
        print("Generated artifacts not found. Please run the generation part of the script first.")
        # For a real run, you might call a generation function here.
        return

    with open(GENERATED_ARTIFACTS_PATH, "r") as f:
        generated_artifacts = json.load(f)

    all_results = []

    for i, article_artifacts in enumerate(generated_artifacts):
        print(f"\n--- Evaluating Article {i+1}/{len(generated_artifacts)} (ID: {article_artifacts['id']}) ---")
        article_text = article_artifacts["article"]

        # 1. Generate ground truth Q&A for this article
        ground_truth_qa = generate_ground_truth_qa(article_text)
        questions = [qa["question"] for qa in ground_truth_qa]
        ground_truth_answers = [qa["answer"] for qa in ground_truth_qa]

        results = {"id": article_artifacts["id"], "scores": {}}

        # 2. Evaluate each artifact
        try:
            artifacts_to_test = {
                "dense": article_artifacts["dense_summary"],
                "hierarchical": json.loads(clean_json_string(article_artifacts["hierarchical_summary_str"])),
                "qa_interface": json.loads(clean_json_string(article_artifacts["qa_interface_str"]))
            }
        except json.JSONDecodeError as e:
            print(f"Fatal Error: Failed to parse cleaned JSON for article {article_artifacts['id']}. Skipping article.")
            print(f"Error: {e}")
            print("Problematic hierarchical string:", article_artifacts["hierarchical_summary_str"])
            print("Problematic qa_interface string:", article_artifacts["qa_interface_str"])
            continue


        for name, content in artifacts_to_test.items():
            simulated_answers = get_simulated_user_answers(name, content, questions)
            accuracy, individual_scores = score_answers(questions, ground_truth_answers, simulated_answers)
            results["scores"][name] = {"accuracy": accuracy, "individual_scores": individual_scores}
            print(f"Artifact '{name}' accuracy: {accuracy:.2f}")

        # 3. Get simulated user preference
        preference = get_simulated_preference(article_text, artifacts_to_test)
        results["preference"] = preference
        print(f"Simulated Preference: {preference}")

        all_results.append(results)

    # Save all evaluation results
    with open(EVALUATION_RESULTS_PATH, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nSuccessfully completed evaluation. Results saved to {EVALUATION_RESULTS_PATH}")

if __name__ == "__main__":
    main()
