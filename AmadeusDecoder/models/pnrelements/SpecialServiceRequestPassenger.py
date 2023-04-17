'''
Created on 19 Sep 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class SpecialServiceRequestPassenger(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_ssr_passenger'
    
    parent_ssr = models.ForeignKey(
        'AmadeusDecoder.SpecialServiceRequestBase',
        on_delete=models.CASCADE,
        related_name='passengers'
    )
    
    passenger = models.ForeignKey(
        'AmadeusDecoder.Passenger',
        on_delete=models.CASCADE,
        related_name='ssr_list',
    )
    
    # get ssr passenger by parent ssr and passenger
    def get_ssr_passenger_by_parent_passenger(self, parent_ssr, passenger):
        ssr_passenger = SpecialServiceRequestPassenger.objects.filter(parent_ssr=parent_ssr, passenger=passenger)
        return ssr_passenger.first()