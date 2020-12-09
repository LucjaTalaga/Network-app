from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self')

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    content = models.CharField(max_length=8900)
    liked_by = models.ManyToManyField(User, blank=True, related_name="liked_by")

    def __str__(self):
        return f"{self.id}"
