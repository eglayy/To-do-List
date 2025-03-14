from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ToDoTags(models.Model):
    title = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TodoList(models.Model):
    HIGH = 3
    MEDIUM = 2
    LOW = 1

    PRIORITY_CHOICES = [
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
    ]

    title = models.CharField(max_length=256)
    body = models.TextField(max_length=512, default="")
    deadline = models.DateTimeField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=MEDIUM)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(ToDoTags)
    image = models.ImageField(upload_to='todo_lists/', null=True, blank=True)
