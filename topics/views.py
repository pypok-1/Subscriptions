from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .models import Topic, TopicActivity


@login_required
def topics_view(request: HttpRequest) -> HttpResponse:
    data = cache.get(f"user:{request.user.id}:topics")
    if data is None:
        request.user.topics.all()

        
