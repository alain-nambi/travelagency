'''
Created on 1 Jun 2023

@author: Famenontsoa
'''

from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class CustomerAddress(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_customer_address'
        
    pnr = models.ForeignKey(
        "AmadeusDecoder.Pnr",
        on_delete=models.CASCADE,
        related_name='customerAddresses'
    )
    
    passenger = models.ForeignKey(
        "AmadeusDecoder.Passenger",
        on_delete=models.CASCADE,
        related_name='address',
        null=True
    )
    
    address = models.CharField(max_length=255)
    
    # get customer's address
    def get_customer_address(self):
        return CustomerAddress.objects.filter(pnr=self.pnr, passenger=self.passenger, address=self.address).first()
    