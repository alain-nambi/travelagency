'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class Airport(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_airports'
        constraints = [
                models.UniqueConstraint(fields=['iata_code'], name='unique_airport_iata_code')
            ]
    ident = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=False)
    elevation_ft = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    continent = models.CharField(max_length=200, null=True)
    # airport_continent = relationship(Continent,lazy='subquery', primaryjoin = continent == Continent.code, foreign_keys=continent)
    iso_country = models.CharField(max_length=200, null=True)
    # airport_country = relationship(Country,lazy='subquery', primaryjoin=iso_country == Country.code, foreign_keys=iso_country)
    iso_region = models.CharField(max_length=200, null=True)
    municipality =models.CharField(max_length=200, null=True)
    gps_code = models.CharField(max_length=200, null=True)
    iata_code = models.CharField(max_length=200, null=True)
    local_code = models.CharField(max_length=200, null=True)
    coordinates = models.CharField(max_length=200, null=True)