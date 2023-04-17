'''
Created on 22 Sep 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class SpecialServiceRequestSegment(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_ssr_segment'
    
    parent_ssr = models.ForeignKey(
        'AmadeusDecoder.SpecialServiceRequestBase',
        on_delete=models.CASCADE,
        related_name='segments'
    )
    
    segment = models.ForeignKey(
        'AmadeusDecoder.PnrAirSegments',
        on_delete=models.CASCADE,
        related_name='ssr_list',
        null = True
    )
    
    # get ssr segment by parent ssr and segment
    def get_ssr_segment_by_parent_segment(self, parent_ssr, segment):
        ssr_segment = SpecialServiceRequestSegment.objects.filter(parent_ssr=parent_ssr, segment=segment)
        return ssr_segment.first()