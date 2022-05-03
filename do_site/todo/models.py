from django.db import models
from Login.models import User, UserManager
from datetime import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    desc = models.TextField(null=True, blank=True)
    completion = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='tasks',  on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.SET_NULL, null=True, default=None)

    objects = UserManager()

    def __str__(self):
        return self.title

