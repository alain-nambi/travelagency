'''
Created on 19 Sep 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class Remark(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_remark'
        constraints = [
                models.UniqueConstraint(fields=['type', 'code'], name='unique_remark')
            ]
    type = models.CharField(max_length=200)
    code = models.CharField(max_length=10)