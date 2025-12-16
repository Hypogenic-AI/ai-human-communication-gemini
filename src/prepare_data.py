
import json
from datasets import load_dataset

def prepare_and_save_data():
    """
    Loads the cnn_dailymail dataset, selects 5 articles,
    and saves them to a JSON file.
    """
    print("Loading cnn_dailymail dataset...")
    # Load the dataset
    # Using a specific version for reproducibility
    dataset = load_dataset("cnn_dailymail", "3.0.0", split="test")
    print("Dataset loaded successfully.")

    # Select 5 diverse articles by index
    indices = [10, 100, 200, 300, 400]
    
    selected_articles = []
    for i in indices:
        article = dataset[i]
        selected_articles.append({
            "id": article["id"],
            "article": article["article"],
            "highlights": article["highlights"]
        })
        print(f"Selected article with ID: {article['id']}")

    # Save the selected articles to a file
    output_path = "artifacts/selected_articles.json"
    with open(output_path, "w") as f:
        json.dump(selected_articles, f, indent=2)
    
    print(f"Successfully saved 5 articles to {output_path}")

if __name__ == "__main__":
    prepare_and_save_data()
