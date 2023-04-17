'''
Created on 29 Dec 2022

@author: Mihaja
'''
from django.db import models
from django.db.models import Q
from AmadeusDecoder.models.BaseModel import BaseModel

class Tjq(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_tjq'

    agent = models.ForeignKey(
        'AmadeusDecoder.User',
        on_delete=models.CASCADE,
        null=True
    )

    agency = models.ForeignKey(
        'AmadeusDecoder.Office',
        db_column='agency_code',
        on_delete=models.CASCADE,
        to_field='code',
        null=True
    )
    
    agency_name = models.CharField(max_length=200, default='')
    tjq_agent_type = models.CharField(max_length=200) 
    doc_date = models.CharField(max_length=200) 
    currency = models.CharField(max_length=200)
    seq_no = models.CharField(max_length=200)
    ticket_number = models.CharField(max_length=200)
    pnr_number = models.CharField(max_length=200)
    tax = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    fee = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    comm = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    fp_pax = models.CharField(max_length=200)
    passenger = models.CharField(max_length=200)
    agent_code = models.CharField(max_length=100, default='')
    type = models.CharField(max_length=100, default='')
    system_creation_date = models.DateTimeField(null=True)
    
    
        