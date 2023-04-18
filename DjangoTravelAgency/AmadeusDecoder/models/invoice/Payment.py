'''
Created on 29 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel
from django.utils import timezone

class Payment(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_payment'
    
    ticket = models.ForeignKey(
        'AmadeusDecoder.Ticket',
        on_delete=models.CASCADE,
        related_name='ticket'
    )
    type = models.CharField(max_length=200, null=False)
    amount = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    date = models.DateField(default=timezone.now)
    state = models.CharField(max_length=200, null=True)