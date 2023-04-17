'''
Created on 26 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class Contact(models.Model, BaseModel):
    '''
    classdocs
    '''
    class Meta:
        db_table = 't_pnr_contact'
        
    pnr = models.ForeignKey(
        'AmadeusDecoder.Pnr',
        on_delete=models.CASCADE,
        related_name='contacts',
        null=False
    )
    contacttype = models.CharField(max_length=100, null=True)
    value = models.CharField(max_length=200, null=True)
    owner = models.CharField(max_length=200, null=True)
    
    # get contact
    def get_contact(self):
        contact = Contact.objects.filter(pnr=self.pnr, contacttype=self.contacttype, value=self.value, owner=self.owner)
        return contact.first()
    
    def __str__(self):
        return '{}: {}'.format(self.contacttype, self.value)
        