import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return ' '.join(soup.get_text(separator=' ', strip=True).split())

def summarize_text(text):
    messages = [
        {"role": "system", "content": "Summarize the webpage content clearly and concisely."},
        {"role": "user", "content": text[:4000]}
    ]
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content
