from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/<int:id>/', views.subscribe_view, name='subscribe_view'),
    path('', views.topics_view, name='topics_view'),
    path("unsubscribe/<int:id>/", views.unsubscribe_view, name='unsubscribe_view'),
    path("delete/<int:id>/", views.delete_topic_view, name='delete_topic_view'),
    path("create/", views.create_topic_view, name='create_topic_view'),
]
