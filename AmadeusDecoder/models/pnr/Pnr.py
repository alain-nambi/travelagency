'''
Created on 25 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from django.db.models import Q, Min, Max
from AmadeusDecoder.models.BaseModel import BaseModel
from django.contrib.postgres.fields.array import ArrayField
from django.contrib.postgres.fields import HStoreField

class Pnr(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_pnr'
        constraints = [
                models.UniqueConstraint(fields=['number', 'pnr_status'], name='unique_pnr')
            ]
        
    agent = models.ForeignKey(
        'AmadeusDecoder.User',
        on_delete=models.CASCADE,
        related_name='pnrs',
        null=True
    )
    
    agent_code = models.CharField(max_length=100, default='')
    
    agency = models.ForeignKey(
        'AmadeusDecoder.Office',
        db_column='agency_code',
        on_delete=models.CASCADE,
        to_field='code',
        related_name='pnrs',
        null=True
    )
    
    agency_name = models.CharField(max_length=200, default='') # used mainly with EWA PNR
    
    currency = models.ForeignKey(
        "AmadeusDecoder.Currency",
        db_column='currency_code',
        on_delete=models.CASCADE,
        to_field='code',
        related_name='pnrs',
        null=True
    )

    customer = models.ForeignKey(
        "AmadeusDecoder.Client",
        on_delete = models.CASCADE,
        related_name='customer',
        null=True
    )
    
    state = models.IntegerField(default=0) # 0: normal, 1: Missing PNR, 2: Missing Ticket(s), 3: Missing TST(s)
    number = models.CharField(max_length=100, null=False)
    gds_creation_date = models.DateField(null=True)
    system_creation_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, null=False, default='Non émis')
    status_value = models.IntegerField(default=1) # 0, 1
    exportdate = models.DateTimeField(null=True)
    type = models.CharField(max_length=100, default='Inconnu')
    validationstatus = models.IntegerField(default=0)
    dateexport = models.DateTimeField(null=True)
    changedate = models.DateField(null=True)
    lasttransactiondate = models.DateField(null=True)
    otherinformations = ArrayField(
            models.CharField(max_length=200, null=True),
            null=True,
            size=20
        )
    ssr = HStoreField(null=True)
    openingstatus = models.BooleanField(null=False, default=0) # to prevent two different agents from editing the same pnr
    is_splitted = models.BooleanField(default=0)
    is_duplicated = models.BooleanField(default=0)
    is_parent = models.BooleanField(default=0)
    is_child = models.BooleanField(default=0)
    is_read = models.BooleanField(default=0) # False if the pnr has not been opened yet
    is_invoiced = models.BooleanField(default=0)
    parent_pnr = ArrayField(
            models.CharField(max_length=10, null=True),
            null=True,
            size=20
        )
    children_pnr = ArrayField(
            models.CharField(max_length=10, null=True),
            null=True,
            size=20
        )
    is_archived = models.BooleanField(default=0)
    # pnr status
    pnr_status = models.IntegerField(default=1) # pnr status: 1: active, 0: void
    
    # get the minimum deadline date: can be segment or ssr
    def get_min_opc(self):
        from AmadeusDecoder.models.pnrelements.ConfirmationDeadline import ConfirmationDeadline
        confirmation_deadline = ConfirmationDeadline.objects.select_related('segment', 'ssr', 'segment__pnr', 'ssr__pnr').filter(Q(segment__pnr_id=self.id) | Q(ssr__pnr_id=self.id)).filter(type="OPC")
        confirmation_deadline = confirmation_deadline.aggregate(Min('doc_date'))
        return confirmation_deadline['doc_date__min']
    
    # get the maximum issuing date among tickets'
    def get_max_issuing_date(self):
        from AmadeusDecoder.models.invoice.Ticket import Ticket
        ticket = Ticket.objects.filter(pnr__number=self.number).exclude(ticket_status=0)
        ticket = ticket.aggregate(Max('issuing_date'))
        return ticket['issuing_date__max']
    
    # get pnr emit agent
    def get_emit_agent(self):
        from AmadeusDecoder.models.user.Users import User
        try:
            issuing_user = User.objects.filter(copied_documents__document=self.number).order_by('copied_documents__id').last()
            if issuing_user is not None:
                return issuing_user
            elif issuing_user is None and self.agent is not None:
                return self.agent
            else:
                return None
        except Exception as e:
            raise e
            print(e)
            
    # get pnr creator agent
    def get_creator_agent(self):
        from AmadeusDecoder.models.user.Users import User
        try:
            issuing_user = User.objects.filter(copied_documents__document=self.number).order_by('id').first()
            if self.agent is not None:
                return self.agent
            elif issuing_user is not None:
                return issuing_user
            else:
                return self.agent_code
        except Exception as e:
            raise e
            print(e)
    
    # update is_read status
    def update_read_status(self):
        if not self.is_read:
            self.is_read = True
            self.save()
    
    # update TST missing status
    def update_tst_missing_status(self):
        from AmadeusDecoder.models.invoice.Ticket import Ticket
        if self.status_value == 1:
            temp_tst = Ticket.objects.filter(pnr__id=self.id, ticket_type='TST').first()
            if temp_tst is not None:
                self.state = 0
                self.save()
    
    # get pnr creator from user copying table
    def get_pnr_creator_user_copying(self):
        from AmadeusDecoder.models.user.Users import UserCopying
        first_copier = UserCopying.objects.filter(document=self.number).order_by('id').first()
        if first_copier is not None:
            return first_copier.user_id
        else:
            return None
    
    def __str__(self):
        return str(self.number) + ' {}{}{}'.format('(', 'Zenith' if self.type == 'EWA' else self.type, ')')
        