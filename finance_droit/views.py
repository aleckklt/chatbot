from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import ask_ollama

def chat_page(request):
    return render(request, "finance_droit/chatbot.html")

@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        response = ask_ollama(user_message)
        return JsonResponse({"reply": response})
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
