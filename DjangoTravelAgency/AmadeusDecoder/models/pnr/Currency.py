'''
Created on 26 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel
from django.utils import timezone

class Currency(models.Model, BaseModel):
    class Meta:
        db_table = 't_currency'
        constraints = [
            models.UniqueConstraint(fields=['code'], name="unique_currency_code"),
            models.UniqueConstraint(fields=['name'], name="unique_currency_name")
        ]
    
    name = models.CharField(max_length=200, null=False)
    code = models.CharField(max_length=5, null=False)

class CurrencyRate(models.Model, BaseModel):
    '''
    classdocs
    '''
    class Meta:
        db_table = 't_currency_rate'

    currency = models.OneToOneField(
        'AmadeusDecoder.Currency',
        on_delete=models.CASCADE
    )
    value = models.DecimalField(decimal_places=4, max_digits=10, default=0.0)
    lastupdate = models.DateTimeField(default=timezone.now)