'''
Created on 15 Sep 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class SpecialServiceRequestDescription(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_ssr_description'
        
    ssr = models.ForeignKey(
        'AmadeusDecoder.SpecialServiceRequest',
        on_delete=models.CASCADE,
        related_name='description'
    )
    lang = models.CharField(max_length=10) # en, fr, ....
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.description