from django.db import models
from accounts.models import User


class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title
