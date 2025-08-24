
# Financial News Sentiment Analysis

## Project Overview
This project provides sentiment analysis for Spanish financial news headlines using a fine-tuned BERT-based model (finbeto-lora) with PEFT and LoRA. 

## Model
- **Model:** `finbeto-lora` (adapter for `dccuchile/bert-base-spanish-wwm-cased`)
- **Technique:** LoRA (PEFT)
- **Task:** Sentiment classification (positive, negative, neutral) in Spanish financial news
- **Location:** `model/finbeto-lora/`

## Architecture
```
├── LICENSE
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── model/
│   └── finbeto-lora/
├── notebooks/
├── tests/
```

## Requirements
- Python 3.8+
- See `requirements.txt` for essential packages

## Configuration
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/FinancialNewsSentimentAnalysis.git
    cd FinancialNewsSentimentAnalysis
    ```
2. Create a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Data
- **Raw:** `data/raw/financial_news.csv` (Spanish headlines)
- **Processed:** `data/processed/financial_phrasebank_google_translate_es.csv` (PhraseBank, translated)

## Evaluation
- **Accuracy:** ~0.83
- **F1-score:** ~0.83
- See `notebooks/3_beto-bert_fine_tuning.ipynb` for details

## License
MIT License. See `LICENSE` for details.