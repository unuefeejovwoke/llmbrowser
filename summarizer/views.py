from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import fetch_webpage, summarize_text
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def home(request):
    summary = None
    if request.method == "POST":
        url = request.POST.get("url")
        try:
            content = fetch_webpage(url)
            summary = summarize_text(content)
        except Exception as e:
            summary = f"Error: {str(e)}"
    return render(request, "summarizer/home.html", {"summary": summary})


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
