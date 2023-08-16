'''
Created on 27 Aug 2022

@author: Famenontsoa
'''

import traceback

from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel
from AmadeusDecoder.models.pnrelements.Country import Country
from datetime import datetime
from AmadeusDecoder.models.user.Users import OfficeSubcontractor
from AmadeusDecoder.models.invoice.Fee import OthersFee

_AIRPORT_AGENCY_CODE_ = ['DZAUU000B']
_NOT_FEED_ = ['RESIDUAL VALUE', 'DISCOUNT CARD']

class Ticket(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_ticket'
        constraints = [
            models.UniqueConstraint(fields=['number', 'pnr'], name="unique_ticket")
        ]
        
    pnr = models.ForeignKey(
        "AmadeusDecoder.Pnr",
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    
    passenger = models.ForeignKey(
        "AmadeusDecoder.Passenger",
        on_delete=models.CASCADE,
        related_name='ticket',
        null=True
    )
    
    emitter = models.ForeignKey(
        "AmadeusDecoder.User",
        on_delete=models.CASCADE,
        related_name='emitted_tickets',
        null=True
    )
    
    issuing_agency = models.ForeignKey(
        "AmadeusDecoder.Office",
        on_delete=models.CASCADE,
        related_name='emitted_tickets',
        null=True
    )
    
    issuing_date = models.DateField(null=True)
    number = models.CharField(max_length=200, null=False)
    path = models.CharField(max_length=200, null=True)
    transport_cost = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    tax = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    total = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    exch_val = models.DecimalField(max_digits=11, decimal_places=4, default=0) # Exchange value of the EMD
    rfnd_val = models.DecimalField(max_digits=11, decimal_places=4, default=0) # Refundable value of the EMD
    passengerpath = models.CharField(max_length=200, null=True)
    flightclass = models.CharField(max_length=200, null=True)
    referenceticket = models.CharField(max_length=200, null=True)
    state = models.IntegerField(default=0) # 0: normal, 1: PNR missing, 2: Ticket missing
    status = models.CharField(max_length=200, null=True)
    doccurrency = models.CharField(max_length=200, null=True)
    farecurrency = models.CharField(max_length=200, null=True)
    fare = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    fare_type = models.CharField(max_length=4, default='F') # Fare type: IT, Y, F, ....
    fareequiv = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    farerate = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    commission = models.CharField(max_length=200, null=True)
    origcity = models.CharField(max_length=200, null=True)
    destcity = models.CharField(max_length=200, null=True)
    paxtype = models.CharField(max_length=200, null=True)
    ticket_type = models.CharField(max_length=100, null=True) # Ticket, SSR or TST or Credit note(Avoir); Values: TKT, EMD, TST, CREDIT_NOTE
    payment_option = models.CharField(max_length=100, null=True)
    ticket_status = models.IntegerField(default=1) # 1 Open for use, 0 cancelled/void, 2 Airport control, 3 Flown, 4 refunded, 5 exchanged, 6 printed
    ticket_gp_status = models.CharField(max_length=10, default='OK') # SA, OK, NS....
    is_gp = models.BooleanField(default=0) # true if ticket is GP (no fee)
    ticket_description = models.CharField(max_length=250, null=True) # used mostly on EMD ticket
    passenger_type = models.CharField(max_length=10, default='PAX') # PAX or INF
    is_prime = models.BooleanField(default=0) # true or false => true: prime, false: not prime
    is_regional = models.BooleanField(default=1) # true of false => regional or international/metropole
    is_no_adc = models.BooleanField(default=0) # true or false => true: no additional cost, false: ! no additional cost
    is_subjected_to_fees = models.BooleanField(default=1) # true or false => true: fees will be deducted from cost, false: ticket will have no fees 
    is_invoiced = models.BooleanField(default=0)
    # when the passengers are grouped, we cannot identify the passenger for each ticket.
    # Then the following field was added in order to store the string representation of the related ticket passenger i.e: P1, P2, ...
    # When the passenger list arrives, the system will fetch and update "passenger" automatically
    related_passenger_order = models.CharField(max_length=10, null=True)
    # when the ticket line (FA PAX/INF) in a PNR is mark with DRxx, this current ticket should be a refund
    # its value should be negative
    is_refund = models.BooleanField(default=0)
    is_deposit = models.BooleanField(default=0)
    # when the ticket has been issued outside current travel agency the following filed will be true
    is_issued_outside = models.BooleanField(default=0)
    # for other signification than FA
    is_not_fa_line = models.BooleanField(default=0)
    # this filed has been added to handle ticket modification status
    is_ticket_modification = models.BooleanField(default=0) # true: current ticket is a modification
    # temp ticket status field to store original ticket status
    original_ticket_status = models.IntegerField(default=1) 
    # issuing agency name (original issuing agency name when ID cannot be found)
    issuing_agency_name = models.CharField(max_length=200, null=True)
    # issuing emitter name (when not found from database)
    issuing_agent_name = models.CharField(max_length=200, null=True)
    
    # update ticket status if PNR has been reissued with different tickets
    def update_ticket_status_PNR_reissued(self, pnr, new_ticket_list):
        current_ticket_list = Ticket.objects.filter(pnr=pnr).all()
        common_ticket_index = []
        for i in range(len(current_ticket_list)):
            for j in range(len(new_ticket_list)):
                if current_ticket_list[i].number == new_ticket_list[j].number:
                    common_ticket_index.append(i)
        
        for k in range(len(current_ticket_list)):
            if k not in common_ticket_index:
                current_ticket_list[k].ticket_status = 0
                current_ticket_list[k].state = 0
                current_ticket_list[k].save()
            elif k in common_ticket_index:
                current_ticket_list[k].ticket_status = 1
                current_ticket_list[k].save()
        
        # update pnr state
        self.update_pnr_state(pnr)
    
    # update ticket status if PNR has been reissued with different tickets on Zenith
    def update_ticket_status_PNR_reissued_EWA(self, pnr, new_ticket_list, is_multiple_file):
        current_ticket_list = Ticket.objects.filter(pnr=pnr).all()
        common_ticket_index = []
        for i in range(len(current_ticket_list)):
            for j in range(len(new_ticket_list)):
                if current_ticket_list[i].number == new_ticket_list[j].number:
                    common_ticket_index.append(i)
        
        for k in range(len(current_ticket_list)):
            if k not in common_ticket_index:
                if is_multiple_file:
                    if not current_ticket_list[k].is_invoiced:
                        current_ticket_list[k].ticket_status = 0
                        current_ticket_list[k].save()
                else:
                    if not current_ticket_list[k].is_invoiced:
                        current_ticket_list[k].ticket_status = 0
                        current_ticket_list[k].save()
            elif k in common_ticket_index:
                current_ticket_list[k].ticket_status = 1
                current_ticket_list[k].save()
        
    # update ticket status
    def update_ticket_status_FLOWN(self, pnr):
        from AmadeusDecoder.models.pnrelements.PnrAirSegments import PnrAirSegments
        tickets = Ticket.objects.filter(pnr__id=pnr.id).all()
        for ticket in tickets:
            temp_ticket_segment = PnrAirSegments.objects.filter(tickets__ticket__id=ticket.id).all()
            flown_count = 0
            normal_count = 0
            for segment in temp_ticket_segment:
                if segment.segment_state == 1:
                    flown_count += 1
                elif segment.segment_state == 0:
                    normal_count += 1
            
            if flown_count > 0 and normal_count == 0 and not pnr.is_archived and not ticket.is_deposit and not ticket.is_refund:
                # ticket.ticket_status = 3
                ticket.original_ticket_status = 3
                ticket.state = 0
                ticket.save()
                    
        # update pnr state
        unfilled_ticket = Ticket.objects.filter(pnr__id=pnr.id, state=2).first()
        if unfilled_ticket is None:
            pnr.state = 0
            pnr.save()
    
    # get issuing user !!! important especially when the PNR has been created and issued by different agent !!!
    def get_issuing_user_different_creator(self):
        from AmadeusDecoder.models.user.Users import User
        try:
            issuing_user = User.objects.filter(copied_documents__document=self.pnr.number).order_by('-id').first()
            if issuing_user is not None:
                self.emitter = issuing_user
            elif self.pnr.agent is not None:
                self.emitter = self.pnr.agent
        except Exception as e:
            print(e)
            
    # check and set regional status
    def get_set_regional_status(self):
        import AmadeusDecoder.utilities.configuration_data as configs
        try:
            ticket_destination_countries = []
            temp_company_regional_countries = []
            for country_name in configs.REGIONAL_COUNTRIES:
                temp_country = Country.objects.filter(name=country_name).first()
                if temp_country is not None:
                    temp_company_regional_countries.append(temp_country.code)
            # ticket parts: ticket and segment
            temp_tickets_parts = self.ticket_parts.all()
            for ticket_part in temp_tickets_parts:
                temp_segment = ticket_part.segment
                if temp_segment.codedest is not None:
                    temp_dest_airport = temp_segment.codedest
                    if temp_dest_airport.iso_country is not None:
                        temp_dest_country = Country.objects.filter(code=temp_dest_airport.iso_country).first()
                        if temp_dest_country is not None:
                            ticket_destination_countries.append(temp_dest_country.code)
            # check if international
            for dest_country in ticket_destination_countries:
                if len(temp_company_regional_countries) > 0 and dest_country not in temp_company_regional_countries:
                    self.is_regional = False
                    break
        except:
            traceback.print_exc()
            
    # update ticket status: new ticket line inserted 2 days or more later
    def update_ticket_status_new_line(self, pnr):
        tickets = Ticket.objects.filter(pnr__id=pnr.id).all()
        for ticket in tickets:
            date_difference = pnr.gds_creation_date - ticket.issuing_date
            # to uncomment later
            if date_difference.days > 1:
                ticket.state = 0
                # ticket.ticket_status = 3
                ticket.original_ticket_status = 3
                ticket.save()
            
            first_accepted_date = datetime(2023, 1, 1).date()
            if ticket.issuing_date < first_accepted_date:
                ticket.state = 0
                ticket.ticket_status = 3
                ticket.save()
    
    # update ticket state and status
    def update_ticket_state_status(self, pnr, issuing_date, pnr_creation_date_day):
        if issuing_date is not None:
            issuing_date_day = issuing_date.strftime('%A')
            pnr_creation_date_day = pnr.gds_creation_date.strftime('%A')
            date_difference = pnr.gds_creation_date - issuing_date
            # old process
            if (issuing_date < pnr.gds_creation_date and issuing_date_day != 'Saturday' \
                and issuing_date_day != 'Sunday' and pnr_creation_date_day != 'Monday') or date_difference.days > 2:
                    self.state = 0
                    self.original_ticket_status = 3
                    # self.ticket_status = 3
            
            
            first_accepted_date = datetime(2023, 1, 1).date()
            if issuing_date < first_accepted_date:
                self.state = 0
                self.ticket_status = 3
    
    # udpate ticket status and state after checking their issuing office
    def update_ticket_status_from_office(self, pnr):
        tickets = Ticket.objects.filter(pnr=pnr).all()
        
        for ticket in tickets:
            temp_subcontractor = None
            if ticket.issuing_agency is not None:
                temp_subcontractor = OfficeSubcontractor.objects.filter(code=ticket.issuing_agency.code).first()
                
            if ticket.issuing_agency is None and temp_subcontractor is None:
                ticket.state = 0
                ticket.ticket_status = 3
                ticket.is_issued_outside = True
                ticket.save()
            elif ticket.issuing_agency.company is None and temp_subcontractor is None:
                ticket.state = 0
                ticket.ticket_status = 3
                ticket.is_issued_outside = True
                ticket.save()
        self.update_pnr_state(pnr)
    
    # re-calibrate emd fee
    def recalibrate_fee(self, pnr):
        active_emd = Ticket.objects.filter(pnr=pnr, ticket_type='EMD', ticket_status=1).all()
        for emd in active_emd:
            try:
                is_emitted_in_airport = False
                emd_issuing_date = emd.issuing_date
                emitter = emd.pnr.get_emit_agent()
                # test by agent
                if emitter is not None:
                    try:
                        if emitter.office.code in _AIRPORT_AGENCY_CODE_:
                            is_emitted_in_airport = True
                    except:
                        pass
                # test by current emd issuing agency
                try:
                    if emd.issuing_agency.code in _AIRPORT_AGENCY_CODE_:
                        is_emitted_in_airport = True
                except:
                    pass
                
                if emd.ticket_ssrs.first() is not None:
                    emd_related_segment = emd.ticket_ssrs.first().ssr.segments.first().segment
                    emd_segment_flight_date = emd_related_segment.departuretime.date()
                    if emd_issuing_date == emd_segment_flight_date and is_emitted_in_airport:
                        emd.is_subjected_to_fees = False
                
                if emd.ticket_parts.first() is not None:
                    emd_related_segment = emd.ticket_parts.first().segment
                    emd_segment_flight_date = emd_related_segment.departuretime.date()
                    if emd_issuing_date == emd_segment_flight_date and is_emitted_in_airport:
                        emd.is_subjected_to_fees = False
                
                if emd.is_subjected_to_fees:
                    if emd.ticket_parts.first() is not None:
                        emd_related_segment = emd.ticket_parts.first().segment
                        emd_segment_flight_date = emd_related_segment.departuretime.date()
                        if emd_issuing_date == emd_segment_flight_date and is_emitted_in_airport:
                            emd.is_subjected_to_fees = False
                
                # check fee subjection based on description
                for element in _NOT_FEED_:
                    if emd.ticket_description is not None and emd.ticket_description.find(element) > -1:
                        emd.is_subjected_to_fees = False
                        break
                
                # save modified ticket object
                emd.save()
                
                # update fee if exists
                if not emd.is_subjected_to_fees:
                    temp_fee = emd.fees.first()
                    if temp_fee is not None:
                        temp_fee.cost = 0
                        temp_fee.tax = 0
                        temp_fee.total = 0
                        temp_fee.newest_cost = 0
                        temp_fee.old_cost = 0
                        temp_fee.save()
            except:
                traceback.print_exc()
            
    
    # ticket issued by subcontractor
    def process_subcontract(self):
        if self.issuing_agency is not None:
            issuing_office = OfficeSubcontractor.objects.filter(code=self.issuing_agency.code).first()
            if issuing_office is not None:
                subcontracting_cost = issuing_office.subcontracting_cost
                temp_other_fee_obj = OthersFee()
                temp_other_fee_obj.designation = 'FRAIS DE SOUS-TRAITANCE'
                temp_other_fee_obj.cost = subcontracting_cost
                temp_other_fee_obj.tax = 0
                temp_other_fee_obj.total = subcontracting_cost
                temp_other_fee_obj.pnr = self.pnr
                temp_other_fee_obj.ticket = self
                temp_other_fee_obj.fee_type = 'outsourcing'
                temp_other_fee_obj.creation_date = self.issuing_date
                temp_other_fee_obj.is_subjected_to_fee = False
                temp_other_fee_obj.other_fee_status = self.ticket_status
                
                # check if record already exists
                temp_other_fee_obj_record = OthersFee.objects.filter(ticket=self, designation='FRAIS DE SOUS-TRAITANCE', pnr=self.pnr).first()
                if temp_other_fee_obj_record is not None:
                    temp_other_fee_obj = temp_other_fee_obj_record
                    
                temp_other_fee_obj.save()
                
                self.ticket_status = 1
                self.save()
                
    # udpate pnr state
    def update_pnr_state(self, pnr):
        unfilled_ticket = Ticket.objects.filter(pnr=pnr, state=2).first()
        if unfilled_ticket is None:
            pnr.state = 0
        else:
            pnr.state = 2
        pnr.save()
        
    def __str__(self):
        return self.number