'''
Created on 25 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class Flight(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_pnr_flight'
        # This table actually not user !!!!!!!!!!!!!!!!!!!!!!!!

    pnr = models.ForeignKey(
        'AmadeusDecoder.Pnr',
        on_delete=models.CASCADE
    )
    airlinecode = models.CharField(max_length=100, null=True)
    flightnumber = models.CharField(max_length=100, default='Inconnu')
    departureairportcode = models.CharField(max_length=100, null=True)
    landingairportcode = models.CharField(max_length=100, null=True)
    departuretime = models.DateTimeField(null=True)
    landingtime = models.DateTimeField(null=True)
        