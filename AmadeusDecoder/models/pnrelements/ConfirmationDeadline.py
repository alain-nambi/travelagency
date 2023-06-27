'''
Created on 22 Sep 2022

@author: Famenontsoa
'''
from django.db import models
from django.db.models import Q
from AmadeusDecoder.models.BaseModel import BaseModel

class ConfirmationDeadline(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_confirmation_deadline'
        
    segment = models.ForeignKey(
        'AmadeusDecoder.PnrAirSegments',
        on_delete=models.CASCADE,
        related_name='confirmation_deadline',
        null=True
    )
    
    ssr = models.ForeignKey(
        'AmadeusDecoder.SpecialServiceRequestBase',
        on_delete=models.CASCADE,
        related_name='confirmation_deadline',
        null=True
    )
    
    type = models.CharField(max_length=200) # OPW or OPC
    free_flow_text = models.CharField(max_length=200)
    doc_date = models.DateTimeField() # the displayed date: Deadline or Creation
    
    # get the confirmation deadline
    def get_confirmation_deadline(self):
        if hasattr(self, 'segment'):
            try:
                return ConfirmationDeadline.objects.filter(segment__id=self.segment.id, type='OPC').first()
            except:
                pass
        elif hasattr(self, 'ssr'):
            return ConfirmationDeadline.objects.filter(ssr__id=self.ssr.id, type='OPC').first()
        else:
            return None    
    
    # get the confirmation deadline of ssrs in modal
    def get_confirmation_deadline_ssr_modal(self):
        try:
            return ConfirmationDeadline.objects.filter(ssr__id=self.ssr.id, type='OPC').first()
        except:
            return None
    
    # get confirmation deadline by segment, ssr and type
    def get_confirmation_deadline_by_segment_ssr_type(self):
        confirmation_deadline = ConfirmationDeadline.objects.filter(segment=self.segment, ssr=self.ssr, type=self.type)
        return confirmation_deadline.first()
    
    # delete confirmation deadline
    def delete_confirmation_deadline(self, pnr, confirmation_deadlines):
        all_confirmation_deadlines = ConfirmationDeadline.objects.filter(Q(segment__pnr_id=pnr.id) | Q(ssr__pnr_id=pnr.id)).all()
        for temp in all_confirmation_deadlines:
            if temp not in confirmation_deadlines:
                temp.delete()
        
    def __str__(self):
        return str(self.doc_date)
        