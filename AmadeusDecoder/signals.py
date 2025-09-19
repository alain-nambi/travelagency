from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import NotFetched

@receiver(post_save, sender=NotFetched)
def notify_pnr_update(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    data = {
        "pnr_number": instance.pnr_number,
        "follower": instance.follower.username,
        "status": instance.status,
    }
    async_to_sync(channel_layer.group_send)(
        "pnr_updates",
        {
            "type": "send_pnr_update",
            "data": data,
        }
    )
