from django.db import models
from django.contrib.auth.models import User


class TodoListModel(models.Model):
    STATUS_CHOICES =(
    ("START", "START"),
    ("IN-PROGRESS", "IN-PROGRESS"),
    ("DONE", "DONE"),
    )
    title = models.CharField(max_length=100)
    details=models.TextField(max_length=200)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.title
