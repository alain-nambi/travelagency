from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from AmadeusDecoder.models.pnr.Pnr import Pnr 
from .Comments import NotFetched

@receiver(post_save, sender=Pnr)
def mark_not_fetched_as_fetched(sender, instance, created, **kwargs):
    if created:
        # Utiliser une boucle pour déclencher auto_now
        not_fetched_items = NotFetched.objects.filter(pnr_number=instance.number, status=1)
        for item in not_fetched_items:
            item.status = 0
            item.save()  # Ceci déclenchera auto_now pour updated_at