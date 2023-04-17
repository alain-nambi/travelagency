'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class AirSegment(models.Model, BaseModel):
    '''
    classdocs
    '''


    class Meta:
        db_table = 't_airsegments'
    
    ticket = models.ForeignKey(
        "AmadeusDecoder.Ticket",
        on_delete=models.CASCADE
    )
    servicecarrier = models.CharField(max_length=200, null=True)
    flightno = models.CharField(max_length=50, null=True)
    bkgclass = models.CharField(max_length=100, null=True)
    departuretime = models.DateTimeField(null=True)
    arrivaltime = models.DateTimeField(null=True)
    codeorg = models.CharField(max_length=50, null=True)
    amanameorg = models.CharField(max_length=200, null=True)
    countryorg = models.CharField(max_length=200, null=True)
    codedest = models.CharField(max_length=50, null=True)
    amanamedest = models.CharField(max_length=200, null=True)
    countrydest = models.CharField(max_length=200, null=True)
    baggageallow = models.CharField(max_length=200, null=True)
    terminalchecking = models.CharField(max_length=50, null=True)
    terminalarrival = models.CharField(max_length=50, null=True)
    acrecloc = models.CharField(max_length=200, null=True)