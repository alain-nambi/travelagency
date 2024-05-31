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
    # is_canceled = models.BooleanField(default=0)
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
            
    def update_agency_name(self, agency_name):
        # Mise à jour du nom de l'agence pour les émissions de Zenith uniquement
        try:
            pnr = Pnr.objects.get(pk=self.id, type='EWA')
            pnr.agency_name = agency_name
            pnr.save()
        except Pnr.DoesNotExist:
            pass
            # Gérer le cas où aucun PNR de type 'EWA' n'est trouvé
            print("Aucun PNR de type 'EWA' n'a été trouvé pour cette instance.")
        
    def get_agency_name(self, issuing_office):
        if issuing_office is not None:
            # print(f"** {issuing_office} **")
            agency_name = issuing_office.issuing_agency_name
            # print(agency_name)
            
            if agency_name:
                self.update_agency_name(agency_name)
                return agency_name
        return None
            
    # get PNR issuing / creating office
    def get_pnr_office(self):
        try:
            issuing_office_other_fee =  OthersFee.objects.filter(
                                            Q(pnr=self) & (Q(other_fee_status=1) | Q(is_invoiced=True))
                                        ).exclude(issuing_agency_name=None).exclude(issuing_agency_name__icontains='web').last()
            
            issuing_office_ticket = Ticket.objects.filter(
                                        Q(pnr=self) & (Q(ticket_status=1) | Q(is_invoiced=True))
                                    ).exclude(issuing_agency_name=None).exclude(issuing_agency_name__icontains='web').last()

            agency_name = self.get_agency_name(issuing_office_ticket)
            if agency_name:
                return agency_name

            agency_name = self.get_agency_name(issuing_office_other_fee)
            if agency_name:
                return agency_name

            return self.agency.name if self.agency else self.agency_name
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
        
    def attach_ticket_to_first_passenger_segment(self):
        """
        Function: attach_ticket_to_first_passenger_segment
        Description: This function is responsible for attaching tickets to the first passenger and available segments.
                    It is applicable only for Passenger Name Records (PNRs) with a single passenger.
        Parameters: self (instance): Instance of the class containing the function
        Returns: None
        """
        
        # Import necessary models
        from AmadeusDecoder.models.pnr.PnrPassenger import PnrPassenger
        from AmadeusDecoder.models.pnrelements.PnrAirSegments import PnrAirSegments
        from AmadeusDecoder.models.invoice.Ticket import Ticket
        from AmadeusDecoder.models.invoice.TicketPassengerSegment import TicketPassengerSegment
        
        passenger_instance = PnrPassenger.objects.filter(pnr_id=self.id).all()
        ticket_obj = Ticket.objects.filter(pnr_id=self.id, passenger=None).all()
        pnr_segment_obj = PnrAirSegments.objects.filter(pnr_id=self.id).first()
        
        # Check if PNR has only one passenger relation
        if passenger_instance.exists() and len(passenger_instance) == 1:
            print("==> One passenger <==")      
            if ticket_obj.exists():
                # Get all ticket ids by only set id as required column
                ticket_ids = list(ticket_obj.values_list('id', flat=True))
                
                # Fetch existing TicketPassengerSegment objects for these tickets
                ticket_segment_obj = TicketPassengerSegment.objects.filter(ticket_id__in=ticket_ids)
                
                # Iterate through each ticket
                for ticket_id in ticket_ids:
                    if pnr_segment_obj:
                        existing_ticket_segment = ticket_segment_obj.filter(segment=pnr_segment_obj, ticket_id=ticket_id).exists()
                        if not existing_ticket_segment:
                            # If TicketPassengerSegment does not exist, create a new one
                            ticket_segment = TicketPassengerSegment(
                                segment=pnr_segment_obj,
                                ticket_id=ticket_id,
                                fare=0,
                                tax=0,
                                total=0
                            )
                            ticket_segment.save()
                    
                # Update the passenger attribute for all tickets
                for ticket in ticket_obj:
                    ticket.passenger = passenger_instance.first().passenger
                    ticket.save()
                    
    def rectify_fare_cost(self):
        """
        Function: rectify_fare_cost
        Description: This function is responsible for updating the fare cost of a ticket or other fees to ensure they are correct.
        """
        # Retrieve tickets related to the PNR
        tickets = Ticket.objects.filter(pnr_id=self.id, ticket_status=1)

        # Iterate over each ticket to check and adjust costs if necessary
        for ticket in tickets:
            # Calculate the sum of transport cost and tax
            transport_and_tax_sum = ticket.transport_cost + ticket.tax
            
            # Check if the sum equals the total cost of the ticket
            if transport_and_tax_sum == ticket.total:
                print(f"<Ticket cost correct {ticket.number}> HT {ticket.transport_cost} TAX: {ticket.tax} TOTAL: {ticket.total}")
                continue
            
            # Check if total cost is greater than 0 and transport cost + tax not equal to total
            if ticket.total > 0 and transport_and_tax_sum != ticket.total:
                # Calculate the corrected transport cost
                corrected_transport_cost = min(ticket.total - ticket.tax, ticket.total)

                # If the corrected transport cost is negative, set it to 0
                corrected_transport_cost = max(corrected_transport_cost, 0)

                # Adjust the transport cost and tax accordingly
                ticket.transport_cost = corrected_transport_cost
                ticket.tax = ticket.total - corrected_transport_cost
                
                # Display a banner indicating the start of fare cost rectification
                print(f"<Ticket cost rectification {ticket.number} {ticket.pnr}> HT {ticket.transport_cost} TAX: {ticket.tax} TOTAL: {ticket.total}")

                # Save the modifications made to the ticket
                ticket.save()
                    
        # # Display the tickets and other fees after rectification
        # print(tickets)
        # print(other_fees)

    
    def __str__(self):
        return str(self.number) + ' {}{}{}'.format('(', 'Zenith' if self.type == 'EWA' else self.type, ')')
        
class UnremountedPnr(models.Model):
    class Meta:
        db_table = 't_unremouted_pnr'
        
    number = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=20, null=False)
    emitter = models.ForeignKey(
        'AmadeusDecoder.User',
        on_delete=models.CASCADE,
    )

    creation_date = models.DateTimeField(auto_now=True)
    state = models.IntegerField(default=0) # 0 en attente - 1 validé - 2 annulé - 3 supprimé


class unRemountedPnrPassenger(models.Model):
    class Meta:
        db_table = 't_unremounted_pnr_passenger'

    unremountedPnr = models.ForeignKey(
        'AmadeusDecoder.UnremountedPnr',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100, null=True)
    surname = models.CharField(max_length=100, null=True)
    designation = models.CharField(max_length=100, null=True)
    type = models.ForeignKey(
        'AmadeusDecoder.PassengerType',
        on_delete=models.CASCADE,
    )
    passeport = models.CharField(max_length=100, null=True)
    order = models.CharField(max_length=100, null=False)

class unRemountedPnrSegment(models.Model):
    class Meta:
        db_table = 't_unremounted_pnr_segment'

    unremountedPnr = models.ForeignKey(
        'AmadeusDecoder.UnremountedPnr',
        on_delete=models.CASCADE,
    )
    order = models.CharField(max_length=10, null=True)
    flightno = models.CharField(max_length=50, null=True)
    servicecarrier = models.ForeignKey(
        "AmadeusDecoder.Airline",
        on_delete=models.CASCADE,
        related_name="segment_airline"
    )
    departuretime = models.DateTimeField(null=True)
    arrivaltime = models.DateTimeField(null=True)
    codeorg = models.ForeignKey(
        "AmadeusDecoder.Airport",
        on_delete=models.CASCADE,
        related_name="origin_code"
    )
    codedest = models.ForeignKey(
        "AmadeusDecoder.Airport",
        on_delete=models.CASCADE,
        related_name="destination_code"
    )

class unRemountedPnrTickets(models.Model):
    class Meta:
        db_table = 't_unremounted_pnr_ticket'

    unremountedPnr = models.ForeignKey(
        'AmadeusDecoder.UnremountedPnr',
        on_delete=models.CASCADE,
    )
    number = models.CharField(max_length=50, null=True)
    type = models.CharField(max_length=50, null=True)
    transport_cost = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    tax = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    fee = models.BooleanField(default=True)
    ticket_type = models.IntegerField(default=0) # 0 ticket , 1 other fee

    passenger = models.ForeignKey(
        'AmadeusDecoder.unRemountedPnrPassenger',
        on_delete=models.CASCADE,
    )

class unRemountedPnrTicketSegment(models.Model):
    class Meta:
        db_table = 't_unremounted_pnt_ticket_segment'

    ticket = models.ForeignKey(
        'AmadeusDecoder.unRemountedPnrTickets',
        on_delete=models.CASCADE,
    )

    segment = models.ForeignKey(
        'AmadeusDecoder.unRemountedPnrSegment',
        on_delete=models.CASCADE,
    )