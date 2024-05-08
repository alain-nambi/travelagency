from django.db import models
from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.Fee import Fee, OthersFee
from AmadeusDecoder.models.invoice.Clients import Client
from AmadeusDecoder.models.user.Users import User

class CancelSaleOrder(models.Model):
    class Meta:
        db_table = 't_cancel_sale_order'
    
    pnr = models.ForeignKey(Pnr, on_delete=models.CASCADE, related_name='cancel_sale_orders')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    agent = models.CharField(max_length=255, null=False)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, null=True)
    fee = models.OneToOneField(Fee, on_delete=models.CASCADE, null=True)
    other_fee = models.OneToOneField(OthersFee, on_delete=models.CASCADE, null=True)
    invoice_number = models.CharField(max_length=20, null=False)
    created_at = models.DateTimeField(auto_now=True)