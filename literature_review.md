## Literature Review

### Research Area Overview
The research area of AI-to-human communication focuses on making AI-generated information more understandable and trustworthy for human users. This involves investigating how to present information concisely, provide explanations for AI decisions, and design human-AI interactions that are effective and user-friendly. A key challenge is bridging the gap between the dense, comprehensive information that AIs process and the concise, actionable information that humans prefer. This research area draws from Human-Computer Interaction (HCI), Explainable AI (XAI), and Natural Language Processing (NLP).

### Key Papers

#### Paper 1: Towards Human-centered Design of Explainable Artificial Intelligence (XAI): A Survey of Empirical Studies
- **Authors**: Shuai Ma
- **Year**: 2024
- **Source**: arXiv:2410.21183
- **Key Contribution**: This survey provides a framework for human-centered XAI design. It reviews the design space of XAI, including explanation types, interactivity, and modality. It also covers evaluation metrics and common findings from empirical studies.
- **Methodology**: The paper is a systematic survey of empirical studies in human-centered XAI.
- **Datasets Used**: Not applicable (survey paper).
- **Results**: The paper finds that there is a need for more user-centered and context-aware XAI design. It also highlights the lack of standardized evaluation methods for XAI. The paper proposes a framework for human-centered XAI design that includes three stages: identifying the design goal, designing the explanatory interface, and evaluating with human subjects.
- **Code Available**: No.
- **Relevance to Our Research**: This paper is highly relevant as it provides a comprehensive overview of the research area and a framework for designing and evaluating XAI systems. It directly informs the methodology for the current research project.

#### Paper 2: DODO: Dynamic Contextual Compression for Decoder-only LMs
- **Authors**: Guanghui Qin, Nikhil Rao, Corby Rosset, Ethan C. Chau, Benjamin Van Durme
- **Year**: 2024
- **Source**: arXiv:2407.01684
- **Key Contribution**: The paper proposes DODO, a method for dynamic contextual compression in decoder-only language models. DODO can represent text with a dynamic number of hidden states, reducing the computational cost of self-attention.
- **Methodology**: DODO is implemented as a modification to a standard transformer model. It uses a "Scorer" network to select which tokens to keep as "nuggets" for the context.
- **Datasets Used**: The Pile, WikiText-103, SQuAD, CNN/DailyMail.
- **Results**: DODO is shown to achieve significant compression ratios (up to 20x) with minimal loss of performance on tasks like language modeling, question answering, and summarization.
- **Code Available**: Not specified, but the paper mentions using huggingface/PEFT.
- **Relevance to Our Research**: This paper is highly relevant to the research hypothesis. The concept of "nuggets" and contextual compression directly addresses the idea of making AI communication more concise. DODO could be a key technology for the experimental phase of this research.

#### Paper 3: Human-in-the-loop Abstractive Dialogue Summarization
- **Authors**: Jiaao Chen, Mohan Dodda, and Diyi Yang
- **Year**: 2023
- **Source**: Findings of the Association for Computational Linguistics: ACL 2023 (arXiv:2212.09750)
- **Key Contribution**: The paper proposes a method for incorporating human feedback into the training process of abstractive dialogue summarization models to improve the quality of generated summaries.
- **Methodology**: The authors use a Reinforcement Learning framework to fine-tune a dialogue summarization model with two types of human feedback: local (highlighting salient information) and global (comparing summaries).
- **Datasets Used**: Not explicitly mentioned in the summary, but the paper conducted experiments on "multiple datasets".
- **Results**: The proposed method outperforms supervised baselines, especially in human evaluations.
- **Code Available**: Not specified.
- **Relevance to Our Research**: This paper is highly relevant as it directly addresses the "human-in-the-loop" aspect of the research hypothesis. It provides a concrete example of how human feedback can be used to improve AI-generated summaries, which is a key part of making AI communication more effective.

**Note on Paper 3:** There was a discrepancy in the `papers` directory. The file `2305.12195_Human_in_the_Loop_Summarization.pdf` contained a paper on solid-state physics. The correct paper, "Human-in-the-loop Abstractive Dialogue Summarization", has arXiv ID `2212.09750`. The summary above is for the correct paper.

### Common Methodologies
- **Human-in-the-loop Reinforcement Learning**: Used to fine-tune models based on human feedback (Paper 3).
- **Contextual Compression**: Dynamically compressing the context for language models (Paper 2).
- **Systematic Literature Review**: Used to survey the field of human-centered XAI (Paper 1).

### Standard Baselines
- **Supervised Baselines**: Standard transformer models fine-tuned on specific tasks (Paper 3).
- **In-Context Autoencoder (ICAE)**: A baseline for context compression (Paper 2).

### Evaluation Metrics
- **Human Evaluation**: Considered the gold standard for summarization and XAI tasks (Paper 1, Paper 3).
- **BLEU**: For autoencoding reconstruction quality (Paper 2).
- **Perplexity**: For language modeling (Paper 2).
- **ROUGE**: For summarization (not explicitly in the papers, but a standard metric).
- **Task-specific metrics**: Accuracy for QA, etc. (Paper 2).

### Datasets in the Literature
- **The Pile**: A large, diverse text corpus (Paper 2).
- **WikiText-103**: For language modeling (Paper 2).
- **SQuAD**: For question answering (Paper 2).
- **CNN/DailyMail**: For summarization (Paper 2).

### Gaps and Opportunities
- **Lack of standardized evaluation for XAI**: Paper 1 highlights this as a major challenge.
- **Need for more user-centered and context-aware XAI design**: Also from Paper 1.
- **Exploring different types of human feedback**: Paper 3 focuses on local and global feedback, but other types could be explored.
- **Applying contextual compression to more tasks**: Paper 2 focuses on a few tasks, but the technique could be more broadly applied.

### Recommendations for Our Experiment
- **Recommended datasets**: SQuAD for question answering and CNN/DailyMail for summarization are good starting points.
- **Recommended baselines**: Standard fine-tuned language models (e.g., from Hugging Face) would be appropriate baselines.
- **Recommended metrics**: A combination of automated metrics (ROUGE, accuracy) and human evaluation will be crucial.
- **Methodological considerations**: The DODO model from Paper 2 appears to be a very promising technology to investigate for making AI communication more concise. An experiment could compare the performance of a DODO-compressed model to a full model on a downstream task, both in terms of task performance and human perception of conciseness and clarity. The human-in-the-loop approach from Paper 3 could also be incorporated to further refine the model's output.
