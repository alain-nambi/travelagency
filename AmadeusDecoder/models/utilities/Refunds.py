from django.contrib.postgres.fields import HStoreField
from django.db import models
from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.user.Users import User

class Refunds(models.Model):

    class Meta:
        db_table = 't_refunds'
        
    pnr = models.ForeignKey(Pnr, on_delete=models.CASCADE)
    number = models.CharField(max_length=100, unique=True, null=True)
    total = models.DecimalField(max_digits=13, decimal_places=4, default=0.0)
    issuing_date = models.DateField(auto_now=False)
    emitter = HStoreField()
    
    # Add timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)