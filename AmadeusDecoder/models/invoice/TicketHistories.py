'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class ticketHistories(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_histories'
        
    ticket = models.ForeignKey(
        "AmadeusDecoder.Ticket",
        on_delete=models.CASCADE,
        related_name='histories'
    )
    
    action = models.CharField(max_length=200, null=True)
    actiondate = models.DateTimeField(null=True)
    agentsign = models.CharField(max_length=200, null=True)
    nationalamount = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    nationalcurrency = models.CharField(max_length=200, null=True)
    markuptotal = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    markupvat = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    markupdiscount = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    creditcurrencyrate = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    documentcredittotal = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    
    amount = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    servicefeediscount = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    sftotal = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    sftotalvat = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    sfsubagent = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    sfsubagentret = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    sfsubagentvat = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    sfsubagentvatret = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    sfconsolidator = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    sfconsolidatorvat = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    sfconsolidatorret = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    
    currency = models.CharField(max_length=200, null=True)
    farepaid = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    fareused = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    farerefund = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    netrefund = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    cancellationfee = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    miscallaneousfee = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    taxrefund = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    refundtotal = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    docissuedate = models.DateField(null=True)
    departuredate = models.DateField(null=True)
    comission = models.CharField(max_length=200, null=True)
    sfconsolidatorvatret = models.CharField(max_length=200, null=True)
    creditcurrency = models.CharField(max_length=200, null=True)