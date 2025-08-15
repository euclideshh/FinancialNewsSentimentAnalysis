# Financial News Sentiment Analysis

This project implements a sentiment analysis system for Spanish financial news using a fine-tuned FinBERT model with Parameter-Efficient Fine-Tuning (PEFT) and Low-Rank Adaptation (LoRA). The project addresses the issue of class imbalance in the dataset through back-translation.

## Project Structure

```
├── .gitignore             # Git ignore rules
├── LICENSE                # Project license
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── setup.py               # Package setup file
├── config/                # Configuration files
├── data/                  # Data directory
│   ├── raw/               # Raw data files
│   └── processed/         # Processed data files
├── notebooks/             # Jupyter notebooks for exploration and model training
├── src/                   # Source code
│   └── llm/               # Trained model files
└── tests/                 # Test files
```

## Data

The project uses a dataset of Spanish financial news headlines. The original dataset is located in `data/raw/financial_news.csv`. Due to a class imbalance (fewer "neutral" samples), the dataset was balanced using back-translation. The balanced dataset is stored in `data/processed/financial_news_balanced.csv`.

## Model

The sentiment analysis model is a fine-tuned version of the `ProsusAI/finbert` model. The fine-tuning process uses Parameter-Efficient Fine-Tuning (PEFT) with Low-Rank Adaptation (LoRA) to efficiently adapt the model to the Spanish financial news domain. The trained model is saved in `src/llm/finbert-lora-spanish`.

## Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/FinancialNewsSentimentAnalysis.git
    cd FinancialNewsSentimentAnalysis
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The project is organized into three main notebooks that demonstrate the entire workflow:

1.  **`notebooks/1_data_exploration.ipynb`**: This notebook performs an initial exploratory data analysis of the raw dataset.
2.  **`notebooks/2_imbalance_handling_with_back_translation.ipynb`**: This notebook demonstrates how the class imbalance is addressed using back-translation.
3.  **`notebooks/3_finbert_fine_tuning.ipynb`**: This notebook shows the process of fine-tuning the FinBERT model with PEFT and LoRA.

To run the notebooks, start the Jupyter server:
```bash
jupyter notebook
```

## Testing

Run tests using pytest:
```bash
pytest tests/
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.