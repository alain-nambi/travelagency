'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class Tax(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_taxes'
    
    ticket = models.ForeignKey(
        "AmadeusDecoder.Ticket",
        on_delete=models.CASCADE,
        related_name='taxes'
    )
    amount = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    taxcode = models.CharField(max_length=200, null=True)
    naturecode = models.CharField(max_length=200, null=True)
        