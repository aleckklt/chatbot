from django.shortcuts import render

def chatbot(request):
    return render(request, 'finance_droit/chatbot.html')