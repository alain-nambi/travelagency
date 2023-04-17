'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class PassengerAttribute(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_passenger_additional_infos'
    
    passenger = models.ForeignKey(
        "AmadeusDecoder.Passenger",
        on_delete = models.CASCADE,
        related_name='attributes'
    )
    type = models.CharField(max_length=200, null=True)
    value = models.CharField(max_length=200, null=True)
        