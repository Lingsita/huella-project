from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Chat(models.Model):
    emisor=models.ForeignKey(User, related_name='chat_emisor')
    receptor= models.ForeignKey(User, related_name='chat_receptor')
    comentario = models.CharField(max_length=200)
    active=models.BooleanField(default=True)


