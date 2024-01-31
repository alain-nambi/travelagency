'''
Created on 25 Aug 2022

@author: Famenontsoa
'''
import os
import datetime
import traceback

from django.db import models
from django.db.models import Q, Min, Max
from AmadeusDecoder.models.BaseModel import BaseModel
from django.contrib.postgres.fields.array import ArrayField
from django.contrib.postgres.fields import HStoreField
from AmadeusDecoder.models.invoice.Fee import OthersFee
from AmadeusDecoder.models.invoice.Ticket import Ticket

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
    
    
    def get_invoices_number(self):
        invoices = PassengerInvoice.objects.filter(pnr_id=self.id).distinct()
        return invoices
    
    # get the minimum deadline date: can be segment or ssr
    def get_min_opc(self):
        from AmadeusDecoder.models.pnrelements.ConfirmationDeadline import ConfirmationDeadline
        confirmation_deadline = ConfirmationDeadline.objects.select_related('segment', 'ssr', 'segment__pnr', 'ssr__pnr').filter(Q(segment__pnr_id=self.id) | Q(ssr__pnr_id=self.id)).filter(type="OPC")
        confirmation_deadline = confirmation_deadline.aggregate(Min('doc_date'))
        return confirmation_deadline['doc_date__min']
    
    # get the maximum issuing date among tickets'
    def get_max_issuing_date(self):
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
                issuing_user = User.objects.filter(
                    (Q(emitted_other_fees__pnr=self) & (Q(emitted_other_fees__other_fee_status=1) | Q(emitted_other_fees__is_invoiced=True)))
                    | (Q(emitted_tickets__pnr=self) & (Q(emitted_tickets__ticket_status=1) | Q(emitted_tickets__is_invoiced=True)))
                ).order_by('id').last()
                if issuing_user is None:
                    issuing_user_other_fee = OthersFee.objects.filter(Q(pnr=self) & (Q(other_fee_status=1) | Q(is_invoiced=True))).exclude(issuing_agent_name=None).last()
                    issuing_user_ticket= Ticket.objects.filter(Q(pnr=self) & (Q(ticket_status=1) | Q(is_invoiced=True))).exclude(issuing_agent_name=None).last()
                    if issuing_user_other_fee is not None:
                        return issuing_user_other_fee.issuing_agent_name
                    elif issuing_user_ticket is not None:
                        return issuing_user_ticket.issuing_agent_name
                    else:
                        return None
                else:
                    return issuing_user
        except Exception as e:
            traceback.print_exc()
            print(e)
            
    # get pnr creator agent
    def get_creator_agent(self):
        from AmadeusDecoder.models.user.Users import User
        try:
            creator = None
            issuing_user = User.objects.filter(copied_documents__document=self.number).order_by('id').first()
            if self.agent is not None:
                creator = self.agent
            elif issuing_user is not None:
                creator = issuing_user
            else:
                creator = self.agent_code
            
            if creator is None or creator == "":
                creator = self.get_emit_agent()
            return creator
        except Exception as e:
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Error with function {}'.format("get_pnr_office"))
                traceback.print_exc(file=error_file)
                error_file.write('\n')
            print(e)
            
    # get PNR issuing / creating office
    def get_pnr_office(self):
        try:
            issuing_office_other_fee = OthersFee.objects.filter(Q(pnr=self) & (Q(other_fee_status=1) | Q(is_invoiced=True))).exclude(issuing_agency_name=None).last()
            issuing_office_ticket= Ticket.objects.filter(Q(pnr=self) & (Q(ticket_status=1) | Q(is_invoiced=True))).exclude(issuing_agency_name=None).last()
            if issuing_office_ticket is not None:
                return issuing_office_ticket.issuing_agency_name
            elif issuing_office_other_fee is not None:
                return issuing_office_other_fee.issuing_agency_name
            else:
                if self.agency is not None:
                    return self.agency.name
                else:
                    return self.agency_name
        except Exception as e:
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Error with function {}'.format("get_pnr_office"))
                traceback.print_exc(file=error_file)
                error_file.write('\n')
            print(e)
    
    # update is_read status
    def update_read_status(self):
        if not self.is_read:
            self.is_read = True
            self.save()
    
    # update TST missing status
    def update_tst_missing_status(self):
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
    
    def update_ticket_status_present_in_passenger_invoice(self):
        from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
        from AmadeusDecoder.models.invoice.Ticket import Ticket
        
        passenger_invoices = PassengerInvoice.objects.filter(pnr_id=self.id).exclude(status='quotation')
    
        if passenger_invoices.exists():
            for passenger_invoice in passenger_invoices:
                if (passenger_invoice.ticket_id is not None and not passenger_invoice.is_invoiced):
                    ticket = Ticket.objects.get(pk=passenger_invoice.ticket_id)
                    ticket.ticket_status = 1
                    ticket.save()
        else:
            print("No passenger invoiced")
            return None

    
    def __str__(self):
        return str(self.number) + ' {}{}{}'.format('(', 'Zenith' if self.type == 'EWA' else self.type, ')')
        