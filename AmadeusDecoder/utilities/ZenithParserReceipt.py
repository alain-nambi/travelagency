'''
Created on 3 Feb 2023

@author: Famenontsoa
'''
import decimal
import traceback
from datetime import datetime
from django.db.models import Q

import AmadeusDecoder.utilities.configuration_data as configs

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.TicketPassengerSegment import TicketPassengerSegment,\
    OtherFeeSegment
from AmadeusDecoder.models.invoice.Fee import OthersFee
from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.models.pnr.PnrPassenger import PnrPassenger
from rdflib.util import date_time
from AmadeusDecoder.utilities.Utility import Utility

# PAYMENT_OPTIONS = ['Comptant', 'En compte', 'Virement']
# TICKET_NUMBER_PREFIX = ['Echange billet', 'EMD']
# TO_BE_EXCLUDED_KEY_KEYWORDS = ['Encaissement transaction', 'Encaissement Modification', 'Encaissement des suppléments']
# AIRPORT_AGENCY_CODE = ['DZAUU000B', 'Mayotte ATO']
STARTED_PROCESS_DATE = datetime(2023, 1, 1, 0, 0, 0, 0).date()
# CURRENT_TRAVEL_AGENCY_IDENTIFIER = ['Issoufali', 'ISSOUFALI', 'Mayotte ATO']

PAYMENT_OPTIONS = configs.PAYMENT_OPTIONS
TICKET_NUMBER_PREFIX = configs.TICKET_NUMBER_PREFIX
TO_BE_EXCLUDED_KEY_KEYWORDS = configs.TO_BE_EXCLUDED_KEY_KEYWORDS
AIRPORT_AGENCY_CODE = configs.AIRPORT_AGENCY_CODE
# STARTED_PROCESS_DATE = configs.STARTED_PROCESS_DATE.date()
CURRENT_TRAVEL_AGENCY_IDENTIFIER = configs.CURRENT_TRAVEL_AGENCY_IDENTIFIER

# part types
TICKET_PAYMENT_PART = configs.TICKET_PAYMENT_PART
ADJUSTMENT_PART = configs.ADJUSTMENT_PART
EMD_CANCELLATION_PART = configs.EMD_CANCELLATION_PART
TICKET_CANCELLATION_PART = configs.TICKET_CANCELLATION_PART
PENALTY_PART = configs.PENALTY_PART
AGENCY_FEE_PART = configs.AGENCY_FEE_PART
EMD_NO_NUMBER_POSSIBLE_DESIGNATION = configs.EMD_NO_NUMBER_POSSIBLE_DESIGNATION
DEFAULT_ASSIGNED_PASSENGER_ON_OBJECT = configs.DEFAULT_ASSIGNED_PASSENGER_ON_OBJECT
EMD_BALANCING_STATEMENT_PART = configs.EMD_BALANCING_STATEMENT_PART

# excluded part special identifier
CREDIT_NOTE_IDENTIFIER = ['EMD']

class ZenithParserReceipt():
    '''
    classdocs
    '''


    def __init__(self, content):
        '''
        Constructor
        '''
        self.content = content
        
        self.ajustment_total = []
    
    # get PNR
    def get_pnr(self):
        for part in self.content[0:5]:
            if len(part) == 6:
                return Pnr.objects.filter(number = part).first()
        return None
    
    # get all passenger
    def get_passengers(self):
        passengers = []
        pnr = self.get_pnr()
        if pnr is not None:
            pnr_passengers = pnr.passengers.all()
            for passenger in pnr_passengers:
                passengers.append(passenger.passenger)
            return passengers
        return passengers
    
    # check datetime
    def check_date_time(self, element):
        is_datetime = False
        try:
            datetime.strptime(element.strip().replace('  ', ' '), '%d/%m/%Y %H:%M:%S')
            return True
        except:
            pass
        return is_datetime
    
    # get full date indexes
    def get_full_date_indexes(self):
        date_time_indexes = []
        for i in range(len(self.content)):
            is_date_time = self.check_date_time(self.content[i])
            if is_date_time:
                date_time_indexes.append(i)
        return date_time_indexes
    
    # excluded part from content interval
    def is_excluded(self, part):
        to_be_excluded = False
        for element in part:
            for keyword in TO_BE_EXCLUDED_KEY_KEYWORDS:
                if element.find(keyword) > -1:
                    return True
        return to_be_excluded
        
    # get each parts
    def get_all_receipt_part(self):
        date_time_indexes = self.get_full_date_indexes()
        parts = []
        for i in range(len(date_time_indexes)):
            temp_content = None
            if i == len(date_time_indexes) - 1:
                temp_content = self.content[date_time_indexes[i]:]
            else:
                temp_content = self.content[date_time_indexes[i]: date_time_indexes[i+1]]
            
            if not self.is_excluded(temp_content):
                parts.append(temp_content)
            
        return parts
    
    # get excluded parts
    def get_all_excluded_part(self):
        date_time_indexes = self.get_full_date_indexes()
        parts = []
        for i in range(len(date_time_indexes)):
            temp_content = None
            if i == len(date_time_indexes) - 1:
                temp_content = self.content[date_time_indexes[i]:]
            else:
                temp_content = self.content[date_time_indexes[i]: date_time_indexes[i+1]]
            
            if self.is_excluded(temp_content):
                parts.append(temp_content)
        
        return parts
    
    # get each part by type
    def get_parts_by_type(self, receipt_parts, part_types):
        matching_part_types = []
        for part in receipt_parts:
            for part_type in part_types:
                if part_type in part:
                    matching_part_types.append(part)
        return matching_part_types
    
    # get parts by type [advanced search]
    def get_parts_by_type_advanced_search(self, receipt_parts, part_types):
        matching_part_types = []
        for part in receipt_parts:
            for sub_part in part:
                sub_part_space_split = sub_part.split(' ')
                for part_type in part_types:
                    if part_type in sub_part_space_split:
                        matching_part_types.append(part)
                        continue
        return matching_part_types
    
    # get part emitter
    def get_part_emitter(self, current_part):
        is_known_emitter = False
        emitter_displayed_name = ''
        
        emitter_part = current_part[1]
        if len(emitter_part.split('.')) > 1:
            emitter_displayed_name = emitter_part.split('.')[-1]
        else:
            emitter_displayed_name = emitter_part
        
        # Search by username and first_name
        temp_user = User.objects.filter( \
                        Q(username__iexact=emitter_displayed_name.capitalize()) | \
                        Q(username=emitter_displayed_name) | \
                        Q(username=emitter_displayed_name.lower()) | \
                        Q(username=emitter_displayed_name.upper()) | \
                        Q(first_name__iexact=emitter_displayed_name.capitalize()) | \
                        Q(first_name=emitter_displayed_name) | \
                        Q(first_name=emitter_displayed_name.lower()) | \
                        Q(first_name=emitter_displayed_name.upper())
                    ).first()
        
        print(f'<> Temp User : {temp_user} \n<> Emitter Displayed Name : {emitter_displayed_name}')
        
        if temp_user is not None:
            is_known_emitter = True
            return is_known_emitter, temp_user
        else:
            return is_known_emitter, emitter_displayed_name
    
    
    # check if part has been issued by current Travel Agency
    def check_part_emitter(self, current_part):
        is_emitted = False
        for identifier in CURRENT_TRAVEL_AGENCY_IDENTIFIER:
            if current_part[1].find(identifier) > -1 or current_part[2].find(identifier) > -1:
                return True
        
        # check agent
        if len(current_part[1].split('.')) > 1:
            temp_user = User.objects.filter(username__iexact=current_part[1].split('.')[1].capitalize()).first()
            if temp_user is not None:
                return True
        
        return is_emitted
    
    # get target part index
    def get_target_part_index(self, current_part, targets):
        for i in range(len(current_part)):
            for target in targets:
                if current_part[i].strip() == target:
                    return i
        return 0
    
    # get target part index: find target inside strings
    def get_target_part_index_extended(self, current_part, targets):
        for i in range(len(current_part)):
            for target in targets:
                if (current_part[i].find(target.capitalize()) > -1 or current_part[i].find(target) > -1 or current_part[i].find(target.upper()) > -1):
                    return i
        return 0
    
    # get passenger assigned on part
    def get_passenger_assigned_on_part(self, passengers, current_part, is_none_required):
        # possible cases
        # '[Jacky Joseph bernard Maunier]' => OK
        # '[Jacky Joseph','bernard Maunier]' => OK
        # '[DZA>RUN] [Jacky Joseph bernard', 'Maunier]'
        # '[Aller Retour] [Jacky Joseph bernard', 'Maunier] [coupons: [15774394]'
        part_passenger = None
        next_index = 0
        passenger_name = ''
        for i in range(len(current_part)):
            # temp_part_split = current_part[i].split(' ')
            temp_part_split_2 = current_part[i].split('[')
            for passenger in passengers:
                # for temp_part in temp_part_split:
                #     if passenger.name.find(temp_part.removeprefix('[').removesuffix(']')) > -1 and temp_part != '':
                #         print(temp_part)
                #         passenger_name += temp_part.removeprefix('[').removesuffix(']') + ' '
                for temp_part in temp_part_split_2:
                    if passenger.name.find(temp_part.removesuffix(']')) > -1 and temp_part != '':
                        # '[Jacky Joseph bernard Maunier]'
                        if temp_part.removesuffix(']').strip() == passenger.name:
                            passenger_name += temp_part.removesuffix(']')
                        else:
                            # '[DZA>NOS][SALIMA KAZOUKO EP', 'SAID][coupons:1246159] () (EMD'
                            # '[Jacky Joseph','bernard Maunier]' or '[DZA>RUN] [Jacky Joseph bernard', 'Maunier]' or [Aller Retour] [Jacky Joseph bernard', 'Maunier] [coupons: [15774394]
                            if passenger.name.find(current_part[i + 1].split(']')[0].removesuffix(']')) > -1:
                                passenger_name += temp_part + ' ' + current_part[i + 1].split(']')[0].removesuffix(']')
                        break
                    # '[Ali Hamza HAMZA] (EMD', ':7328200069142)'
                    elif temp_part.split(']')[0].strip() == passenger.name or temp_part.split(']')[0].strip() == ' '.join(passenger.name.split()[::-1]):
                        passenger_name += temp_part.split(']')[0]
                        break
            if current_part[i].strip() in PAYMENT_OPTIONS:
                next_index = i
        
        for passenger in passengers:
            if passenger_name.strip() == passenger.name or ' '.join(passenger_name.strip().split()[::-1]) == passenger.name:
                part_passenger = passenger
        
        if part_passenger is None and not is_none_required:
            for passenger in passengers:
                if passenger.types in DEFAULT_ASSIGNED_PASSENGER_ON_OBJECT:
                    part_passenger = passenger
                    break
            if part_passenger is None:
                part_passenger = passengers[0]
        elif part_passenger is None and is_none_required:
            part_passenger = None
            
        return part_passenger, next_index
    
    # get ticket/emd number assigned on part
    def get_ticket_emd_number_on_part(self, current_part):
        ticket_number = None
        for i in range(len(current_part)):
            element = current_part[i]
            for prefix in TICKET_NUMBER_PREFIX:
                if element.startswith(prefix):
                    ticket_number = element.removeprefix(prefix).strip().removeprefix('[').removesuffix(']').removeprefix(':').removeprefix('(').removesuffix(')')
                elif element.endswith(prefix):
                    temp_element = current_part[i + 1]
                    ticket_number = temp_element.removeprefix(prefix).strip().removeprefix('[').removesuffix(']').removeprefix(':').removeprefix('(').removesuffix(')')
                elif not element.startswith(prefix) and not element.endswith(prefix) and element.find(prefix) > -1:
                    element = element[element.find(prefix):]
                    ticket_number = element.replace(prefix, '').replace('(', '').replace(')', '').replace(':', '').strip()
        if ticket_number:
            if not ticket_number.strip().isnumeric():
                return None
        return ticket_number
    
    def get_ticket_number_on_part_advanced(self, current_part):
        # we must exclude the cost part so for i in range(len(current_part)-1) notice the -1
        for i in reversed(range(len(current_part)-1)):
            temp_value_separated = Utility.separate_number(current_part[i], 13)
            if len(temp_value_separated) > 0:
                for value in temp_value_separated:
                    if value.isnumeric():
                        return value
    
    # get segment assigned on part
    def get_segments_assigned_on_part(self, current_part):
        # possible cases
        # [DZA>RUN]
        # [DZA>RUN] [Jacky Joseph bernard', 'Maunier]
        # 1er BAGAGE 23kg [DZA>RUN]
        # [Aller Retour]
        segment = None
        air_segments = self.get_pnr().segments.all()
        for i in range(len(current_part)):
            temp_part_split = current_part[i].split(' ')
            for temp_segment in air_segments:
                for temp_part in temp_part_split:
                    if len(temp_part.split('>')) > 1:
                        if temp_part.split('>')[0].removeprefix('[').removesuffix(']').find(temp_segment.codeorg.iata_code) > -1 \
                            and temp_part.split('>')[1].removeprefix('[').removesuffix(']').find(temp_segment.codedest.iata_code) > -1 \
                            and temp_part != '':
                                return temp_segment
        
        if segment is None:
            segment = []
            for temp in air_segments:
                segment.append(temp)
            return segment
    
    # get issuing date
    def get_issuing_date_on_part(self, current_part):
        issuing_date = None
        try:
            issuing_date = datetime.strptime(current_part[0].strip().replace('  ', ' '), '%d/%m/%Y %H:%M:%S')
        except:
            print('Getting issuing date encountered some error in ZenithParserReceipt.')
            return datetime.now()
        return issuing_date
    
    # check if current item has been invoiced or not yet
    def check_is_invoiced_status(self, ticket, other_fee):
        if ticket is not None:
            return ticket.is_invoiced
        elif other_fee is not None:
            return other_fee.is_invoiced
        return False
    
    # get issuing agency name
    def getIssuingAgencyName(self, part):
        return part[2]
    
    # fee subjection status
    def check_fee_subjection_status(self, date_time, current_segment, pnr, ticket, other_fee, part):
        emitter = pnr.get_emit_agent()
        tester = False
        segment_departuretime = None
                
        if emitter is not None and not isinstance(emitter, str):
            if isinstance(current_segment, list):
                for segment in current_segment:
                    segment_departuretime = segment.departuretime
                    if emitter.office.code in AIRPORT_AGENCY_CODE and segment_departuretime is not None:
                        if segment_departuretime.date() == date_time.date():
                            tester = True
                            break
            else:
                segment_departuretime = current_segment.departuretime
                if emitter.office.code in AIRPORT_AGENCY_CODE and segment_departuretime is not None:
                    if segment_departuretime.date() == date_time.date():
                        tester = True
        
        if part[2] in AIRPORT_AGENCY_CODE:
            # set issuing agency name
            if ticket is not None:
                ticket.issuing_agency_name = part[2]
            elif other_fee is not None:
                other_fee.issuing_agency_name = part[2]
            
            if isinstance(current_segment, list):
                for segment in current_segment:
                    segment_departuretime = segment.departuretime
                    if segment_departuretime is not None:
                        if segment_departuretime.date() == date_time.date():
                            tester = True
                            break
            else:
                segment_departuretime = current_segment.departuretime
                if segment_departuretime is not None:
                    if segment_departuretime.date() == date_time.date():
                        tester = True
        
        if tester:
            if ticket is not None:
                ticket.is_subjected_to_fees = False
            elif other_fee is not None:
                other_fee.is_subjected_to_fee = False
                    
    # check issuing date
    def check_issuing_date(self, date_time):
        is_flown = False
        if date_time < STARTED_PROCESS_DATE:
            is_flown = True
        return is_flown
    
    # get same issued ticket based on cost, issuing_date and segment
    def get_ticket(self, cost, issuing_date, segment, current_pnr):
        if isinstance(segment, list):
            segment = segment[0]
        related_tickets = Ticket.objects.filter(total=cost, issuing_date__lte=issuing_date
                                                , ticket_parts__segment__departuretime=segment.departuretime
                                                , ticket_parts__segment__arrivaltime=segment.arrivaltime
                                                , ticket_parts__segment__codedest=segment.codedest
                                                , ticket_parts__segment__codeorg=segment.codeorg
                                                , ticket_parts__segment__flightno=segment.flightno) \
                                                .exclude(pnr=current_pnr).all()
        
        return related_tickets
    
    # perform data transfer between parent and child pnr
    def child_parent_data_transfer(self, parent_pnr, child_pnr):
        # current pnr's segments
        child_pnr_segment = child_pnr.segments.all()
        
        # transfer passenger
        parent_pnr_passengers = parent_pnr.passengers.all()
        for pnr_passenger in parent_pnr_passengers:
            temp_pnr_passenger_obj = PnrPassenger()
            temp_pnr_passenger_obj.passenger = pnr_passenger.passenger
            temp_pnr_passenger_obj.pnr = child_pnr
            temp_pnr_passenger_obj.save()
        
        # transfer ticket
        parent_pnr_tickets = parent_pnr.tickets.all()
        for ticket in parent_pnr_tickets:
            for segment in child_pnr_segment:
                if ticket.ticket_parts.first().segment.codeorg == segment.codeorg and \
                    ticket.ticket_parts.first().segment.codedest == segment.codedest:
                    temp_ticket_status = ticket.ticket_status
                    # required to update parent PNR total
                    ticket.ticket_status = 0
                    ticket.save()
                    
                    ticket.pnr = child_pnr
                    ticket.ticket_status = temp_ticket_status
                    ticket.save()
        
        # transfer other fees
        parent_pnr_otherfees = parent_pnr.others_fees.all()
        for other_fee in parent_pnr_otherfees:
            for segment in child_pnr_segment:
                if other_fee.related_segments.first().segment.codeorg == segment.codeorg and \
                    other_fee.related_segments.first().segment.codedest == segment.codedest:
                    temp_other_fee_status = other_fee.other_fee_status
                    # required to update parent PNR total
                    other_fee.other_fee_status = 0
                    other_fee.save()
                    
                    other_fee.pnr = child_pnr
                    other_fee.other_fee_status = temp_other_fee_status
                    other_fee.save()
                    
        # update pnr split values
        parent_pnr.is_parent = True
        parent_pnr.is_splitted = True
        parent_pnr.children_pnr = [child_pnr.number]
        parent_pnr.save()
        
        child_pnr.is_child = True
        child_pnr.is_splitted = True
        child_pnr.parent_pnr = [parent_pnr.number]
        child_pnr.save()
    
    # process PNR split
    def process_pnr_split(self, issuing_date, current_part, element_cost, current_pnr):
        part_segment = self.get_segments_assigned_on_part(current_part)
        related_tickets = self.get_ticket(element_cost, issuing_date, part_segment, current_pnr)
        parent_pnr = None
        
        for ticket in related_tickets:
            temp_passenger = [ticket.passenger]
            current_passenger_match = self.get_passenger_assigned_on_part(temp_passenger, current_part, True)
            if current_passenger_match is not None:
                parent_pnr = ticket.pnr
                
        # perform data transfer between parent and child PNR
        if parent_pnr is not None:
            self.child_parent_data_transfer(parent_pnr, current_pnr)
    
    # ticket payment handling
    # When costs and taxes are not found on the original PNR
    def handle_ticket_payment(self, pnr, passengers, payment_part):
        for part in payment_part:
            date_time = self.get_issuing_date_on_part(part)
            current_passenger, next_index = self.get_passenger_assigned_on_part(passengers, part, True)
            is_created_by_us = self.check_part_emitter(part)
            is_know_emitter, emitter = self.get_part_emitter(part)
            issuing_agency_name = self.getIssuingAgencyName(part)
            
            ticket_total = 0
            try:
                ticket_total = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
            except:
                traceback.print_exc()
            
            ticket = Ticket.objects.filter(pnr=pnr, passenger=current_passenger).filter(Q(total=ticket_total) | Q(total=0)).first()
            # ticket = Ticket.objects.filter(Q(pnr=pnr) & Q(passenger=current_passenger) & (Q(total=ticket_total) | Q(total=0))).first()
            try:
                payment_option = part[next_index]
                if ticket is not None:
                    ticket.payment_option = payment_option
                    if ticket.total == 0 and ticket_total > 0:
                        ticket.total = ticket_total
                        ticket.transport_cost = ticket_total - ticket.tax
                        ticket.issuing_date  = date_time.date()
                    if not is_created_by_us or self.check_issuing_date(date_time.date()):
                        # or (pnr.system_creation_date.date() > date_time.date() and self.check_is_invoiced_status(ticket, None)):
                        ticket.state = 0
                        ticket.ticket_status = 3
                    ticket.is_subjected_to_fees = True
                    # emitter
                    if is_know_emitter:
                        ticket.emitter = emitter
                    else:
                        ticket.issuing_agent_name = emitter
                    ticket.issuing_agency_name = issuing_agency_name
                    ticket.save()
                # PNR has been modified and old ticket record has been removed by Zenith
                # So, the ticket payment will be saved as other fees with designation as "Paiement billet - 1"
                else:
                    ticket = Ticket.objects.filter(pnr=pnr, passenger=current_passenger, total=ticket_total).first()
                    if ticket is None and ticket_total > 0 and current_passenger is not None:
                        designation = "Paiement Billet - " + str(current_passenger)
                        
                        new_payment = OthersFee()
                        new_payment.pnr = pnr
                        new_payment.cost = ticket_total
                        new_payment.total = ticket_total
                        new_payment.passenger = current_passenger
                        new_payment.designation = designation
                        new_payment.is_subjected_to_fee = True
                        new_payment.issuing_agency_name = issuing_agency_name
                        
                        # check if it has been already saved
                        temp_new_payment = OthersFee.objects.filter(passenger=current_passenger, total=ticket_total, pnr=pnr, designation=designation).first()
                        if temp_new_payment is not None:
                            new_payment = temp_new_payment
                        
                        if not is_created_by_us or self.check_issuing_date(date_time.date()):
                            # or (pnr.system_creation_date.date() > date_time.date() and self.check_is_invoiced_status(None, new_payment)):
                            new_payment.other_fee_status = 3
                            
                        if current_passenger.passenger_status == 0:
                            new_payment.other_fee_status = 0
                        
                        new_payment.creation_date = date_time
                        new_payment.fee_type = 'TKT'
                        
                        # emitter
                        if is_know_emitter:
                            new_payment.emitter = emitter
                        else:
                            new_payment.issuing_agent_name = emitter
                        
                        new_payment.save()
                    else:
                        # check splitted PNR
                        '''
                            Duplicate PNR processing: comment to be removed once PNR/passenger transfer issue solved
                            Check functions: process_pnr_split, child_parent_data_transfer, get_ticket and get_passenger_assigned_on_part
                        '''
                        # self.process_pnr_split(date_time.date(), part, ticket_total, pnr)
            except Exception as e:
                traceback.print_exc()
                print(e)
                
            #
            # temp_ticket = Ticket.objects.filter(pnr=pnr, passenger=current_passenger, issuing_date=date_time).first()
            #
            # if current_passenger is not None and temp_ticket is not None:
            #     try:
            #         temp_ticket.payment_option = part[next_index]
            #         if temp_ticket.total == 0:
            #             temp_ticket.total = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
            #             temp_ticket.transport_cost = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.')) - temp_ticket.tax
            #             temp_ticket.issuing_date  = date_time.date()
            #         if not is_created_by_us or (pnr.system_creation_date.date() > date_time.date() and self.check_is_invoiced_status(temp_ticket, None)):
            #             temp_ticket.state = 0
            #             temp_ticket.ticket_status = 3
            #     except Exception as e:
            #         traceback.print_exc()
            #         print(e)
            #     temp_ticket.save()
    
    # ticket adjustment
    def handle_ticket_adjustment(self, pnr, passengers, adjustment_part):
        for part in adjustment_part: 
            date_time = self.get_issuing_date_on_part(part)
            current_passenger, next_index = self.get_passenger_assigned_on_part(passengers, part, False)
            is_created_by_us = self.check_part_emitter(part)
            is_know_emitter, emitter = self.get_part_emitter(part)
            issuing_agency_name = self.getIssuingAgencyName(part)
            # make current tickets as flown
            # temp_ticket = Ticket.objects.filter(pnr=pnr, passenger=current_passenger, ticket_type='TKT').order_by('-id').first()
            
            # remove line from display when an invoice has already been created
            # if temp_ticket is not None:
            #     if self.check_is_invoiced_status(temp_ticket, None):
            #         temp_ticket.ticket_status = 3
            #         temp_ticket.save()
            
            # amount
            transport_cost = 0
            tax = 0
            total = 0
            
            try:
                transport_cost = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                tax = 0
                total = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
            except:
                pass   
                            
            # get adjustment
            # for element in part:
            #     for prefix in TICKET_NUMBER_PREFIX:
            #         if element.startswith(prefix):
            #             new_ticket.number = element.removeprefix(prefix).strip().removeprefix('[').removesuffix(']').removeprefix(':')
            
            is_untracked_reajustment = False
            
            original_ticket_number = self.get_ticket_emd_number_on_part(part)
            
            if original_ticket_number is not None:
                # check if it has been already saved
                # ⚠️⚠️⚠️ Ticket adjustment always come with the number 
                # of the original ticket and must be preceded by a PNR with a new ticket number under the old original cost 
                #
                ticket_saved_checker = Ticket.objects.filter(number=original_ticket_number, pnr=pnr).first() # we don't touch this one
                if ticket_saved_checker is not None:
                    # check if is invoiced
                    # if ticket_saved_checker.is_invoiced:
                    #    continue
                    
                    previous_ticket = Ticket.objects.filter(total=ticket_saved_checker.total, pnr=pnr, passenger=ticket_saved_checker.passenger).exclude(number=original_ticket_number).last()
                    if previous_ticket is not None:
                        # amount
                        previous_ticket.transport_cost = transport_cost
                        previous_ticket.tax = tax
                        previous_ticket.total = total
                
                        if previous_ticket.total == 0:
                            previous_ticket.is_no_adc = True
                            previous_ticket.tax = 0
                        
                        if not is_created_by_us:
                            #or (pnr.system_creation_date.date() > date_time.date()):
                            previous_ticket.ticket_status = 3
                        
                        # if ((pnr.system_creation_date.date() > date_time.date()) and self.check_is_invoiced_status(previous_ticket, None)) or self.check_issuing_date(date_time.date()):
                        if self.check_issuing_date(date_time.date()):
                            #self.check_is_invoiced_status(previous_ticket, None) or 
                            previous_ticket.ticket_status = 3
                        
                        previous_ticket.ticket_description = 'modif'
                        
                        # emitter
                        if is_know_emitter:
                            previous_ticket.emitter = emitter
                        else:
                            previous_ticket.issuing_agent_name = emitter
                        
                        previous_ticket.issuing_agency_name = issuing_agency_name
                        previous_ticket.save()
                        self.ajustment_total.append({'ticket': previous_ticket, 'total': total})
                    else:
                        # if receipt is sent twice
                        previous_ticket = Ticket.objects.filter(pnr=pnr, passenger=ticket_saved_checker.passenger, ticket_description='modif', issuing_date=date_time.date()).exclude(number=original_ticket_number).exclude(ticket_status=0).last()
                        if previous_ticket is None:
                            is_untracked_reajustment = True
                else:
                    is_untracked_reajustment = True
                
                # if ticket is not saved 
                # PNR has no history
                if is_untracked_reajustment:
                    designation = 'Reissuance Adjustment: ' + original_ticket_number
                    current_segment = self.get_segments_assigned_on_part(part)
                    cost = 0
                    tax = 0
                    total = 0
                    
                    try:
                        cost = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                        tax = 0
                        total = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                    except:
                        pass
                    
                    adjustment_tester = OthersFee.objects.filter(designation=designation, pnr=pnr, total=total).first()
                                    
                    if adjustment_tester is None:
                        new_other_fee = OthersFee()
                        new_other_fee.designation = designation
                        new_other_fee.cost = cost
                        new_other_fee.tax = tax
                        new_other_fee.total = total
                        new_other_fee.pnr = pnr
                        new_other_fee.fee_type = 'TKT'
                        new_other_fee.creation_date = date_time.date()
                        new_other_fee.issuing_agency_name = issuing_agency_name
                        
                        if not is_created_by_us:
                            new_other_fee.other_fee_status = 0
                        
                        if self.check_issuing_date(date_time.date()):
                            new_other_fee.ticket_status = 3
                        
                        # emitter
                        if is_know_emitter:
                            new_other_fee.emitter = emitter
                        else:
                            new_other_fee.issuing_agent_name = emitter
                        
                        new_other_fee.save()
                        self.ajustment_total.append({'other_fee': new_other_fee, 'total': total})
                        
                        if isinstance(current_segment, list):
                            for segment in current_segment:
                                other_fee_passenger_segment = OtherFeeSegment()
                                other_fee_passenger_segment.other_fee = new_other_fee
                                other_fee_passenger_segment.passenger = current_passenger
                                other_fee_passenger_segment.segment = segment
                                other_fee_passenger_segment.save()
                        else:
                            other_fee_passenger_segment = OtherFeeSegment()
                            other_fee_passenger_segment.other_fee = new_other_fee
                            other_fee_passenger_segment.passenger = current_passenger
                            other_fee_passenger_segment.segment = current_segment
                            other_fee_passenger_segment.save()
                    
    # emd cancellation
    def handle_emd_cancellation(self, pnr, passengers, cancellation_part):
        for part in cancellation_part:
            date_time = self.get_issuing_date_on_part(part)
            current_passenger, next_index = self.get_passenger_assigned_on_part(passengers, part, False)
            current_segment = self.get_segments_assigned_on_part(part)
            is_know_emitter, emitter = self.get_part_emitter(part)
            issuing_agency_name = self.getIssuingAgencyName(part)
            # new emd to be inserted
            new_emd = OthersFee()
            new_emd.pnr = pnr
            part_name_index = self.get_target_part_index(part, EMD_CANCELLATION_PART)
            if part_name_index is not None:
                new_emd.designation = part[part_name_index + 1]
            
            is_created_by_us = self.check_part_emitter(part)
            
            # make current other_fee as flown
            '''
            temp_emd = Ticket.objects.filter(pnr=pnr, passenger=current_passenger, ticket_type='EMD').order_by('-id').first()
            if temp_emd is not None:
                if self.check_is_invoiced_status(temp_emd, None):
                    temp_emd.ticket_status = 3
                    temp_emd.save()
            
            temp_other_fees = OthersFee.objects.filter(pnr=pnr, related_segments__passenger=current_passenger).all()
            for other_fee in temp_other_fees:
                if self.check_is_invoiced_status(None, other_fee):
                    other_fee.other_fee_status = 3
                    other_fee.save()'''
            
            # get cancellation
            if new_emd.designation is not None:
                try:
                    new_emd.cost = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                    new_emd.total = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                except:
                    pass
                
                # check is it has been already saved
                otherfee_saved_checker = OthersFee.objects.filter(designation=new_emd.designation, pnr=pnr, related_segments__passenger=current_passenger).first()
                if otherfee_saved_checker != None:
                    new_emd = otherfee_saved_checker
                    if is_created_by_us:
                        new_emd.other_fee_status = 1
                    # if (pnr.system_creation_date.date() > date_time.date()) and self.check_is_invoiced_status(otherfee_saved_checker, None):
                    #     otherfee_saved_checker.other_fee_status = 3
                if not is_created_by_us or self.check_issuing_date(date_time.date()):
                    new_emd.other_fee_status = 3
                new_emd.fee_type = 'Cancellation'
                new_emd.creation_date = date_time.date()
                
                # emitter
                if is_know_emitter:
                    new_emd.emitter = emitter
                else:
                    new_emd.issuing_agent_name = emitter
                
                new_emd.issuing_agency_name = issuing_agency_name
                new_emd.save()
                if otherfee_saved_checker is None:
                    if isinstance(current_segment, list):
                        for segment in current_segment:
                            other_fee_passenger_segment = OtherFeeSegment()
                            other_fee_passenger_segment.other_fee = new_emd
                            other_fee_passenger_segment.passenger = current_passenger
                            other_fee_passenger_segment.segment = segment
                            other_fee_passenger_segment.save()
                    else:
                        other_fee_passenger_segment = OtherFeeSegment()
                        other_fee_passenger_segment.other_fee = new_emd
                        other_fee_passenger_segment.passenger = current_passenger
                        other_fee_passenger_segment.segment = current_segment
                        other_fee_passenger_segment.save()
                        
    # ticket cancellation
    def handle_ticket_cancellation(self, pnr, passengers, cancellation_part):
        for part in cancellation_part:
            date_time = self.get_issuing_date_on_part(part)
            current_passenger, next_index = self.get_passenger_assigned_on_part(passengers, part, False)
            current_segment = self.get_segments_assigned_on_part(part)
            is_know_emitter, emitter = self.get_part_emitter(part)
            issuing_agency_name = self.getIssuingAgencyName(part)
            # new emd to be inserted
            new_emd = OthersFee()
            new_emd.pnr = pnr
            part_name_index = self.get_target_part_index(part, TICKET_CANCELLATION_PART)
            if part_name_index is not None:
                new_emd.designation = part[part_name_index + 1]
            
            is_created_by_us = self.check_part_emitter(part)
            
            # make current other_fee as flown
            '''
            temp_emd = Ticket.objects.filter(pnr=pnr, passenger=current_passenger, ticket_type='EMD').order_by('-id').first()
            if temp_emd is not None:
                if self.check_is_invoiced_status(temp_emd, None):
                    temp_emd.ticket_status = 3
                    temp_emd.save()
            
            temp_other_fees = OthersFee.objects.filter(pnr=pnr, related_segments__passenger=current_passenger).all()
            for other_fee in temp_other_fees:
                if self.check_is_invoiced_status(None, other_fee):
                    other_fee.other_fee_status = 3
                    other_fee.save()'''
            
            # get cancellation
            if new_emd.designation is not None:
                try:
                    new_emd.cost = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                    new_emd.total = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                except:
                    pass
                
                # check is it has been already saved
                otherfee_saved_checker = OthersFee.objects.filter(designation=new_emd.designation, pnr=pnr, related_segments__passenger=current_passenger, total=new_emd.total).first()
                if otherfee_saved_checker != None:
                    new_emd = otherfee_saved_checker
                    if is_created_by_us:
                        new_emd.other_fee_status = 1
                    # if (pnr.system_creation_date.date() > date_time.date()) and self.check_is_invoiced_status(otherfee_saved_checker, None):
                    #     otherfee_saved_checker.other_fee_status = 3
                if not is_created_by_us or self.check_issuing_date(date_time.date()):
                    new_emd.other_fee_status = 3
                new_emd.fee_type = 'Cancellation'
                new_emd.creation_date = date_time.date()
                
                # check if cancellation occurs at the same time as ticket arrival
                # issuing date must be the same for both ticket or other fee
                # both ticket or other fee must not be invoiced
                # ticket or other fee's abs total cost must be the same as abs of current cancellation 
                # after all above conditions checked, related ticket or other fee's fee must be removed from database
                temp_related_ticket = Ticket.objects.filter(issuing_date=date_time.date(), is_invoiced=False, total=abs(new_emd.total)).last()
                temp_related_other_fee = OthersFee.objects.filter(creation_date=date_time.date(), is_invoiced=False, total=abs(new_emd.total)).last()
                if temp_related_ticket is not None:
                    new_emd.ticket = temp_related_ticket
                    temp_related_ticket.is_subjected_to_fee = False
                    temp_related_ticket.save()
                    
                    temp_related_ticket_fee = temp_related_ticket.fees.first()
                    if temp_related_ticket_fee is not None:
                        temp_related_ticket_fee.delete()
                elif temp_related_other_fee is not None:
                    new_emd.other_fee = temp_related_other_fee
                    temp_related_other_fee.is_subjected_to_fee = False
                    temp_related_other_fee.save()
                    
                    temp_related_other_fee_fee = temp_related_other_fee.fees.first()
                    if temp_related_other_fee_fee is not None:
                        temp_related_other_fee_fee.delete()
                
                # emitter
                if is_know_emitter:
                    new_emd.emitter = emitter
                else:
                    new_emd.issuing_agent_name = emitter
                
                new_emd.issuing_agency_name = issuing_agency_name
                
                new_emd.save()
                if otherfee_saved_checker is None:
                    if isinstance(current_segment, list):
                        for segment in current_segment:
                            other_fee_passenger_segment = OtherFeeSegment()
                            other_fee_passenger_segment.other_fee = new_emd
                            other_fee_passenger_segment.passenger = current_passenger
                            other_fee_passenger_segment.segment = segment
                            other_fee_passenger_segment.save()
                    else:
                        other_fee_passenger_segment = OtherFeeSegment()
                        other_fee_passenger_segment.other_fee = new_emd
                        other_fee_passenger_segment.passenger = current_passenger
                        other_fee_passenger_segment.segment = current_segment
                        other_fee_passenger_segment.save()
                    
    # emd when no ticket number provided
    def handle_emd_no_number(self, pnr, current_passenger, current_segment, is_created_by_us, cost, total, date_time, issuing_agency_name, emd_single_part):
        is_know_emitter, emitter = self.get_part_emitter(emd_single_part)
        is_balancing_statement = False
        
        designation_index = self.get_target_part_index_extended(emd_single_part, EMD_NO_NUMBER_POSSIBLE_DESIGNATION)
        
        # check if current line is just an EMD Balancing Statement
        if designation_index == 0 and self.get_target_part_index_extended(emd_single_part, EMD_BALANCING_STATEMENT_PART) > 0:
            is_balancing_statement = True
            designation_index = self.get_target_part_index_extended(emd_single_part, EMD_BALANCING_STATEMENT_PART)
        
        designation = None
        if designation_index > 0:
            designation = emd_single_part[designation_index]

        new_emd = OthersFee()
        new_emd.pnr = pnr
        new_emd.designation = designation
        
        # get cancellation
        if new_emd.designation is not None:
            try:
                new_emd.cost = cost
                new_emd.total = total
            except:
                pass
            
            # check is it has been already saved
            if isinstance(current_segment, list):
                otherfee_saved_checker = OthersFee.objects.filter(designation=new_emd.designation, pnr=pnr, related_segments__passenger=current_passenger, total=new_emd.total).first()
            else:
                otherfee_saved_checker = OthersFee.objects.filter(designation=new_emd.designation, pnr=pnr, related_segments__passenger=current_passenger, related_segments__segment=current_segment, total=new_emd.total).first()
                
            if otherfee_saved_checker is not None:
                new_emd = otherfee_saved_checker
                new_emd.other_fee_status = 1
                if is_created_by_us:
                    new_emd.other_fee_status = 1
                # if self.check_is_invoiced_status(None, otherfee_saved_checker):
                #     new_emd.other_fee_status = 3
            if not is_created_by_us or self.check_issuing_date(date_time.date()):
                # or (pnr.system_creation_date.date() > date_time.date()):
                new_emd.other_fee_status = 3
            new_emd.fee_type = 'EMD'
            new_emd.creation_date = date_time.date()
            # check fee subjection
            try:
                self.check_fee_subjection_status(date_time, current_segment, pnr, None, new_emd, emd_single_part)
            except:
                traceback.print_exc()
            
            # remove fee if special condition
            if is_balancing_statement:
                new_emd.is_subjected_to_fee = False
            
            # emitter
            if is_know_emitter:
                new_emd.emitter = emitter
            else:
                new_emd.issuing_agent_name = emitter
            
            new_emd.issuing_agency_name = issuing_agency_name
            
            new_emd.save()
            if otherfee_saved_checker is None:
                if isinstance(current_segment, list):
                    for segment in current_segment:
                        other_fee_passenger_segment = OtherFeeSegment()
                        other_fee_passenger_segment.other_fee = new_emd
                        other_fee_passenger_segment.passenger = current_passenger
                        other_fee_passenger_segment.segment = segment
                        other_fee_passenger_segment.save()
                else:
                    other_fee_passenger_segment = OtherFeeSegment()
                    other_fee_passenger_segment.other_fee = new_emd
                    other_fee_passenger_segment.passenger = current_passenger
                    other_fee_passenger_segment.segment = current_segment
                    other_fee_passenger_segment.save()
    
    # emd
    def handle_emd(self, pnr, passengers, emd_part):
        for part in emd_part:
            date_time = self.get_issuing_date_on_part(part)
            current_passenger, next_index = self.get_passenger_assigned_on_part(passengers, part, False)
            current_segment = self.get_segments_assigned_on_part(part)
            part_name_index = self.get_target_part_index(part, PENALTY_PART)
            is_know_emitter, emitter = self.get_part_emitter(part)
            issuing_agency_name = self.getIssuingAgencyName(part)
            # skip "Frais d'agence"
            internal_fee = self.get_target_part_index(part, AGENCY_FEE_PART)
            if internal_fee != 0:
                continue
            
            if part_name_index == 0:
                # new emd to be inserted
                new_emd = Ticket()
                new_emd.pnr = pnr
                transport_cost = 0
                try:
                    new_emd.transport_cost = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                    transport_cost = new_emd.transport_cost
                    new_emd.total = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                except:
                    pass

                is_created_by_us = self.check_part_emitter(part)
                # make current other_fee as flown
                
                '''
                temp_emd = Ticket.objects.filter(pnr=pnr, passenger=current_passenger, ticket_type='EMD').order_by('-id').first()
                if temp_emd is not None:
                    if self.check_is_invoiced_status(temp_emd, None):
                        temp_emd.ticket_status = 3
                        temp_emd.save()'''
                
                if isinstance(current_segment, list):
                    temp_other_fees = OthersFee.objects.filter(pnr=pnr, related_segments__passenger=current_passenger, fee_type='EMD').all()
                else:
                    temp_other_fees = OthersFee.objects.filter(pnr=pnr, related_segments__passenger=current_passenger, related_segments__segment=current_segment, fee_type='EMD').all()
                
                for other_fee in temp_other_fees:
                    if other_fee.cost == transport_cost:
                        #self.check_is_invoiced_status(None, other_fee) or 
                        other_fee.other_fee_status = 3
                        other_fee.save()
                
                # get emd
                # for element in part:
                #     for prefix in TICKET_NUMBER_PREFIX:
                #         if element.find(prefix) > -1:
                #             new_emd.number = element.replace(prefix, '').replace('(', '').replace(')', '').replace(':', '')
                # new_emd.number = element.removeprefix(prefix).strip().removeprefix('[').removesuffix(']').removeprefix(':')
                new_emd.number = self.get_ticket_emd_number_on_part(part)
                
                if new_emd.number is not None:
                    # if not is_created_by_us:
                        # or (pnr.system_creation_date.date() > date_time.date()):
                        # new_emd.ticket_status = 3
                    # check is it has been already saved
                    ticket_saved_checker = Ticket.objects.filter(number=new_emd.number, pnr=pnr).first()
                    if ticket_saved_checker != None:
                        new_emd = ticket_saved_checker
                        if is_created_by_us:
                            new_emd.ticket_status = 1
                        '''
                        if self.check_is_invoiced_status(new_emd, None):
                            new_emd.ticket_status = 3 '''
                    if not is_created_by_us or self.check_issuing_date(date_time.date()):
                        # or (pnr.system_creation_date.date() > date_time.date()):
                        new_emd.ticket_status = 3
                    if new_emd.transport_cost == 0:
                        new_emd.is_no_adc = True
                    new_emd.passenger = current_passenger
                    new_emd.ticket_type = 'EMD'
                    new_emd.issuing_date = date_time
                    # check fee subjection
                    try:
                        self.check_fee_subjection_status(date_time, current_segment, pnr, new_emd, None, part)
                    except:
                        traceback.print_exc()
                    # set to refund when negative
                    if new_emd.total < 0:
                        new_emd.is_refund = True
                    
                    # emitter
                    if is_know_emitter:
                        new_emd.emitter = emitter
                    else:
                        new_emd.issuing_agent_name = emitter    
                    
                    new_emd.issuing_agency_name = issuing_agency_name
                    
                    new_emd.save()
                    if ticket_saved_checker is None:
                        if isinstance(current_segment, list):
                            for segment in current_segment:
                                ticket_segment = TicketPassengerSegment()
                                ticket_segment.ticket = new_emd
                                ticket_segment.segment = segment
                                ticket_segment.save()
                        else:
                            ticket_segment = TicketPassengerSegment()
                            ticket_segment.ticket = new_emd
                            ticket_segment.segment = current_segment
                            ticket_segment.save()
                        
                else:
                    # handle EMD with no number
                    self.handle_emd_no_number(pnr, current_passenger, current_segment, is_created_by_us,  new_emd.transport_cost,  new_emd.total, date_time, issuing_agency_name, part)
                    continue
            elif part_name_index > 0:
                # new emd to be inserted
                new_emd = OthersFee()
                new_emd.pnr = pnr
                if part_name_index is not None:
                    new_emd.designation = part[part_name_index + 1]
                
                is_created_by_us = self.check_part_emitter(part)
                
                # make current other_fee as flown
                '''
                temp_emd = Ticket.objects.filter(pnr=pnr, passenger=current_passenger, ticket_type='EMD').order_by('-id').first()
                if temp_emd is not None:
                    # if pnr.system_creation_date.date() > date_time.date():
                    if self.check_is_invoiced_status(temp_emd, None):
                        temp_emd.ticket_status = 3
                        temp_emd.save()
                
                temp_other_fees = OthersFee.objects.filter(pnr=pnr, related_segments__passenger=current_passenger).all()
                for other_fee in temp_other_fees:
                    if self.check_is_invoiced_status(None, other_fee):
                        other_fee.other_fee_status = 3
                        other_fee.save()
                    
                temp_other_emd = Ticket.objects.filter(pnr=pnr, ticket_type='TKT').exclude(ticket_description='modif').all()
                for other_emd in temp_other_emd:
                    if self.check_is_invoiced_status(other_emd, None):
                        other_emd.ticket_status = 3
                        other_emd.save()'''
                
                # get penalty
                if new_emd.designation is not None:
                    try:
                        new_emd.cost = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                        new_emd.total = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                    except:
                        pass
                    
                    # print("***** NEW EMD *****")
                    # print(new_emd.cost)
                    # print(date_time.date)
                    # print(new_emd.designation)
                    # print(new_emd.emitter)
                    # print(current_passenger)
                    # print("----- NEW EMD -----")
                    
                    if not is_created_by_us or self.check_issuing_date(date_time.date()):
                        new_emd.other_fee_status = 3
                    # check is it has been already saved
                    otherfee_saved_checker  =   OthersFee.objects.filter(
                                                    designation=new_emd.designation, 
                                                    pnr=pnr, 
                                                    related_segments__passenger=current_passenger, 
                                                    creation_date=date_time
                                                ).first()

                    # print("***** OTHER FEE SAVED CHECKER *******")
                    # print(otherfee_saved_checker)
                    # print("----- OTHER FEE SAVED CHECKER -------")

                    if otherfee_saved_checker != None:
                        new_emd = otherfee_saved_checker
                        if is_created_by_us:
                            new_emd.other_fee_status = 1
                        # if self.check_is_invoiced_status(None, otherfee_saved_checker):
                        #     otherfee_saved_checker.other_fee_status = 3
                    new_emd.fee_type = 'TKT'
                    new_emd.is_subjected_to_fee = False
                    
                    # check if current penalty has been saved under ticket number added with DE
                    # is_already_saved = False
                    # current_ticket_modif = Ticket.objects.filter(pnr=pnr, ticket_description='modif').all()
                    # for ticket_modif in current_ticket_modif:
                    #     for total in self.ajustment_total:
                    #         if ticket_modif.total == (total['total']+new_emd.total):
                    #             is_already_saved = True
                    #             break
                    
                    new_emd.creation_date = date_time
                    
                    # emitter
                    if is_know_emitter:
                        new_emd.emitter = emitter
                    else:
                        new_emd.issuing_agent_name = emitter
                    
                    new_emd.issuing_agency_name = issuing_agency_name
                    
                    new_emd.save()
                    # if not is_already_saved:
                    if otherfee_saved_checker is None:
                        if isinstance(current_segment, list):
                            for segment in current_segment:
                                other_fee_passenger_segment = OtherFeeSegment()
                                other_fee_passenger_segment.other_fee = new_emd
                                other_fee_passenger_segment.passenger = current_passenger
                                other_fee_passenger_segment.segment = segment
                                other_fee_passenger_segment.save()
                        else:
                            other_fee_passenger_segment = OtherFeeSegment()
                            other_fee_passenger_segment.other_fee = new_emd
                            other_fee_passenger_segment.passenger = current_passenger
                            other_fee_passenger_segment.segment = current_segment
                            other_fee_passenger_segment.save()
                            
    # get Credit note from excluded part
    def get_credit_from_excluded_part(self, pnr, passengers, credit_note_part):
        for part in credit_note_part:
            date_time = self.get_issuing_date_on_part(part)
            current_passenger, next_index = self.get_passenger_assigned_on_part(passengers, part, False)
            current_segment = self.get_segments_assigned_on_part(part)
            is_know_emitter, emitter = self.get_part_emitter(part)
            issuing_agency_name = self.getIssuingAgencyName(part)
            
            new_emd = Ticket()
            new_emd.pnr = pnr
            transport_cost = 0
            new_emd.is_subjected_to_fees = False
            
            # as payment method is here an EMD, the cost will be the last element of the part
            next_index = -2
            try:
                new_emd.transport_cost = -1 * decimal.Decimal("".join(part[next_index+1].split(" ")[0:2]).replace(',','.').replace('EUR', ''))
                transport_cost = -1 * new_emd.transport_cost
                new_emd.total = -1 * decimal.Decimal("".join(part[next_index+1].split(" ")[0:2]).replace(',','.').replace('EUR', ''))
            except:
                pass
            
            
            print("########################################")
            print("# PROCESSING TO CREDIT NOTE FOR ZENITH #")
            print(f"> Transport cost : {new_emd.transport_cost}")
            print(f">          Total : {new_emd.total}")                   
            print("########################################\n") 
            

            is_created_by_us = self.check_part_emitter(part)
            
            if isinstance(current_segment, list):
                temp_other_fees = OthersFee.objects.filter(pnr=pnr, related_segments__passenger=current_passenger, fee_type='EMD').all()
            else:
                temp_other_fees = OthersFee.objects.filter(pnr=pnr, related_segments__passenger=current_passenger, related_segments__segment=current_segment, fee_type='EMD').all()
            
            for other_fee in temp_other_fees:
                if other_fee.cost == transport_cost:
                    other_fee.other_fee_status = 3
                    other_fee.save()
            
            new_emd.number = self.get_ticket_number_on_part_advanced(part)
            
            if new_emd.number is not None:
                # check is it has been already saved
                ticket_saved_checker = Ticket.objects.filter(number=new_emd.number, pnr=pnr).first()
                if ticket_saved_checker != None:
                    new_emd = ticket_saved_checker
                    if is_created_by_us:
                        new_emd.ticket_status = 1
                if not is_created_by_us or self.check_issuing_date(date_time.date()):
                    # or (pnr.system_creation_date.date() > date_time.date()):
                    new_emd.ticket_status = 3
                if new_emd.transport_cost == 0:
                    new_emd.is_no_adc = True
                new_emd.passenger = current_passenger
                new_emd.ticket_type = 'EMD'
                new_emd.issuing_date = date_time
                # check fee subjection
                # try:
                #     self.check_fee_subjection_status(date_time, current_segment, pnr, new_emd, None, part)
                # except:
                #     traceback.print_exc()
                # set to refund when negative
                if new_emd.total < 0:
                    new_emd.is_refund = True
                
                # emitter
                if is_know_emitter:
                    new_emd.emitter = emitter
                else:
                    new_emd.issuing_agent_name = emitter    
                
                new_emd.issuing_agency_name = issuing_agency_name
                
                new_emd.save()
                if ticket_saved_checker is None:
                    if isinstance(current_segment, list):
                        for segment in current_segment:
                            ticket_segment = TicketPassengerSegment()
                            ticket_segment.ticket = new_emd
                            ticket_segment.segment = segment
                            ticket_segment.save()
                    else:
                        ticket_segment = TicketPassengerSegment()
                        ticket_segment.ticket = new_emd
                        ticket_segment.segment = current_segment
                        ticket_segment.save()
        
    # get each value by type and value
    def get_each_value(self):
        receipt_parts = self.get_all_receipt_part()
        passengers = self.get_passengers()
        pnr = self.get_pnr()
        # get ticket payment
        # Marked with: "Paiement Billet"
        ticket_payment_parts = self.get_parts_by_type(receipt_parts, TICKET_PAYMENT_PART)
        self.handle_ticket_payment(pnr, passengers, ticket_payment_parts)
        
        # get ticket adjustment
        # Marked with: "Reissuance Adjustment" or "Réajustement tarifaire"
        ticket_adjustment_part = self.get_parts_by_type(receipt_parts, ADJUSTMENT_PART)
        self.handle_ticket_adjustment(pnr, passengers, ticket_adjustment_part)
        
        # emd cancellation
        # Marked with: "Annulation ancillaries"
        emd_cancellation_part = self.get_parts_by_type(receipt_parts, EMD_CANCELLATION_PART)
        self.handle_emd_cancellation(pnr, passengers, emd_cancellation_part)
        
        # ticket cancellation
        # ticket void
        # refund
        ticket_cancellation_part = self.get_parts_by_type(receipt_parts, TICKET_CANCELLATION_PART)
        self.handle_ticket_cancellation(pnr, passengers, ticket_cancellation_part)
        
        # emd
        # Marked with any other flags to signal EMD like "1er BAGAGE 23kg"
        for ticket_pay_part in ticket_payment_parts:
            receipt_parts.remove(ticket_pay_part)
        
        for ticket_adjust_part in ticket_adjustment_part:
            receipt_parts.remove(ticket_adjust_part)
            
        for emd_cancelled_part in emd_cancellation_part:
            receipt_parts.remove(emd_cancelled_part)
            
        for ticket_cancelled_part in ticket_cancellation_part:
            receipt_parts.remove(ticket_cancelled_part)
        self.handle_emd(pnr, passengers, receipt_parts)
        
        # excluded parts
        excluded_parts = self.get_all_excluded_part()
        
        # credit note
        credit_note_in_excluded_parts = self.get_parts_by_type_advanced_search(excluded_parts, CREDIT_NOTE_IDENTIFIER)
        self.get_credit_from_excluded_part(pnr, passengers, credit_note_in_excluded_parts)
        
        
        # re-check if re-adjustment has been saved
        ''' Currently not used as Ticket adjustment from PNR are ignored.'''
        # self.recheck_saved_adjustment(pnr)
    
    # re-check if re-adjustment has been saved
    def recheck_saved_adjustment(self, pnr):
        current_ticket_modif = Ticket.objects.filter(pnr=pnr, ticket_description='modif').all()
        current_penalty = OthersFee.objects.filter(pnr=pnr, fee_type='TKT', designation__contains='.énalité.').all()
        for modif in current_ticket_modif:
            tester = False
            for total in self.ajustment_total:
                if 'other_fee' in total:
                    if len(current_penalty) > 0:
                        for penalty in current_penalty:
                            if modif.total == (total['total'] + penalty.total):
                                total['other_fee'].other_fee_status = 0
                                total['other_fee'].save()
                                tester = True
                                break
                    else:
                        if modif.total == total['total']:
                            total['other_fee'].other_fee_status = 0
                            total['other_fee'].save()
                            tester = True
                            break
            if tester:
                break
                    
    
    # get all passengers's ticket fares
    def parseReceipt(self):
        parts = self.get_all_receipt_part()
        print('Parts')
        for temp in parts:
            print(temp)
        
        excluded_parts = self.get_all_excluded_part()
        print('Excluded parts')
        for temp in excluded_parts:
            print(temp)
        
        self.get_each_value()
        self.ajustment_total = []
                     
        