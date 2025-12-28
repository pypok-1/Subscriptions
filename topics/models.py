from django.contrib.auth.models import User
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='topics', blank=True)

    def __str__(self):
        return self.name


class TopicActivity(models.Model):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    action = models.CharField(
        max_length=20,
        choices=[('created', 'Created'), ('deleted', 'Deleted'), ('updated', 'Updated')]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic.name} - {self.action} at {self.created_at}"
