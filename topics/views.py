from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib import messages

from .forms import TopicForm
from .models import Topic


@login_required
def topics_view(request):
    topics_key = f"user:{request.user.id}:topics"

    topics_us = cache.get(topics_key)

    if topics_us is None:
        topics_us = list(request.user.topics.all())
        cache.set(topics_key, topics_us, 60)
        print("бази даних")
    else:
        print("кешу")

    all_topics = Topic.objects.all()

    return render(request, "topics/topics.html", {
        "all_topics": all_topics,
        "topics_us": topics_us
    })


@login_required
def create_topic_view(request):
    if request.method == "POST":
        topic_name = request.POST.get("name", "")
        if topic_name:
            Topic.objects.get_or_create(name=topic_name)
    return redirect("topics_view")


@login_required
def subscribe_view(request, id):
    if request.method == "POST":
        topic = get_object_or_404(Topic, id=id)
        topic.subscribers.add(request.user)
    return redirect("topics_view")


@login_required
def unsubscribe_view(request, id):
    if request.method == "POST":
        topic = get_object_or_404(Topic, id=id)
        topic.subscribers.remove(request.user)
    return redirect("topics_view")


@login_required
def delete_topic_view(request, id):
    if request.method == "POST":
        Topic.objects.filter(id=id).delete()
    return redirect("topics_view")
