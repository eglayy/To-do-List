from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ToDoTags(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class TodoList(models.Model):
    HIGH = 3
    MEDIUM = 2
    LOW = 1

    PRIORITY_CHOICES = [
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
    ]

    title = models.CharField(max_length=256, verbose_name="Название")
    body = models.TextField(max_length=512, default="", verbose_name="To-do лист")
    image = models.ImageField(upload_to='todo_lists/', null=True, blank=True, verbose_name="Фото")
    deadline = models.DateTimeField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=MEDIUM)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(ToDoTags, verbose_name="Теги", blank=True)
