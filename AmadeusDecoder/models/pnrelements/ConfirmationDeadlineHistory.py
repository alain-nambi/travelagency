'''
Created on 27 Oct 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class ConfirmationDeadlineHistory(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_confirmation_deadline_history'
        
    segment = models.ForeignKey(
        'AmadeusDecoder.PnrAirSegments',
        on_delete=models.SET_NULL,
        related_name='confirmation_deadline_histories',
        null=True
    )
    
    ssr = models.ForeignKey(
        'AmadeusDecoder.SpecialServiceRequestBase',
        on_delete=models.SET_NULL,
        related_name='confirmation_deadline_histories',
        null=True
    )
    
    pnr_number = models.CharField(max_length=6, null=True)
    
    type = models.CharField(max_length=200, null=True) # OPW or OPC
    free_flow_text = models.CharField(max_length=200, null=True)
    doc_date = models.DateTimeField(null=True) # the displayed date: Deadline or Creation
    history_datetime = models.DateTimeField(null=True)