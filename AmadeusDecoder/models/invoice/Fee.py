'''
Created on 27 Aug 2022

@author: Famenontsoa, Ra-Sam
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class Fee(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_fee'
    
    pnr = models.ForeignKey(
        "AmadeusDecoder.Pnr",
        on_delete = models.CASCADE,
        related_name='fees'
    )
    ticket = models.ForeignKey(
        "AmadeusDecoder.Ticket",
        on_delete = models.CASCADE,
        related_name='fees',
        null=True
    )
    other_fee = models.ForeignKey(
        "AmadeusDecoder.OthersFee",
        on_delete=models.CASCADE,
        related_name='fees',
        null=True
    )
    type = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200, null=True)
    value = models.DecimalField(max_digits=11, decimal_places=4, null=True)
    cost = models.DecimalField(max_digits=11, decimal_places=4, default=0.0)
    tax = models.DecimalField(max_digits=11, decimal_places=4, default=0.0)
    total = models.DecimalField(max_digits=11, decimal_places=4, default=0.0)
    newest_cost = models.DecimalField(max_digits=11, decimal_places=4, default=0.0)
    old_cost = models.DecimalField(max_digits=11, decimal_places=4, default=0.0)
    is_invoiced = models.BooleanField(default=0)

class OthersFee(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_other_fee'

    pnr = models.ForeignKey(
        "AmadeusDecoder.Pnr",
        on_delete = models.CASCADE,
        related_name='others_fees'
    )

    ticket = models.ForeignKey(
        "AmadeusDecoder.Ticket",
        on_delete=models.CASCADE,
        related_name='others_fees',
        null=True
    )
    
    other_fee = models.ForeignKey(
        "AmadeusDecoder.OthersFee",
        on_delete=models.CASCADE,
        related_name='others_fees',
        null=True
    )
    
    passenger = models.ForeignKey(
        "AmadeusDecoder.Passenger",
        on_delete=models.CASCADE,
        related_name='other_fees',
        null=True
    )

    designation = models.CharField(max_length=100, null=True)
    quantity = models.IntegerField(default=1)
    value = models.DecimalField(max_digits=11, decimal_places=4, null=True)
    cost = models.DecimalField(max_digits=11, decimal_places=4, default=0.0)
    tax = models.DecimalField(max_digits=11, decimal_places=4, default=0.0)
    total = models.DecimalField(max_digits=11, decimal_places=4, default=0.0)
    fee_type = models.CharField(max_length=100, default='Other_fee')
    reference = models.CharField(max_length=100, default=None, null=True)
    passenger_segment = models.CharField(max_length=100, default=None, null=True)
    creation_date = models.DateField(null=True)
    is_subjected_to_fee = models.BooleanField(default='1') # True when the other will have some fees False when not
    is_invoiced = models.BooleanField(default=False)
    product_id = models.IntegerField(default=None, null=True)
    other_fee_status = models.IntegerField(default=1) # 0: void, 1: open for use, 3: flown
    
    def __str__(self):
        return self.designation

class Product(models.Model, BaseModel):

    class Meta:
        db_table = 't_product'

    ticket = models.ForeignKey(
        "AmadeusDecoder.Ticket",
        on_delete = models.CASCADE,
        related_name='products',
        null=True
    )

    designation = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=100, null=True)
    cost = models.DecimalField(max_digits=11, decimal_places=4, default=0.0)
    tax = models.DecimalField(max_digits=11, decimal_places=4, default=0.0)
    total = models.DecimalField(max_digits=11, decimal_places=4, default=0.0)
    type = models.CharField(max_length=100, default=None, null=True)
    product_id = models.IntegerField(null=False)

class ReducePnrFeeRequest(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_reduce_pnr_fee_request'

    pnr = models.ForeignKey(
        "AmadeusDecoder.Pnr",
        on_delete = models.CASCADE,
        related_name='pnr'
    )

    fee = models.ForeignKey(
        "AmadeusDecoder.Fee",
        on_delete = models.CASCADE,
        related_name='reduce_pnr_fee_request'
    )

    user = models.ForeignKey(
        'AmadeusDecoder.User',
        on_delete=models.CASCADE,
        related_name='reduce_pnr_fee_request',
    )
    
    # responder
    user_responder = models.ForeignKey(
        'AmadeusDecoder.User',
        on_delete=models.CASCADE,
        related_name='reduce_pnr_fee_request_responder',
        null=True
    )

    origin_amount = models.DecimalField(max_digits=11, decimal_places=4, default=0.0)
    amount = models.DecimalField(max_digits=11, decimal_places=4, default=0.0)
    system_creation_date = models.DateTimeField()
    status = models.IntegerField(default=0) # 0: non traité, 1: accepté, 2: réfusé, 3: montant modifié
    token = models.CharField(max_length=100)
    motif = models.TextField(max_length=800)
