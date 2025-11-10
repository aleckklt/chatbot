from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import ask_ollama
from .models import Conversation

def chat_page(request):
    return render(request, "finance_droit/chatbot.html")


@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        if not user_message:
            return JsonResponse({"reply": "Veuillez entrer un message valide."})
        history = Conversation.objects.order_by("created_at")
        bot_reply = ask_ollama(user_message, history)
        Conversation.objects.create(user_message=user_message, bot_reply=bot_reply)
        return JsonResponse({"reply": bot_reply})
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)