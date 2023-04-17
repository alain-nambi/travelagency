'''
Created on 3 Feb 2023

@author: Famenontsoa
'''
import decimal
import traceback
from datetime import datetime

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.TicketPassengerSegment import TicketPassengerSegment,\
    OtherFeeSegment
from AmadeusDecoder.models.invoice.Fee import OthersFee
from AmadeusDecoder.models.user.Users import User

_PAYMENT_OPTIONS_ = ['Comptant', 'En compte']
_TICKET_NUMBER_PREFIX_ = ['Echange billet', 'EMD']
_TO_BE_EXCLUDED_KEY_KEYWORDS_ = ['Encaissement transaction', 'Encaissement Modification', 'Encaissement des suppléments']
_AIRPORT_AGENCY_CODE_ = ['DZAUU000B']
_STARTED_PROCESS_DATE_ = datetime(2023, 1, 1, 0, 0, 0, 0).date()

class ZenithParserReceipt():
    '''
    classdocs
    '''


    def __init__(self, content):
        '''
        Constructor
        '''
        self.content = content
    
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
            for keyword in _TO_BE_EXCLUDED_KEY_KEYWORDS_:
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
    
    # get each part by type
    def get_parts_by_type(self, receipt_parts, part_type):
        part_types = []
        for part in receipt_parts:
            if part_type in part:
                part_types.append(part)
        return part_types
     
    # check if part has been issued by current Travel Agency
    def check_part_emitter(self, current_part):
        is_emitted = False
        if current_part[1].find("ISSOUFALI") > -1 or current_part[1].find("Issoufali") > -1 or current_part[2].find("ISSOUFALI") > -1 or current_part[1].find("Issoufali") > -1:
            return True
        
        # check agent
        if len(current_part[1].split('.')) > 1:
            temp_user = User.objects.filter(username__iexact=current_part[1].split('.')[1].capitalize()).first()
            if temp_user is not None:
                return True
        
        return is_emitted
    
    # get target part index
    def get_target_part_index(self, current_part, target):
        for i in range(len(current_part)):
            if current_part[i].strip() == target:
                return i
        return 0
    
    # get target part index: find target inside strings
    def get_target_part_index_extended(self, current_part, target):
        for i in range(len(current_part)):
            if (current_part[i].find(target.capitalize()) > -1 or current_part[i].find(target) > -1):
                return i
        return 0
    
    # get passenger assigned on part
    def get_passenger_assigned_on_part(self, passengers, current_part):
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
                    elif temp_part.split(']')[0].strip() == passenger.name:
                        passenger_name += temp_part.split(']')[0]
                        break
            if current_part[i].strip() in _PAYMENT_OPTIONS_:
                next_index = i
        
        for passenger in passengers:
            if passenger_name.strip() == passenger.name:
                part_passenger = passenger
        
        if part_passenger is None:
            part_passenger = passengers[0]
            
        return part_passenger, next_index
    
    # get ticket/emd number assigned on part
    def get_ticket_emd_number_on_part(self, current_part):
        ticket_number = None
        for i in range(len(current_part)):
            element = current_part[i]
            for prefix in _TICKET_NUMBER_PREFIX_:
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
            for segment in air_segments:
                for temp_part in temp_part_split:
                    if temp_part.split('>')[0].removeprefix('[').removesuffix(']').find(segment.codeorg.iata_code) > -1 and temp_part != '':
                        return segment
                    
            if current_part[i].find("Aller Retour"):
                segment = []
                for temp in air_segments:
                    segment.append(temp)
                return segment
        return None
    
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
    
    # fee subjection status
    def check_fee_subjection_status(self, date_time, current_segment, pnr, ticket, other_fee):
        emitter = pnr.get_emit_agent()
        tester = False
        segment_departuretime = None
        if emitter is not None:
            if isinstance(current_segment, list):
                for segment in current_segment:
                    segment_departuretime = segment.departuretime
                    if emitter.office.code in _AIRPORT_AGENCY_CODE_ and segment_departuretime is not None:
                        if segment_departuretime.date() == date_time.date():
                            tester = True
                            break
            else:
                segment_departuretime = current_segment.departuretime
                if emitter.office.code in _AIRPORT_AGENCY_CODE_ and segment_departuretime is not None:
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
        if date_time < _STARTED_PROCESS_DATE_:
            is_flown = True
        return is_flown
    
    # ticket payment handling
    # When costs and taxes are not found on the original PNR
    def handle_ticket_payment(self, pnr, passengers, payment_part):
        for part in payment_part:
            date_time = self.get_issuing_date_on_part(part)
            current_passenger, next_index = self.get_passenger_assigned_on_part(passengers, part)
            is_created_by_us = self.check_part_emitter(part)
            
            tickets = Ticket.objects.filter(pnr=pnr, passenger=current_passenger).all()
            try:
                payment_option = part[next_index]
                for ticket in tickets:
                    ticket.payment_option = payment_option
                    if ticket.total == 0:
                        ticket.total = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                        ticket.transport_cost = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.')) - ticket.tax
                        ticket.issuing_date  = date_time.date()
                    if not is_created_by_us or self.check_issuing_date(date_time.date()) or (pnr.system_creation_date.date() > date_time.date() and self.check_is_invoiced_status(ticket, None)):
                        ticket.state = 0
                        ticket.ticket_status = 3
                    ticket.save()
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
            current_passenger, next_index = self.get_passenger_assigned_on_part(passengers, part)
            # new ticket to be inserted
            new_ticket = Ticket()
            new_ticket.passenger = current_passenger
            new_ticket.pnr = pnr
            is_created_by_us = self.check_part_emitter(part)
            # make current tickets as flown
            temp_ticket = Ticket.objects.filter(pnr=pnr, passenger=current_passenger, ticket_type='TKT').order_by('-id').first()
            ticket_segments = []
            if temp_ticket is not None:
                if self.check_is_invoiced_status(temp_ticket, None):
                    temp_ticket.ticket_status = 3
                    temp_ticket.save()
                # get old ticket segments
                ticket_segments = temp_ticket.ticket_parts.all()
                            
            # get adjustment
            # for element in part:
            #     for prefix in _TICKET_NUMBER_PREFIX_:
            #         if element.startswith(prefix):
            #             new_ticket.number = element.removeprefix(prefix).strip().removeprefix('[').removesuffix(']').removeprefix(':')
            new_ticket.number = self.get_ticket_emd_number_on_part(part)
            
            if new_ticket.number is not None:
                if not is_created_by_us or self.check_issuing_date(date_time.date()):
                #or (pnr.system_creation_date.date() > date_time.date()):
                    new_ticket.ticket_status = 3
                # check if it has been already saved
                ticket_saved_checker = Ticket.objects.filter(number=new_ticket.number, pnr=pnr).first()
                if ticket_saved_checker != None:
                    new_ticket = ticket_saved_checker
                    if is_created_by_us:
                        new_ticket.ticket_status = 1
                    if ((pnr.system_creation_date.date() > date_time.date()) and self.check_is_invoiced_status(new_ticket, None)) or self.check_issuing_date(date_time.date()):
                        new_ticket.ticket_status = 3
                        
                try:
                    new_ticket.transport_cost = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                    new_ticket.tax = 0
                    new_ticket.total = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                except:
                    pass
                
                if new_ticket.total == 0:
                    new_ticket.is_no_adc = True
                    new_ticket.tax = 0
                    
                new_ticket.ticket_type = 'TKT'
                new_ticket.issuing_date = date_time
                new_ticket.emitter = pnr.agent
                new_ticket.save()
                if ticket_saved_checker is None:
                    for segment in ticket_segments:
                        ticket_segment = TicketPassengerSegment()
                        ticket_segment.ticket = new_ticket
                        ticket_segment.segment = segment.segment
                        ticket_segment.save()
    
    # emd cancellation
    def handle_emd_cancellation(self, pnr, passengers, cancellation_part):
        for part in cancellation_part:
            date_time = self.get_issuing_date_on_part(part)
            current_passenger, next_index = self.get_passenger_assigned_on_part(passengers, part)
            current_segment = self.get_segments_assigned_on_part(part)
            # new emd to be inserted
            new_emd = OthersFee()
            new_emd.pnr = pnr
            part_name_index = self.get_target_part_index(part, "Annulation ancillaries")
            if part_name_index is not None:
                new_emd.designation = part[part_name_index + 1]
            
            is_created_by_us = self.check_part_emitter(part)
            
            # make current other_fee as flown
            temp_emd = Ticket.objects.filter(pnr=pnr, passenger=current_passenger, ticket_type='EMD').order_by('-id').first()
            if temp_emd is not None:
                if self.check_is_invoiced_status(temp_emd, None):
                    temp_emd.ticket_status = 3
                    temp_emd.save()
            
            temp_other_fees = OthersFee.objects.filter(pnr=pnr, related_segments__passenger=current_passenger).all()
            for other_fee in temp_other_fees:
                if self.check_is_invoiced_status(None, other_fee):
                    other_fee.other_fee_status = 3
                    other_fee.save()
                
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
                    if (pnr.system_creation_date.date() > date_time.date()) and self.check_is_invoiced_status(otherfee_saved_checker, None):
                        otherfee_saved_checker.other_fee_status = 3
                if not is_created_by_us or self.check_issuing_date(date_time.date()):
                    new_emd.other_fee_status = 3
                new_emd.fee_type = 'Cancellation'
                new_emd.save()
                if otherfee_saved_checker is None:
                    other_fee_passenger_segment = OtherFeeSegment()
                    other_fee_passenger_segment.other_fee = new_emd
                    other_fee_passenger_segment.passenger = current_passenger
                    other_fee_passenger_segment.segment = current_segment[0]
                    other_fee_passenger_segment.save()
    
    # emd when no ticket number provided
    def handle_emd_no_number(self, pnr, current_passenger, current_segment, is_created_by_us, cost, total, date_time, emd_single_part):
        designation_index = self.get_target_part_index_extended(emd_single_part, 'bagage')
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
            otherfee_saved_checker = OthersFee.objects.filter(designation=new_emd.designation, pnr=pnr, related_segments__passenger=current_passenger).first()
            if otherfee_saved_checker != None:
                new_emd = otherfee_saved_checker
                if is_created_by_us:
                    new_emd.other_fee_status = 1
                if self.check_is_invoiced_status(None, otherfee_saved_checker):
                    new_emd.other_fee_status = 3
            if not is_created_by_us or self.check_issuing_date(date_time.date()):
                # or (pnr.system_creation_date.date() > date_time.date()):
                new_emd.other_fee_status = 3
            new_emd.fee_type = 'EMD'
            # check fee subjection
            try:
                self.check_fee_subjection_status(date_time, current_segment, pnr, None, new_emd)
            except:
                traceback.print_exc()
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
            current_passenger, next_index = self.get_passenger_assigned_on_part(passengers, part)
            current_segment = self.get_segments_assigned_on_part(part)
            part_name_index = self.get_target_part_index(part, "Pénalité")
            
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
                temp_emd = Ticket.objects.filter(pnr=pnr, passenger=current_passenger, ticket_type='EMD').order_by('-id').first()
                if temp_emd is not None:
                    if self.check_is_invoiced_status(temp_emd, None):
                        temp_emd.ticket_status = 3
                        temp_emd.save()
                
                temp_other_fees = OthersFee.objects.filter(pnr=pnr, related_segments__passenger=current_passenger, fee_type='EMD').all()
                print('TRANSPORT COST', OthersFee.objects.filter(pnr=pnr, related_segments__passenger=current_passenger, fee_type='EMD').query)
                for other_fee in temp_other_fees:
                    if self.check_is_invoiced_status(None, other_fee) or other_fee.cost == transport_cost:
                        other_fee.other_fee_status = 3
                        other_fee.save()
                
                # get emd
                # for element in part:
                #     for prefix in _TICKET_NUMBER_PREFIX_:
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
                        if self.check_is_invoiced_status(new_emd, None):
                            new_emd.ticket_status = 3
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
                        self.check_fee_subjection_status(date_time, current_segment, pnr, new_emd, None)
                    except:
                        traceback.print_exc()
                    new_emd.save()
                    if ticket_saved_checker is None:
                        if isinstance(current_segment, list):
                            for segment in current_segment:
                                ticket_segment = TicketPassengerSegment()
                                ticket_segment.ticket = new_emd
                                ticket_segment.segment = segment
                                ticket_segment.save()
                        else:
                            ticket_segment = OtherFeeSegment()
                            ticket_segment.ticket = new_emd
                            ticket_segment.segment = current_segment
                            ticket_segment.save()
                        
                else:
                    # handle EMD with no number
                    self.handle_emd_no_number(pnr, current_passenger, current_segment, is_created_by_us,  new_emd.transport_cost,  new_emd.total, date_time, part)
                    continue
            elif part_name_index > 0:
                # new emd to be inserted
                new_emd = OthersFee()
                new_emd.pnr = pnr
                if part_name_index is not None:
                    new_emd.designation = part[part_name_index + 1]
                
                is_created_by_us = self.check_part_emitter(part)
                
                # make current other_fee as flown
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
                        other_emd.save()
                
                # get penalty
                if new_emd.designation is not None:
                    try:
                        new_emd.cost = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                        new_emd.total = decimal.Decimal(part[next_index+1].split(' ')[0].replace(',','.'))
                    except:
                        pass
                    
                    if not is_created_by_us or self.check_issuing_date(date_time.date()):
                        new_emd.other_fee_status = 3
                    # check is it has been already saved
                    otherfee_saved_checker = OthersFee.objects.filter(designation=new_emd.designation, pnr=pnr, related_segments__passenger=current_passenger).first()
                    if otherfee_saved_checker != None:
                        new_emd = otherfee_saved_checker
                        if is_created_by_us:
                            new_emd.other_fee_status = 1
                        if self.check_is_invoiced_status(None, otherfee_saved_checker):
                            otherfee_saved_checker.other_fee_status = 3
                    new_emd.fee_type = 'TKT'
                    new_emd.is_subjected_to_fee = False
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
        
    # get each value by type and value
    def get_each_value(self):
        receipt_parts = self.get_all_receipt_part()
        passengers = self.get_passengers()
        pnr = self.get_pnr()
        # get ticket payment
        # Marked with: "Paiement Billet"
        ticket_payment_parts = self.get_parts_by_type(receipt_parts, "Paiement Billet")
        self.handle_ticket_payment(pnr, passengers, ticket_payment_parts)
        
        # get ticket adjustment
        # Marked with: "Reissuance Adjustment"
        ticket_adjustment_part = self.get_parts_by_type(receipt_parts, "Reissuance Adjustment")
        self.handle_ticket_adjustment(pnr, passengers, ticket_adjustment_part)
        
        # emd cancellation
        # Marked with: "Annulation ancillaries"
        emd_cancellation_part = self.get_parts_by_type(receipt_parts, "Annulation ancillaries")
        self.handle_emd_cancellation(pnr, passengers, emd_cancellation_part)
        
        # emd
        # Marked with any other flags to signal EMD like "1er BAGAGE 23kg"
        for ticket_pay_part in ticket_payment_parts:
            receipt_parts.remove(ticket_pay_part)
        
        for ticket_adjust_part in ticket_adjustment_part:
            receipt_parts.remove(ticket_adjust_part)
            
        for emd_cancelled_part in emd_cancellation_part:
            receipt_parts.remove(emd_cancelled_part)
        self.handle_emd(pnr, passengers, receipt_parts)
    
    # get all passengers's ticket fares
    def parseReceipt(self):
        parts = self.get_all_receipt_part()
        for temp in parts:
            print(temp)
        
        self.get_each_value()
                     
        