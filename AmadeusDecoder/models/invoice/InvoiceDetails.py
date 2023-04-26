'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class InvoiceDetails(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_invoice_detail'
    
    invoice = models.OneToOneField(
        'AmadeusDecoder.Invoice',
        on_delete=models.CASCADE,
        related_name='detail'
    )
    totalht = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    tva_sce = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    total_tax = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    total = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    total_fees = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    duedate = models.DateField(null=True)
    
    # get invoice detail by pnr
    def get_invoice_detail_by_pnr(self, pnr):
        return InvoiceDetails.objects.filter(invoice__pnr = pnr).first()