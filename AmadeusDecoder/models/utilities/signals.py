from django.db.models.signals import post_save
from django.dispatch import receiver
from AmadeusDecoder.models.pnr.Pnr import Pnr 
from .Comments import NotFetched

@receiver(post_save, sender=Pnr)
def mark_not_fetched_as_fetched(sender, instance, created, **kwargs):
    """
    Quand un PNR est créé dans t_pnr, on marque les correspondants dans NotFetched comme "remonté"
    """
    if created:
        NotFetched.objects.filter(pnr_number=instance.number, status=1).update(status=0)