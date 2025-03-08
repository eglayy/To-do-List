from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Priority(models.Model):
    HIGH = 3
    MEDIUM = 2
    LOW = 1

    PRIORITY_CHOICES = [
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
    ]

    priority_level = models.IntegerField(choices=PRIORITY_CHOICES, default=MEDIUM)

    def __str__(self):
        return dict(self.PRIORITY_CHOICES)[self.priority_level]


class ToDoTags(models.Model):
    title = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TodoList(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField(max_length=512)
    date_of_note = models.DateTimeField()
    deadline = models.DateTimeField()
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(ToDoTags)
    image = models.ImageField(upload_to='todo_lists/', null=True, blank=True)
