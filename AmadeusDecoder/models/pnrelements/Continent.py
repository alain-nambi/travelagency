'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class Continent(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_continents'
    
    name = models.CharField(max_length=200, null=False)
    code = models.CharField(max_length=20, null=False)