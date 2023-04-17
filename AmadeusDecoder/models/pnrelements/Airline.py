'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class Airline(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_airlines'
    
    name = models.CharField(max_length=200, null=False)
    alias = models.CharField(max_length=200, null=True)
    iata = models.CharField(max_length=200, null=True)
    icao = models.CharField(max_length=200, null=True)
    callsign = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    # airline_country = relationship(Country, lazy='select', primaryjoin=country == Country.name, foreign_keys=country)
    active = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.iata