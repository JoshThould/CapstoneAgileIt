from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Story

@receiver(post_delete, sender=Story)
def log_story_deletion(sender, instance, **kwargs):
    print(f"[Audit] Story deleted: '{instance.title}' (ID: {instance.id})")