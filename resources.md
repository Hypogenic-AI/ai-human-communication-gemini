## Resources Catalog

### Summary
This document catalogs all resources gathered for the research project, including papers, datasets, and code repositories. It also documents the research process undertaken in this workspace.

### Papers
Total papers downloaded: 3

| Title | Authors | Year | File | Key Info |
|---|---|---|---|---|
| Towards Human-centered Design of Explainable Artificial Intelligence (XAI): A Survey of Empirical Studies | Shuai Ma | 2024 | papers/2410.21183_Towards_Human_centered_Design_of_Explainable_Artificial_Intelligence.pdf | Survey of human-centered XAI. |
| DODO: Dynamic Contextual Compression for Decoder-only LMs | Guanghui Qin, et al. | 2024 | papers/2407.01684_FineSurE.pdf | Proposes a method for context compression. |
| Human-in-the-loop Abstractive Dialogue Summarization | Jiaao Chen, et al. | 2023 | papers/2305.12195_Human_in_the_Loop_Summarization.pdf | Incorporates human feedback for summarization. |

See papers/README.md for detailed descriptions.

### Datasets
Total datasets documented: 3

| Name | Source | Size | Task | Location | Notes |
|---|---|---|---|---|---|
| WikiText-103 | HuggingFace | ~103M words | Language Modeling | datasets/ | Download instructions in README.md |
| SQuAD | HuggingFace | 100,000+ | Question Answering | datasets/ | Download instructions in README.md |
| CNN/DailyMail | HuggingFace | ~300,000+ | Summarization | datasets/ | Download instructions in README.md |

See datasets/README.md for detailed descriptions.

### Code Repositories
Total repositories cloned: 0

| Name | URL | Purpose | Location | Notes |
|---|---|---|---|---|
| DODO | https://github.com/hiaoxui/DODO | Implementation of DODO paper | code/ | Not found |

See code/README.md for detailed descriptions.

### Research Process Documentation

This section documents the research executed in this workspace, as per the final step of the research methodology.

1.  **Planning (`planning.md`):** A detailed research plan was created to test the hypothesis that structured communication formats are more effective than dense summaries. The plan proposed a simulated user study using LLMs to measure comprehension accuracy and user preference.

2.  **Environment Setup:** An isolated Python environment was created using `uv`. Dependencies were installed, including `openai`, `datasets`, `numpy`, `scipy`, and `matplotlib`. All dependencies are listed in `requirements.txt`.

3.  **Data Preparation (`src/prepare_data.py`):** 5 articles were selected from the `cnn_dailymail` test set to serve as the source of "dense information" for the experiment. These were saved to `artifacts/selected_articles.json`.

4.  **Implementation & Experimentation (`src/run_experiment.py`):**
    *   **Artifact Generation:** For each of the 5 articles, three communication artifacts were generated using `gpt-4o`: a dense summary, a hierarchical summary, and a Q&A interface. These were saved in `results/generated_artifacts.json`.
    *   **Evaluation:** A simulated "junior analyst" (`gpt-3.5-turbo`) was tasked with answering 10 ground-truth questions per article, using only the information from one of the three artifacts. The answers were scored for accuracy by another LLM call. A simulated user preference was also recorded. The full evaluation results were saved in `results/evaluation_results.json`.

5.  **Analysis (`src/analyze_results.py`):** The evaluation results were analyzed to calculate mean accuracies and statistical significance. The key finding was a disconnect between performance and preference: the dense summary was most accurate, but the hierarchical summary was most preferred. The analysis and a plot were saved in `results/analysis_summary.txt` and `results/accuracy_comparison.png`.

6.  **Documentation (`REPORT.md`, `README.md`):** The entire process, methodology, results, and conclusions were documented in a comprehensive research report and a summary README file.