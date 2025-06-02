import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_section_content(prompt: str, model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1", temperature: float = 0.7) -> str:
    
    api_token = os.getenv("HF_ACCESS_TOKEN")
    endpoint = f"https://api-inference.huggingface.co/models/{model}"

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": prompt,
        "parameters": {
            "temperature": temperature,
            "max_new_tokens": 512,
            "return_full_text": False
        }
    }

    response = requests.post(endpoint, headers=headers, json=data)
    response.raise_for_status()
    output = response.json()

    # Hugging Face returns a list of dicts with 'generated_text'
    if isinstance(output, list) and len(output) > 0 and 'generated_text' in output[0]:
        return output[0]['generated_text']
    else:
        raise ValueError(f"Unexpected response from HF API: {output}")

