'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
import datetime
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel
from django.utils import timezone

class Invoice(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_invoice'
    
    pnr = models.OneToOneField(
        'AmadeusDecoder.Pnr',
        on_delete=models.CASCADE,
        related_name='invoice'
    )
    client = models.ForeignKey(
        "AmadeusDecoder.Client",
        on_delete = models.CASCADE,
        related_name='invoices',
        null=True
    )
    transmitter = models.CharField(max_length=200, null=True)
    follower = models.ForeignKey(
        'AmadeusDecoder.User',
        on_delete = models.CASCADE,
        related_name='invoices',
        null=True
    )
    reference = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=200, null=True)
    transmission_date = models.DateField(null=True)
        
class InvoicesCanceled(models.Model, BaseModel):
    # PNR décommandé 

    class Meta:
        db_table = 't_invoices_canceled'
        
    pnr = models.ForeignKey(
        "AmadeusDecoder.Pnr",
        on_delete = models.CASCADE,
        related_name = 'pnr_unordered',
    )
    
    user = models.ForeignKey(
        'AmadeusDecoder.User',
        on_delete=models.CASCADE,
        related_name = 'user',
    )
    
    invoice_number = models.CharField(max_length=100,null=False )
    motif = models.CharField(max_length=200, null=False)
    invoice_date = models.DateTimeField(auto_now_add=True , null=True)
    date = models.DateTimeField(auto_now_add=True , null=False)
    ticket = models.ForeignKey(
        'Ticket', 
        on_delete=models.CASCADE, 
        default=False, 
        null=True, 
        related_name= 'pnr_unordered_tickets',
        unique=False,
    )
    other_fee = models.ForeignKey(
        'OthersFee',
        on_delete=models.CASCADE, 
        default=None, 
        null=True, 
        related_name='pnr_unordered_other_fees',
    )
    motif_id = models.ForeignKey("AmadeusDecoder.MotifPnr", on_delete = models.CASCADE, related_name='motif_pnr', default=1)

class MotifPnr(models.Model):
    # motif pour décommander un PNR
    class Meta:
        db_table = 't_motif_pnr'

    designation = models.CharField(max_length=200, null=False)
