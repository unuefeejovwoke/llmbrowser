from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import fetch_webpage, summarize_text
from .ollama_client import summarize_with_ollama
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def home(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            url = data.get("url")
            content = fetch_webpage(url)
            summary = summarize_text(content)
            return JsonResponse({"summary": summary})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "summarizer/home.html")


def teach_yoruba_chat(request):
    return render(request, "summarizer/yoruba_chat.html")

@csrf_exempt
def teach_yoruba(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_prompt = data.get("prompt", "How to greet in Yoruba")

            messages = [
                {"role": "system", "content": "Teach me Yoruba by text"},
                {"role": "user", "content": user_prompt}
            ]

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

            result = response.choices[0].message.content
            return JsonResponse({"success": True, "response": result})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid HTTP method"}, status=405)


def summarize_ollama(request):
    if request.method == "GET":
        return render(request, "summarizer/ollama.html")
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            url = data.get("url")
            content = fetch_webpage(url)
            summary = summarize_with_ollama(content)
            return JsonResponse({"summary": summary})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)

