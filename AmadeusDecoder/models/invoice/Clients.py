from django.db import models
from django.contrib.postgres.fields import HStoreField
from AmadeusDecoder.models.BaseModel import BaseModel

class Client(models.Model, BaseModel):

    class Meta:
        db_table = 't_client'

    last_name = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    address_1 = models.CharField(max_length=200)
    address_2 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    customer_type = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    order_type = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=200, default='Simple', null=False)
    intitule = models.CharField(max_length=200, default=None, null=True)
    classment = models.CharField(max_length=200, default=None, null=True)
    contact = models.CharField(max_length=200, default=None, null=True)
    complement = models.CharField(max_length=200, default=None,  null=True)
    code_postal = models.CharField(max_length=200, default=None, null=False)
    telephone = models.CharField(max_length=200, default=None)
    email = models.CharField(max_length=200, default=None, null=False)
    site = models.CharField(max_length=200, default=None, null=True)
    ct_num = models.CharField(max_length=200, default=None, null=True)
    ct_type = models.IntegerField(default=None, null=True)
    departement = models.CharField(max_length=100, default=None, null=True)
    chart_of_accounts = models.CharField(max_length=50, default=None, null=True)
    date_creation = models.DateTimeField(auto_now=True, null=True)
    creator = models.ForeignKey('AmadeusDecoder.User', on_delete=models.CASCADE, null=True, default=None)
    odoo_id = models.IntegerField(default=None, null=True)

    def __str__(self):
        display = ''
        if self.intitule is not None:
            if self.ct_num is not None:
                display = self.intitule + ' (' + self.ct_num + ')'
            else:
                display = self.intitule
        else:
            if self.ct_num is not None:
                display = self.last_name + ' ' + self.first_name + ' (' + self.ct_num + ')'
            else:
                display = self.last_name + ' ' + self.first_name
        return display


class ClientAddress(models.Model, BaseModel):

    class Meta:
        db_table = 't_client_address'

    value = HStoreField(null=False, default=dict)
    client = models.ForeignKey(
        "AmadeusDecoder.Client",
        on_delete=models.CASCADE,
        related_name='details'
    )
