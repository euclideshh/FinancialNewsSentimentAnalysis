---
base_model: dccuchile/bert-base-spanish-wwm-cased
library_name: peft
tags:
- base_model:adapter:dccuchile/bert-base-spanish-wwm-cased
- lora
- transformers
---


# Model Card: finbeto-lora

## Purpose
`finbeto-lora` analyzes sentiment in Spanish financial news headlines. It is designed for financial text classification (positive, negative, neutral) in Spanish.

## Training Details
- **Base model:** `dccuchile/bert-base-spanish-wwm-cased`
- **Adapter:** LoRA (PEFT)
- **Datasets:**
	- `data/raw/financial_news.csv` (Spanish headlines)
	- `data/processed/financial_phrasebank_google_translate_es.csv` (PhraseBank, translated)
- **Key hyperparameters:**
	- learning_rate: ~2.8e-5
	- weight_decay: 0.1
	- num_train_epochs: 3
	- batch_size: 16 (train), 32 (eval)
	- LoRA rank: 4, alpha: 32, dropout: 0.1
- **Precision:** fp16

## Metrics
- Classification Report:
---
|               | precision | recall | f1-score | support |
|:--------------|:---------:|:------:|:--------:|--------:|
| Positive      |   0.78    |  0.69  |   0.73   |    1095 |
| Negative      |   0.73    |  0.82  |   0.77   |     898 |
| Neutral       |   0.78    |  0.81  |   0.80   |     750 |
|               |           |        |          |         |
| **accuracy**  |           |        | **0.76** |    2743 |
| **macro avg** | **0.77**  |**0.77**| **0.77** |    2743 |
| **weighted avg** | **0.77** |**0.76**| **0.76** |    2743 |
---
(See `notebooks/3_beto-bert_fine_tuning.ipynb` for details)

## Usage Example
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("model/finbeto-lora")
model = AutoModelForSequenceClassification.from_pretrained("model/finbeto-lora")

text = "La empresa reportó un crecimiento significativo en el último trimestre."
inputs = tokenizer(text, return_tensors="pt")
with torch.no_grad():
		logits = model(**inputs).logits
		pred = torch.argmax(logits, dim=1).item()
		print(["negative", "neutral", "positive"][pred])
```
## Contact:
For more information or to stay in touch, please visit:
https://github.com/euclideshh/FinancialNewsSentimentAnalysis

## License
MIT License