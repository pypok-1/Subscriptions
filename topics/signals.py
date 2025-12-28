from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver, Signal
from django.core.cache import cache
from .models import Topic, TopicActivity

topic_changed = Signal()


@receiver(m2m_changed, sender=Topic.subscribers.through)
def handle_m2m_changed(sender, instance, action, pk_set, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        if pk_set:
            for user_id in pk_set:
                cache.delete(f"user:{user_id}:topics")
        else:
            for user in instance.subscribers.all():
                cache.delete(f"user {user.id}")


@receiver(post_save, sender=Topic)
def topic_post_save(sender, instance, created, **kwargs):
    if created:
        TopicActivity.objects.create(topic_id=instance.id, topic_name=instance.name, action="created")
        topic_changed.send(sender=sender, topic_id=instance.id, action="created", instance=instance)


@receiver(post_delete, sender=Topic)
def topic_post_delete(sender, instance, **kwargs):
    TopicActivity.objects.create(topic_id=instance.id, topic_name=instance.name, action="deleted")
    topic_changed.send(sender=sender, topic_id=instance.id, action="deleted", instance=instance)


@receiver(topic_changed)
def handle_topic_changed(sender, topic_id, action, instance, **kwargs):
    print(f"Topic {topic_id} changed: {action}")
    for user in instance.subscribers.all():
        cache.delete(f"user:{user.id}:topics")
