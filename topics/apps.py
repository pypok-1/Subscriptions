from django.apps import AppConfig


class TopicsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'topics'

    def ready(self):
        from . import signals
        signals.topic_changed.connect(signals.handle_topic_changed)