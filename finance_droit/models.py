from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation de {self.user.username} le {self.created_at.strftime('%Y-%m-%d')}"

class Message(models.Model):

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.CharField(max_length=20, choices=[('user', 'Utilisateur'), ('bot', 'IA')])
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.sender} : {self.text[:50]}"
