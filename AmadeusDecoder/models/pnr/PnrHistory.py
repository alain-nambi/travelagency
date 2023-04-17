'''
Created on 16 Oct 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel
from django.contrib.postgres.fields.array import ArrayField
from django.contrib.postgres.fields import HStoreField

class PnrHistory(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_pnr_history'
    
    pnr = models.ForeignKey(
        'AmadeusDecoder.Pnr',
        on_delete=models.SET_NULL,
        related_name='histories',
        null=True
    )
    
    agent = models.ForeignKey(
        'AmadeusDecoder.User',
        on_delete=models.SET_NULL,
        related_name='history_pnrs',
        null=True
    )
    
    agent_code = models.CharField(max_length=100, default='')
    
    agent_username = models.CharField(max_length=100, null=True)
    
    agency = models.ForeignKey(
        'AmadeusDecoder.Office',
        db_column='agency_code',
        on_delete=models.SET_NULL,
        to_field='code',
        related_name='history_pnrs',
        null=True
    )
    
    agency_code_name = models.CharField(max_length=100, null=True)
    
    currency = models.ForeignKey(
        "AmadeusDecoder.Currency",
        db_column='currency_code',
        on_delete=models.SET_NULL,
        to_field='code',
        related_name='history_pnrs',
        null=True
    )
    
    currency_code_name = models.CharField(max_length=100, null=True)
    
    state = models.IntegerField(default=0) # 0, 1, 2, 3
    number = models.CharField(max_length=100, null=False)
    gds_creation_date = models.DateField(null=True)
    system_creation_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, null=False, default='Non émis')
    status_value = models.IntegerField(default=0) # 0, 1
    exportdate = models.DateTimeField(null=True)
    type = models.CharField(max_length=100, default='Inconnu')
    validationstatus = models.IntegerField(default=0)
    dateexport = models.DateTimeField(null=True)
    changedate = models.DateField(null=True)
    lasttransactiondate = models.DateField(null=True)
    otherinformations = ArrayField(
            models.CharField(max_length=200, null=True),
            null=True,
            size=20
        )
    ssr = HStoreField(null=True)
    openingstatus = models.BooleanField(null=False, default=0) # to prevent two different agents from editing the same pnr
    is_splitted = models.BooleanField(default=0)
    is_duplicated = models.BooleanField(default=0)
    is_parent = models.BooleanField(default=0)
    is_child = models.BooleanField(default=0)
    is_read = models.BooleanField(default=0) # False if the pnr has not been opened yet
    parent_pnr = ArrayField(
            models.CharField(max_length=10, null=True),
            null=True,
            size=20
        )
    children_pnr = ArrayField(
            models.CharField(max_length=10, null=True),
            null=True,
            size=20
        )
    
    history_datetime = models.DateTimeField()