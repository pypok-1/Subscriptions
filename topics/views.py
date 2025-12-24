from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .models import Topic, TopicActivity


@login_required
def topics_view(request: HttpRequest) -> HttpResponse:
    topics_key = f"user:{request.user.id}:topics"
    data = cache.get(f"user:{request.user.id}:topics")
    if data is None:
        data = request.user.topics.all()
        cache.set(topics_key, data, timeout=60)

    return render(request, "topics/topics.html", {"user_topics": data})


@login_required
def subscribe_view(request: HttpRequest, id: int) -> HttpResponse:
    topic = get_object_or_404(Topic, id=id)
    topic.subscribers.add(request.user)
    return redirect("topics_list")


@login_required
def unsubscribe_view(request: HttpRequest, id: int) -> HttpResponse:
    topic = get_object_or_404(Topic, id=id)
    topic.subscribers.remove(request.user)
    return redirect("topics_list")

