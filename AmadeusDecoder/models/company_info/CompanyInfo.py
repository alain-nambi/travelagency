'''
Created on 28 Oct 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class CompanyInfo(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_company_info'
        constraints = [
            models.UniqueConstraint(fields=['company_name'], name="unique_company")
        ]
    
    company_name = models.CharField(max_length=200)
    company_currency = models.CharField(max_length=10)
    
    def __str__(self):
        return self.company_name