'''
Created on 6 Oct 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class TicketPassengerTST(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_ticket_passenger_tst'
        
    ticket = models.ForeignKey(
        "AmadeusDecoder.Ticket",
        on_delete = models.CASCADE,
        related_name='ticket_tst_parts'
    )
    
    passenger = models.ForeignKey(
        "AmadeusDecoder.Passenger",
        on_delete = models.CASCADE,
        related_name='tst_parts'
    )