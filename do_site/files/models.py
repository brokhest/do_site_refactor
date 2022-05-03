from django.db import models
from Login.models import User
# Create your models here.


class File(models.Model):
    name = models.CharField(max_length=100, unique=False)
    user = models.ForeignKey(User, related_name='files',  on_delete=models.CASCADE)
    file = models.FileField(upload_to='')
    permission = models.BooleanField(default=False)
    # False - by word, True - to user
    permissioned_to = models.BooleanField(default=True)
    keyword = models.CharField(max_length=20, unique=False, blank=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def delete(self):
        self.file.delete()
        super().delete()