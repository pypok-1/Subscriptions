from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TopicForm
from .models import Topic


@login_required
def topics_view(request: HttpRequest) -> HttpResponse:
    ''' Відображає список тем із використанням кешу за ключем user:{user_id}:topics на 60 секунд. '''
    topics_key = f"user:{request.user.id}:topics"
    data = cache.get(topics_key)

    if data is None:
        data = Topic.objects.prefetch_related('subscribers').all()
        cache.set(topics_key, data, timeout=60)

    return render(request, "topics/topics.html", {"topics": data})


@login_required
def create_topic_view(request: HttpRequest) -> HttpResponse:
    ''' Створює тему через форму; очищення кешу та активність тут не прописуються (це робота сигналів). '''
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('topics_view')
    else:
        form = TopicForm()
    return render(request, 'topics/create_topic.html', {'form': form})


@login_required
def delete_topic_view(request: HttpRequest, id: int) -> HttpResponse:
    ''' Видаляє тему; інвалідація кешу та запис активності покладаються на сигнали. '''
    topic = get_object_or_404(Topic, id=id)
    topic.delete()
    return redirect('topics_view')


@login_required
def subscribe_view(request: HttpRequest, id: int) -> HttpResponse:
    ''' Додає користувача до підписників теми; логіка кешу тут не зачіпається. '''
    topic = get_object_or_404(Topic, id=id)
    if request.user.is_authenticated:
        topic.subscribers.add(request.user)
    return redirect("topics_view")


@login_required
def unsubscribe_view(request: HttpRequest, id: int) -> HttpResponse:
    ''' Видаляє користувача з підписників теми; без ручного очищення кешу. '''
    topic = get_object_or_404(Topic, id=id)
    if request.user.is_authenticated:
        topic.subscribers.remove(request.user)
    return redirect("topics_view")
