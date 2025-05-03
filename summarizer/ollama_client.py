import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

def summarize_with_ollama(content, model="llama3.2"):
    prompt = f"Summarize the following webpage content clearly and concisely:\n\n{content[:3000]}"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes webpage content."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    
    if response.status_code == 200:
        return response.json()['message']['content']
    else:
        raise Exception(f"Ollama API Error: {response.text}")
