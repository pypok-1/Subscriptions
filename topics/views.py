from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TopicForm
from .models import Topic, TopicActivity


def topics_view(request: HttpRequest) -> HttpResponse:
    all_topics = Topic.objects.all()

    topics_key = "all_topics_cache"
    data = cache.get(topics_key)

    if data is None:
        data = Topic.objects.all()
        cache.set(topics_key, data, timeout=60)

    return render(request, "topics/topics.html", {
        "user_topics": data,
        "all_topics": all_topics,
    })


def subscribe_view(request: HttpRequest, id: int) -> HttpResponse:
    topic = get_object_or_404(Topic, id=id)
    if request.user.is_authenticated:
        topic.subscribers.add(request.user)
    return redirect("topics_list")


def unsubscribe_view(request: HttpRequest, id: int) -> HttpResponse:
    topic = get_object_or_404(Topic, id=id)
    if request.user.is_authenticated:
        topic.subscribers.remove(request.user)
    return redirect("topics_view")


def create_topic_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.save()
        return redirect('topics_view')


def delete_topic_view(request: HttpRequest, id:int) -> HttpResponse:
    topic = get_object_or_404(Topic, id=id)
        topic.delete()
        return redirect('topics_view')
