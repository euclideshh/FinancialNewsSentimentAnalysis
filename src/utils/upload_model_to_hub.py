"""
This script is to upload the trained model and tokenizer to Hugging Face Hub.
"""
    
import os
from dotenv import load_dotenv
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def upload_final_model():
    load_dotenv()
    # Setting path and repository ID    
    local_model_path = "../../model/finbeto-lora"
    repo_id = os.getenv("repo_id")

    # Load trained model    
    model = AutoModelForSequenceClassification.from_pretrained(local_model_path, num_labels=3)
    tokenizer = AutoTokenizer.from_pretrained(local_model_path)        
    
    try:
        print(f"🚀 Uploading the model from {local_model_path} to the repository: {repo_id}")
        model.push_to_hub(
            repo_id=repo_id,
            commit_message="Committing final model"
        )
        tokenizer.push_to_hub(
            repo_id=repo_id,
            commit_message="Committing tokenizer files"
        )
        print("✅ Model and tokenizer uploaded successfully!")
        print(f"You can see your model at: https://huggingface.co/{repo_id}")

    except Exception as e:
        print(f"❌ An error occurred during the upload: {e}")

if __name__ == "__main__":
    upload_final_model()