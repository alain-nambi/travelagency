'''
Created on 22 Sep 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class TicketSSR(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_ticket_ssr'
    
    ticket = models.ForeignKey(
        'AmadeusDecoder.Ticket',
        on_delete=models.CASCADE,
        related_name='ticket_ssrs'
    )
    
    ssr = models.ForeignKey(
        'AmadeusDecoder.SpecialServiceRequestBase',
        on_delete=models.CASCADE,
        related_name='tickets'
    )