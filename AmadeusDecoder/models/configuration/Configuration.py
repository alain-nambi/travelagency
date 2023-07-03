'''
Created on Jul 3, 2023

@author: Famenontsoa
'''
from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField

from AmadeusDecoder.models.BaseModel import BaseModel

class Configuration(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_configuration'
        constraints = [
            models.UniqueConstraint(fields=['environment', 'name', 'value_name'], name="unique_configuration")
        ]
        
    environment = models.CharField(max_length=10, default='all')
    name = models.CharField(max_length=255)
    to_be_applied_on = models.CharField(max_length=255)
    value_name = models.CharField(max_length=255)
    single_value = models.TextField(null=True)
    array_value = ArrayField(
            models.CharField(max_length=255, null=True),
            null=True
        )
    array_of_array_value = ArrayField(
            ArrayField(
                models.CharField(max_length=255, null=True),
                null=True,
            ),
            null=True
        )
    dict_value = HStoreField(null=True)
    created_on = models.DateTimeField()
    last_update = models.DateTimeField()
    is_active = models.BooleanField(default=True)