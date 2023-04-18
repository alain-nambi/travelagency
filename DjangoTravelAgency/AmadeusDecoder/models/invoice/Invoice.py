'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class Invoice(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_invoice'
    
    pnr = models.OneToOneField(
        'AmadeusDecoder.Pnr',
        on_delete=models.CASCADE,
        related_name='invoice'
    )
    client = models.ForeignKey(
        "AmadeusDecoder.Client",
        on_delete = models.CASCADE,
        related_name='invoices',
        null=True
    )
    transmitter = models.CharField(max_length=200, null=True)
    follower = models.ForeignKey(
        'AmadeusDecoder.User',
        on_delete = models.CASCADE,
        related_name='invoices',
        null=True
    )
    reference = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=200, null=True)
    transmission_date = models.DateField(null=True)
        
        