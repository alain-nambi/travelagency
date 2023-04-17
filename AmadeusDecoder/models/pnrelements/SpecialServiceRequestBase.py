'''
Created on 22 Sep 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class SpecialServiceRequestBase(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_ssr_base'
    
    ssr = models.ForeignKey(
        'AmadeusDecoder.SpecialServiceRequest',
        on_delete=models.CASCADE,
        related_name='related_ssr'
    )
    
    pnr = models.ForeignKey(
        'AmadeusDecoder.Pnr',
        on_delete=models.CASCADE,
        related_name = 'ssr_list'
    )
    
    ssr_text = models.CharField(max_length=200, default='')
    order_line = models.CharField(max_length=10, default='') # started with E e.g: E8
    
    # get ssr base by ssr_text, ssr, pnr
    def get_ssr_base_by_text_ssr_pnr(self, pnr):
        ssr_base = SpecialServiceRequestBase.objects.filter(ssr=self.ssr, pnr__id=pnr.id, ssr_text=self.ssr_text)
        return ssr_base.first()