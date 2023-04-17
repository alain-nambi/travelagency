'''
Created on 17 Jan 2023

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel
from datetime import datetime
import pytz

class RawData(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_raw_data'
    
    pnr = models.ForeignKey(
        "AmadeusDecoder.Pnr",
        on_delete=models.CASCADE,
        related_name='pnr_data'
    )
    
    ticket = models.ForeignKey(
        "AmadeusDecoder.Ticket",
        on_delete=models.CASCADE,
        related_name='ticket_data',
        null=True
    )
    
    data_text = models.TextField(default='')
    data_datetime = models.DateTimeField(null=True)
    
    # save raw data
    def save_raw_data(self, contents, pnr, ticket):
        raw_data_obj = RawData()
        all_raw_text = ''
        for content in contents:
            all_raw_text += content + '\n'
        
        raw_data_obj.data_text = all_raw_text
        raw_data_obj.pnr = pnr
        raw_data_obj.ticket = ticket
        current_datetime = datetime.now()
        raw_data_obj.data_datetime = datetime(current_datetime.year, current_datetime.month, current_datetime.day, current_datetime.hour, current_datetime.minute, current_datetime.second, current_datetime.microsecond, pytz.UTC)
        raw_data_obj.save()
        
    