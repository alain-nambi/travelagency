'''
Created on 10 Sep 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class TicketPassengerSegment(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta():
        db_table = 't_ticket_passenger_segment'
    
    ticket = models.ForeignKey(
        "AmadeusDecoder.Ticket",
        on_delete=models.CASCADE,
        related_name='ticket_parts'
    )
      
    segment = models.ForeignKey(
        "AmadeusDecoder.PnrAirSegments",
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    
    fare = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    tax = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    total = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    
    def __str__(self):
        return 'Ticket'

class OtherFeeSegment(BaseModel, models.Model):
    
    class Meta():
        db_table = 't_other_fees_segment'
    
    passenger = models.ForeignKey(
        "AmadeusDecoder.Passenger",
        on_delete=models.CASCADE,
        related_name='others_fees'
    )
    
    segment = models.ForeignKey(
        "AmadeusDecoder.PnrAirSegments",
        on_delete=models.CASCADE,
        related_name='related_segments'
    )
    
    other_fee = models.ForeignKey(
        "AmadeusDecoder.OthersFee",
        on_delete=models.CASCADE,
        related_name='related_segments'
    )
    
    def __str__(self):
        return 'Other fees'
    