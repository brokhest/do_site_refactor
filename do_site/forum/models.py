from django.db import models
from Login.models import User

# Create your models here.


class Message(models.Model):
    text = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='messages',on_delete=models.CASCADE)


