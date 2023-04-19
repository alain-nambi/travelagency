'''
Created on 19 Sep 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class PnrRemark(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_pnr_remark'
        
    pnr = models.ForeignKey(
        'AmadeusDecoder.Pnr',
        on_delete=models.CASCADE,
        related_name='remarks'
    )
    
    remark = models.ForeignKey(
        'AmadeusDecoder.Remark',
        on_delete=models.CASCADE,
        related_name='remarks'
    )
    
    remark_text = models.CharField(max_length=200)
    
    # get pnr remark by pnr, remark, remark_text
    def get_pnr_remark(self):
        remark = PnrRemark.objects.filter(pnr=self.pnr, remark=self.remark, remark_text=self.remark_text)
        return remark.first()
    
    # get remarks by pnr
    def get_all_pnr_remark(self, pnr):
        remarks = PnrRemark.objects.filter(pnr=pnr).all()
        return remarks
        