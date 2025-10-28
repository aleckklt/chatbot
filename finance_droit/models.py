from django.db import models

class Conversation(models.Model):
    user_message = models.TextField(blank=True, null=True)
    bot_reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} - {self.user_message[:50]}"