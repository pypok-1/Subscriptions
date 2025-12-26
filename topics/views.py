from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TopicForm
from .models import Topic


@login_required
def topics_view(request: HttpRequest) -> HttpResponse:
    ''' Відображає список усіх тем, використовуючи кешування для конкретного користувача для оптимізації запитів. '''
    topics_key = f"user:{request.user.id}:topics"
    data = cache.get(topics_key)

    if data is None:
        # views.py
        data = Topic.objects.prefetch_related('subscribers').all()
        cache.set(topics_key, data, timeout=60)

    return render(request, "topics/topics.html", {
        "topics": data,
    })


@login_required
def create_topic_view(request: HttpRequest) -> HttpResponse:
    ''' Створює нову тему через форму, очищує загальний кеш тем після успішного збереження та перенаправляє на список. '''
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            cache.delete("all_topics_cache")
            return redirect('topics_view')
    else:
        form = TopicForm()
    return render(request, 'topics/create_topic.html', {'form': form})


@login_required
def delete_topic_view(request: HttpRequest, id: int) -> HttpResponse:
    ''' Видаляє тему за її ID та перенаправляє користувача до загального списку тем. '''
    topic = get_object_or_404(Topic, id=id)
    topic.delete()
    return redirect('topics_view')


@login_required
def subscribe_view(request: HttpRequest, id: int) -> HttpResponse:
    ''' Підписує користувача на обрану тему, скидає загальний кеш та повертає до списку тем. '''
    topic = get_object_or_404(Topic, id=id)
    if request.user.is_authenticated:
        topic.subscribers.add(request.user)
        cache.delete("all_topics_cache")
    return redirect("topics_view")


@login_required
def unsubscribe_view(request: HttpRequest, id: int) -> HttpResponse:
    ''' Відписує користувача від теми, видаляє застарілий кеш та перенаправляє на сторінку тем. '''
    topic = get_object_or_404(Topic, id=id)
    if request.user.is_authenticated:
        topic.subscribers.remove(request.user)
        cache.delete("all_topics_cache")
    return redirect("topics_view")
