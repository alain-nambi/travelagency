'''
Created on 15 Sep 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class SpecialServiceRequest(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_ssr'
        constraints = [
                models.UniqueConstraint(fields=['code'], name='unique_ssr')
            ]
        
    code = models.CharField(max_length=50)
    freeflowtext = models.BooleanField(default=False) # *
    suppliedbyairline = models.BooleanField(default=False) # /
    
    def __str__(self):
        return self.code
    
    
    
        