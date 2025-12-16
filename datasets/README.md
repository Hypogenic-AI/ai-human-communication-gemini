# Downloaded Datasets

This directory contains datasets for the research project. Data files are NOT
committed to git due to size. Follow the download instructions below.

## Dataset 1: WikiText-103

### Overview
- **Source**: [https://huggingface.co/datasets/wikitext](https://huggingface.co/datasets/wikitext)
- **Size**: ~103M words
- **Format**: HuggingFace Dataset
- **Task**: Language Modeling
- **Splits**: train, validation, test
- **License**: Creative Commons Attribution-ShareAlike 4.0 International License

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset
dataset = load_dataset("wikitext", "wikitext-103-v1")
dataset.save_to_disk("datasets/wikitext-103")
```

### Loading the Dataset

Once downloaded, load with:
```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/wikitext-103")
```

## Dataset 2: Stanford Question Answering Dataset (SQuAD)

### Overview
- **Source**: [https://huggingface.co/datasets/squad](https://huggingface.co/datasets/squad)
- **Size**: 100,000+ question-answer pairs
- **Format**: HuggingFace Dataset
- **Task**: Question Answering
- **Splits**: train, validation
- **License**: CC BY-SA 4.0

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset
dataset = load_dataset("squad")
dataset.save_to_disk("datasets/squad")
```

### Loading the Dataset

Once downloaded, load with:
```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/squad")
```

## Dataset 3: CNN/DailyMail

### Overview
- **Source**: [https://huggingface.co/datasets/cnn_dailymail](https://huggingface.co/datasets/cnn_dailymail)
- **Size**: ~300,000+ articles
- **Format**: HuggingFace Dataset
- **Task**: Summarization
- **Splits**: train, validation, test
- **License**: Apache-2.0

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset
dataset = load_dataset("cnn_dailymail", "3.0.0")
dataset.save_to_disk("datasets/cnn_dailymail")
```

### Loading the Dataset

Once downloaded, load with:
```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/cnn_dailymail")
```
