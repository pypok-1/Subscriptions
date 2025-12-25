from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TopicForm
from .models import Topic, TopicActivity


@login_required
def topics_view(request: HttpRequest) -> HttpResponse:
    topics_key = f"user:{request.user.id}:topics"
    data = cache.get(topics_key)

    if data is None:
        data = request.user.topics.all()
        cache.set(topics_key, data, timeout=60)

    all_topics = Topic.objects.all()
    return render(request, "topics/topics.html",{
        "user_topics": data,
        "all_topics": all_topics,
    })


@login_required
def subscribe_view(request: HttpRequest, id: int) -> HttpResponse:
    topic = get_object_or_404(Topic, id=id)
    topic.subscribers.add(request.user)
    return redirect("topics_list")


@login_required
def unsubscribe_view(request: HttpRequest, id: int) -> HttpResponse:
    topic = get_object_or_404(Topic, id=id)
    topic.subscribers.remove(request.user)
    return redirect("topics_view")


@login_required
def create_topic_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
        return redirect('topics_view')


@login_required
def delete_topic_view(request: HttpRequest, id:int) -> HttpResponse:
    topic = get_object_or_404(Topic, id=id)
    if topic.author == request.user:
        topic.delete()
        return redirect('topics_view')
