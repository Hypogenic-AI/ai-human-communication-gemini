
import json
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from collections import Counter

RESULTS_PATH = "results/evaluation_results.json"
ANALYSIS_OUTPUT_PATH = "results/analysis_summary.txt"
PLOT_OUTPUT_PATH = "results/accuracy_comparison.png"

def analyze_results():
    """
    Loads the evaluation results, performs statistical analysis,
    and generates a summary and plots.
    """
    with open(RESULTS_PATH, "r") as f:
        results = json.load(f)

    # --- 1. Accuracy Analysis ---
    accuracies = {
        "dense": [],
        "hierarchical": [],
        "qa_interface": []
    }

    for res in results:
        for method in accuracies.keys():
            accuracies[method].append(res["scores"][method]["accuracy"])

    avg_accuracies = {method: np.mean(acc) for method, acc in accuracies.items()}
    std_accuracies = {method: np.std(acc) for method, acc in accuracies.items()}

    # --- 2. Statistical Testing (Paired T-test) ---
    # Comparing Hierarchical and Q&A against the Dense baseline
    ttest_hierarchical_vs_dense = stats.ttest_rel(accuracies["hierarchical"], accuracies["dense"])
    ttest_qa_vs_dense = stats.ttest_rel(accuracies["qa_interface"], accuracies["dense"])

    # --- 3. Preference Analysis ---
    # We'll use a simple scoring system: 1st place = 3 pts, 2nd = 2, 3rd = 1
    preference_scores = Counter()
    for res in results:
        ranking = res.get("preference", [])
        for i, method_char in enumerate(ranking):
            # Convert 'A', 'B', 'C' to method names
            method_map = {'A': 'dense', 'B': 'hierarchical', 'C': 'qa_interface'}
            method_name = method_map.get(method_char)
            if method_name:
                score = 3 - i
                preference_scores[method_name] += score
    
    # --- 4. Generate Analysis Summary ---
    summary = []
    summary.append("--- Experiment Analysis Summary ---")
    summary.append("\n1. Comprehension Accuracy:")
    for method in accuracies.keys():
        summary.append(f"  - {method.capitalize()}: Mean = {avg_accuracies[method]:.2f}, Std = {std_accuracies[method]:.2f}")

    summary.append("\n2. Statistical Significance (Paired T-test vs. Dense Baseline):")
    summary.append(f"  - Hierarchical vs. Dense: statistic={ttest_hierarchical_vs_dense.statistic:.3f}, p-value={ttest_hierarchical_vs_dense.pvalue:.3f}")
    summary.append(f"  - Q&A Interface vs. Dense: statistic={ttest_qa_vs_dense.statistic:.3f}, p-value={ttest_qa_vs_dense.pvalue:.3f}")

    summary.append("\n3. Simulated User Preference (Score based on ranking):")
    for method, score in preference_scores.most_common():
        summary.append(f"  - {method.capitalize()}: {score} points")

    summary_text = "\n".join(summary)
    print(summary_text)

    with open(ANALYSIS_OUTPUT_PATH, "w") as f:
        f.write(summary_text)
    
    print(f"\nAnalysis summary saved to {ANALYSIS_OUTPUT_PATH}")

    # --- 5. Generate Plot ---
    methods = list(avg_accuracies.keys())
    means = list(avg_accuracies.values())
    stds = list(std_accuracies.values())

    fig, ax = plt.subplots()
    ax.bar(methods, means, yerr=stds, capsize=5, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    ax.set_ylabel('Mean Comprehension Accuracy')
    ax.set_title('Comparison of Communication Methods')
    ax.set_ylim(0, 1)

    plt.savefig(PLOT_OUTPUT_PATH)
    print(f"Accuracy comparison plot saved to {PLOT_OUTPUT_PATH}")


if __name__ == "__main__":
    analyze_results()
