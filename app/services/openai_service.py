import requests
import os
from flask import current_app as app
import requests

api_key = os.getenv("OPENAI_API_KEY")

def query_gpt3(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.15,
        "max_tokens": 400
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()  # This will raise an exception for HTTP error codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": str(e)}
