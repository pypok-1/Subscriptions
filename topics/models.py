from django.contrib.auth.models import User
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='topics', blank=True)


class TopicActivity(models.Model):
    action = models.CharField(
        max_length=20,
        choices=[('created', 'Created'), ('deleted', 'Deleted'), ('updated', 'Updated')] )
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='activities')


