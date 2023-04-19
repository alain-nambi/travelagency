'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class PnrPassenger(models.Model, BaseModel):
    '''
    classdocs
    '''


    class Meta:
        db_table = 't_pnr_passengers'
        constraints = [
            models.UniqueConstraint(fields=['pnr', 'passenger'], name="unique_pnr_passenger")
        ]
        
    pnr = models.ForeignKey(
        "AmadeusDecoder.Pnr",
        on_delete=models.CASCADE,
        related_name='passengers'
    )
    
    passenger = models.OneToOneField(
        "AmadeusDecoder.Passenger",
        on_delete=models.CASCADE,
        related_name='passenger'
    )
    
    order = models.CharField(max_length=200, null=True) # P1 ou P2 ou .....