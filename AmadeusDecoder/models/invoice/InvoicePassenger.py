from django.db import models


from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.Fee import Fee, OthersFee
from AmadeusDecoder.models.invoice.Clients import Client
from AmadeusDecoder.models.user.Users import User

class PassengerInvoice(models.Model):

    class Meta:
        db_table = 't_passenger_invoice'

    pnr = models.ForeignKey('Pnr', on_delete=models.CASCADE, related_name='passenger_invoice')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=True)
    user_follower = models.ForeignKey('User', on_delete=models.CASCADE)
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, default=False, null=True)
    fee = models.ForeignKey('Fee', on_delete=models.CASCADE, default=False, null=True)
    other_fee = models.ForeignKey('OthersFee', on_delete=models.CASCADE, default=None, null=True)

    reference = models.CharField(max_length=100)
    is_invoiced = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=True)
    is_quotation = models.BooleanField(default=False)
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=100, null=True)
    invoice_id = models.ForeignKey('AmadeusDecoder.Invoice', on_delete=models.CASCADE, default=None, null=True)
    date_creation = models.DateTimeField(auto_now=True)
    control = models.IntegerField(default=0) # 0: not controlled, 1: controlled
    invoice_number = models.CharField(max_length=100, null=True, default=None)
    is_archived = models.BooleanField(default=False)