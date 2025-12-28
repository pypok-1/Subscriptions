from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib import messages

from .forms import TopicForm
from .models import Topic


@login_required 
def topics_view(request: HttpRequest) -> HttpResponse:
    user = request.user

    topics_key = f'user:{user.id}:topics'
    topic_ids = cache.get(topics_key)

    if topic_ids is None:
        topic_ids = list(Topic.objects.filter(subscribers=user).values_list('id', flat=True))
        cache.set(topics_key, topic_ids, timeout=60)

    topics = Topic.objects.filter(id__in=topic_ids).order_by('-id')

    paginator = Paginator(topics, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_topics = Topic.objects.exclude(id__in=topic_ids).order_by('-id')[:10]

    return render(request, 'topics/topics.html', {
        'page_obj': page_obj,
        'all_topics': all_topics,
    })


@login_required
def create_topic_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.created_by = request.user
            topic.save()
            topic.subscribers.add(request.user)
            return redirect('topics_view')
    else:
        form = TopicForm()

    return render(request, 'topics/create_topic.html', {'form': form})


@login_required
def delete_topic_view(request: HttpRequest, id: int) -> HttpResponse:
    topic = get_object_or_404(Topic, id=id)

    if topic.created_by == request.user or request.user.is_staff:
        if request.method == "POST":
            topic.delete()

    return redirect("topics_view")


@login_required
def subscribe_view(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        topic = get_object_or_404(Topic, id=id)
        topic.subscribers.add(request.user)
    return redirect("topics_view")


@login_required
def unsubscribe_view(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        topic = get_object_or_404(Topic, id=id)
        topic.subscribers.remove(request.user)
    return redirect("topics_view")
