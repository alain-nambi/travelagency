'''
Created on 4 Oct 2022

@author: Famenontsoa
'''
import os
import traceback
from datetime import datetime

import AmadeusDecoder.utilities.configuration_data as configs

from AmadeusDecoder.models.pnr.Passenger import Passenger
from AmadeusDecoder.models.pnrelements.PnrAirSegments import PnrAirSegments
from AmadeusDecoder.models.pnrelements.Airport import Airport
from AmadeusDecoder.models.pnrelements.Airline import Airline
from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.TicketPassengerTST import TicketPassengerTST
from AmadeusDecoder.models.invoice.TicketPassengerSegment import TicketPassengerSegment
from AmadeusDecoder.models.data.RawData import RawData

# SPECIAL_AGENCY_CODE = ['PARFT278Z']
# PASSENGER_DESIGNATIONS = ['MR', 'MS', 'MRS', 'DR', 'ML', 'ADT', 'INF', 'YTH', 'MSTR']
# TST_IDENTIFIER = ["TST"]
# TICKET_IDENTIFIER = ["TKT"]
# COST_IDENTIFIER = ["FARE", "EQUIV", "GRAND", "TOTAL"]

SPECIAL_AGENCY_CODE = configs.SPECIAL_AGENCY_CODE
PASSENGER_DESIGNATIONS = configs.PASSENGER_DESIGNATIONS
TST_IDENTIFIER = configs.TST_IDENTIFIER
TICKET_IDENTIFIER = configs.TICKET_IDENTIFIER
COST_IDENTIFIER = configs.COST_IDENTIFIER
TST_FARE_IDENTIFIER = configs.TST_FARE_IDENTIFIER
TST_FARE_EQUIV_IDENTIFIER = configs.TST_FARE_EQUIV_IDENTIFIER
TST_TOTAL_IDENTIFIER = configs.TST_TOTAL_IDENTIFIER
TST_GRAND_TOTAL_IDENTIFIER = configs.TST_GRAND_TOTAL_IDENTIFIER

class PnrCostParser():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    # extract passenger
    def get_passenger_tst(self, content):
        passenger_line = []
        order_line = []
        passengers = []
        # tst_elements = ['FV', 'FM', 'FT', 'FP', 'FE', 'FO']
        # remove other line but passenger's
        new_content = []
        start_index = 0
        for i in range(len(content)):
            if content[i].split(".")[0].isnumeric() and len(content[i].split(".")) > 1:
                start_index = i
                break
        
        for i in range(start_index, len(content)):
            if content[i].split(".")[0].isnumeric() and len(content[i].split(".")) > 1:
                new_content.append(content[i])
            else:
                break
            
        content = new_content
               
        # fetch all lines containing passengers
        for i in range(len(new_content)):
            temp_content_space_split = new_content[i].split("  ")
            temp_content_dot_split = new_content[i].split(".")
            # if all passengers are on the same line
            if(len(temp_content_space_split) > 1 and temp_content_dot_split[0].isnumeric() and temp_content_dot_split[0] != '0'):
                for temp in temp_content_space_split:
                    passenger_line.append(temp.split(".")[1])
                    order_line.append(temp.split(".")[0].strip())
            # if passengers are on different lines
            else:
                if(temp_content_dot_split[0].isnumeric() and temp_content_dot_split[0] != '0'):
                    passenger_line.append(temp_content_dot_split[1])
                    order_line.append(temp_content_dot_split[0].strip())
        
        order = 0
        for line in passenger_line:
            all_designation = PASSENGER_DESIGNATIONS
            temp_passenger = Passenger()
            line_split = line.split('(')
            line_space_split = line.split(' ')
            '''
            # possible type
            1.BATROLO/MATHIS KYLIAN MR(CHD/02APR12)
            1.BARRAUD/SALMA(CHD/25AUG17)   2.MOINDANDZE/BARAKA MS
            1.MKOUBOI/FATIMA MRS(INFABDOU/NOLAN/24APR21)
            1.JEANMAIRE/PHILIPPE MR(ADT)
            1.CHAQUIR/EMILIE MS(ADT)(INFMAOULIDA/HAYDEN/10MAR22)
            '''
            # if the passenger is a child
            if len(line_split) > 1 and (line.find('CHD') > 0 or line.find('YTH') > 0 or line.find('CNN') > 0):
                name_part = line_split[0]
                designation_part = line_split[1]
                
                temp_passenger.name = name_part.split("/")[0].strip()
                if len(name_part.split('/')) > 1:
                    # if the passenger is a child but has MR, M., ...
                    if name_part.split(' ')[-1] in all_designation:
                        temp_passenger.surname = name_part.split("/")[1].removesuffix(name_part.split(' ')[-1]).strip()
                        temp_passenger.designation = name_part.split(' ')[-1]
                    # if the passenger is only a child
                    elif name_part.split(' ')[-1] not in all_designation:
                        temp_passenger.surname = name_part.split("/")[1].strip()
                        if line.find('CHD') > 0:
                            temp_passenger.designation = 'CHD'
                        elif line.find('YTH') > 0:
                            temp_passenger.designation = 'YTH'
                            temp_passenger.types = 'YTH'
                        elif line.find('CNN') > 0:
                            temp_passenger.designation = 'CNN'
                            temp_passenger.types = 'CNN'
                try:
                    temp_passenger.birthdate = datetime.strptime(designation_part.split("/")[1].split(")")[0], '%d%b%y')
                except:
                    pass
                    
            # if the passenger is not a child
            # if the passenger has ADT or YCD marked and not associated with an infant
            if len(line_split) > 1 and (line.find('ADT') > 0 or line.find('YCD') > 0 or line.find('STU') > 0) and line.find('INF') == -1:
                name_part = line_split[0]
                
                temp_passenger.name = name_part.split("/")[0]
                if len(name_part.split('/')) > 1:
                    if name_part.split(' ')[-1] in all_designation:
                        temp_passenger.surname = name_part.split("/")[1].removesuffix(name_part.split(' ')[-1]).strip()
                        temp_passenger.designation = name_part.split(' ')[-1]
                    else:
                        temp_passenger.surname = name_part.split("/")[1].strip()
                temp_passenger.types = 'ADT'
            # if the passenger is a simple passenger
            else:
                # if the passenger is not associated with an infant
                if line_space_split[-1] in all_designation or (line_space_split[-1] not in all_designation and len(line_split) == 1):
                    name_part = []
                    for temp_space_split in line_space_split:
                        if temp_space_split not in all_designation:
                            name_part.append(temp_space_split)
                    temp_passenger.name = name_part[0].split('/')[0].strip()
                    surname = ''
                    if len(name_part[0].split('/')) > 1:
                        surname += name_part[0].split('/')[1]
                    for i in range(1, len(name_part)):
                        surname += ' ' + name_part[i]
                    temp_passenger.surname = surname.strip()
                    if line_space_split[-1] in all_designation:
                        temp_passenger.designation = line_space_split[-1]
                # if the passenger is himself an infant
                elif len(line_split) > 1 and line_split[-1].removesuffix(')') == 'INF':
                    name_part = []
                    for temp_space_split in line_split:
                        if temp_space_split.removesuffix(')') not in all_designation:
                            name_part.append(temp_space_split)
                    temp_passenger.name = name_part[0].split('/')[0].strip()
                    surname = ''
                    if len(name_part[0].split('/')) > 1:
                        surname += name_part[0].split('/')[1]
                    for i in range(1, len(name_part)):
                        surname += ' ' + name_part[i]
                    temp_passenger.surname = surname.strip()
                    if line_split[-1].removesuffix(')') in all_designation:
                        temp_passenger.designation = line_split[-1].removesuffix(')')
                # if the passenger is associated with an infant
                elif len(line_split) > 1 and line.find('INF') > 0:
                    temp_passenger_inf = Passenger()
                    name_part = line_split[0]
                    temp_passenger.name = name_part.split('/')[0].strip()
                    
                    if len(name_part.split('/')) > 1:
                        if name_part.split(' ')[-1] in all_designation:
                            temp_passenger.surname = name_part.split('/')[1].removesuffix(name_part.split(' ')[-1]).strip()
                            temp_passenger.designation = name_part.split(' ')[-1]
                        else:
                            temp_passenger.surname = name_part.split('/')[1].strip()
                    
                    # Not having adult or youth flag
                    # 1.MKOUBOI/FATIMA MRS(INFABDOU/NOLAN/24APR21)
                    if line.find('ADT') == -1 and line.find('YTH') == -1:
                        inf_part = line_split[1]
                    # Has adult or youth flag
                    # 1.CHAQUIR/EMILIE MS(ADT)(INFMAOULIDA/HAYDEN/10MAR22)
                    else:
                        inf_part = line_split[2]
                    
                    inf_part_split = inf_part.split('/')
                    temp_passenger_inf.name = inf_part_split[0].removeprefix('INF').strip()
                    if len(inf_part_split) > 1:
                        temp_passenger_inf.surname = inf_part_split[1].strip().removesuffix(')')
                    if len(inf_part_split) > 2:
                        try:
                            temp_passenger_inf.birthdate = datetime.strptime(inf_part_split[2].split(")")[0], '%d%b%y')
                        except:
                            pass
                    temp_passenger_inf.designation = 'INF'
                    temp_passenger_inf.types = 'INF_ASSOC'
                    temp_passenger_inf.order = 'P' + str(order_line[order])
                    passengers.append(temp_passenger_inf)
                                
            temp_passenger.order = 'P' + str(order_line[order])
            passengers.append(temp_passenger)
            order += 1
        
        return passengers
    
    # removing space from string array
    def remove_space(self, string_array):
        ans = []
        for temp in string_array:
            if temp != '':
                ans.append(temp)
        return ans
    
    # get header
    def get_header_info(self, content):
        header_line = []
        for temp in content:
            if 'OD' in temp.split(' ') and temp.startswith(TST_IDENTIFIER[0]):
                header_line = self.remove_space(temp.split(' '))
                break
        
        tst_number = header_line[0]
        origin = header_line[-1][0:3]
        destination = header_line[-1][3:]
        
        return tst_number, origin, destination
    
    # update ticket status for ticket issued outside current travel agency
    def update_status_outside(self, ticket):
        if ticket.is_issued_outside:
            ticket.ticket_status = 1
    
    # format airsegments from segment_line
    def format_airsegments(self, segment_line, passengers):
        air_segments = []
        i = 0
        while i < len(segment_line) - 1:
            temp_pnr_aisegment = PnrAirSegments()
            temp_space_free_line = self.remove_space(segment_line[i].split(' '))
            next_space_free_line = self.remove_space(segment_line[i + 1].split(' '))
            
            if temp_space_free_line[1] != 'O' and temp_space_free_line[1] != 'X' and 'ARNK' not in temp_space_free_line:
                temp_origin = temp_space_free_line[1] 
                try:
                    temp_airline_code = temp_space_free_line[2] 
                    temp_flight_number = temp_space_free_line[3]
                    temp_flight_class = temp_space_free_line[4]
                    departure_date_time = temp_space_free_line[5] + '2023' + ' ' + temp_space_free_line[6] + '00'
                except:
                    print('Index out of range')
            elif temp_space_free_line[1] == 'O' or temp_space_free_line[1] == 'X':
                temp_origin = temp_space_free_line[2]
                try:
                    temp_airline_code = temp_space_free_line[3]
                    temp_flight_number = temp_space_free_line[4] 
                    temp_flight_class = temp_space_free_line[5] 
                    departure_date_time = temp_space_free_line[6] + '2023' + ' ' + temp_space_free_line[7] + '00'
                except:
                    print('Index out of range')
            elif 'ARNK' in temp_space_free_line:
                # 2   DZA    ARNK                                                               
                # 3 O RUN UU  975 V 16DEC 2100  OK VHWRTSM         07MAY      1PC  
                if next_space_free_line[1] == 'O' or next_space_free_line[1] == 'X':
                    temp_origin = temp_space_free_line[1]
                    try:
                        # the following information will be fetched from destination
                        temp_destination_dest = next_space_free_line[2]
                        dest_flight_no = next_space_free_line[4]
                        destination_departure_date_time = datetime.strptime(next_space_free_line[6] + '2023' + ' ' + next_space_free_line[7] + '00', '%d%b%Y %H%M%S')
                        # reduce error by adding passenger on search
                        temp_nearest_current_flight = None
                        temp_last_saved_destination_flight = None
                        for passenger in passengers:
                            temp_passenger_obj = Passenger.objects.filter(name=passenger.name, surname=passenger.surname).all()
                            for one_passenger_match in temp_passenger_obj:
                                temp_ticket_obj = Ticket.objects.filter(passenger=one_passenger_match).all()
                                for one_ticket_match in temp_ticket_obj:
                                    temp_last_saved_destination_flight = PnrAirSegments.objects.filter(codeorg=Airport.objects.filter(iata_code=temp_destination_dest).first(),
                                                                                                       departuretime=destination_departure_date_time,
                                                                                                       flightno=dest_flight_no, tickets__ticket=one_ticket_match).last()
                                    if temp_last_saved_destination_flight is not None:
                                        temp_nearest_current_flight = PnrAirSegments.objects.filter(codeorg=Airport.objects.filter(iata_code=temp_origin).first(),
                                                                                                    codedest=Airport.objects.filter(iata_code=temp_destination_dest).first(),
                                                                                                    pnr=temp_last_saved_destination_flight.pnr, 
                                                                                                    servicecarrier=temp_last_saved_destination_flight.servicecarrier).exclude(segmentorder=temp_last_saved_destination_flight.segmentorder).last()
                                        
                                    try:
                                        if temp_nearest_current_flight is not None:
                                            temp_airline_code = temp_nearest_current_flight.servicecarrier.iata
                                            temp_flight_number = temp_nearest_current_flight.flightno
                                            temp_flight_class = temp_nearest_current_flight.flightclass
                                            departure_date_time = str(temp_nearest_current_flight.departuretime)
                                            break
                                    except:
                                        print("Error when parsing 'ARNK'")
                            #     else:
                            #         continue
                            #     break
                            # else:
                            #     continue
                            # break
                    except:
                        print("Error when parsing 'ARNK'")
                    
            if i == len(segment_line) - 2:
                temp_destination = next_space_free_line[0]
            else:
                if (next_space_free_line[1] != 'O' and next_space_free_line[1] != 'X') or 'ARNK' in next_space_free_line:
                    temp_destination = next_space_free_line[1]
                else:
                    temp_destination = next_space_free_line[2]
            
            # departure time
            try:
                temp_pnr_aisegment.departuretime = datetime.strptime(departure_date_time, '%d%b%Y %H%M%S')
            except:
                print('Date format invalid')
            
            temp_pnr_aisegment.codeorg = Airport.objects.filter(iata_code=temp_origin).first()
            temp_pnr_aisegment.codedest = Airport.objects.filter(iata_code=temp_destination).first()
            temp_pnr_aisegment.servicecarrier = Airline.objects.filter(iata=temp_airline_code).first()
            temp_pnr_aisegment.flightno = temp_flight_number
            
            if air_segments:
                tester = True
                for tester_segment in air_segments:
                    if tester_segment.flightno == temp_pnr_aisegment.flightno and \
                        tester_segment.departuretime == temp_pnr_aisegment.departuretime and \
                        tester_segment.arrivaltime == temp_pnr_aisegment.arrivaltime:
                        tester = False
                        break
                if tester:
                    air_segments.append(temp_pnr_aisegment)
            else:
                air_segments.append(temp_pnr_aisegment)
                
            i += 1
        
        return air_segments, temp_flight_class
    
    # get air segments
    def get_air_segment_tst(self, content, passengers):
        segment_line = []
        
        last_index = 0
        for i in range(len(content)):
            temp_content_split = content[i].split(' ')
            if temp_content_split[0].isnumeric() and len(temp_content_split) > 1:
                segment_line.append(content[i])
                last_index = i
        segment_line.append(content[last_index + 1])
        return self.format_airsegments(segment_line, passengers)
    
    # get fares
    def get_fares_tst(self, content):
        fare = 0
        total = 0
        
        for temp in content:
            space_free_temp = self.remove_space(temp.split(' '))
            if len(space_free_temp) > 0:
                # FARE
                if space_free_temp[0] == TST_FARE_IDENTIFIER[0]:
                    for element in space_free_temp:
                        if element.split('.')[0].isnumeric():
                            fare = float(element)
                            break
                # FARE EQUIV
                # when foreign currency has been used
                if space_free_temp[0] == TST_FARE_EQUIV_IDENTIFIER[0]:
                    for element in space_free_temp:
                        if element.split('.')[0].isnumeric():
                            fare = float(element)
                            break
                # elif space_free_temp[0] == COST_IDENTIFIER[2] and space_free_temp[1] == COST_IDENTIFIER[3]:
                elif space_free_temp[0] == TST_TOTAL_IDENTIFIER[0]:
                    for element in space_free_temp:
                        if element.split('.')[0].isnumeric():
                            total = float(element)
                            break
        
        tax = total - fare
        if total < fare:
            tax = 0
            fare = total
            
        return fare, tax, total
    
    # get related pnr
    def get_tst_related_pnr(self, passengers, air_segments):
        queries = []
        for segment in air_segments:
            pnr = Pnr.objects.filter(segments__codeorg=segment.codeorg, segments__codedest=segment.codedest, segments__servicecarrier=segment.servicecarrier, segments__flightno=segment.flightno)
            if segment.departuretime is not None:
                departuretime = segment.departuretime
                try:
                    # pnr = pnr.filter(segments__departuretime__day=departuretime.day, segments__departuretime__month=departuretime.month, segments__departuretime__hour=departuretime.hour, segments__departuretime__minute=departuretime.minute)
                    pnr = pnr.filter(segments__departuretime__day=departuretime.day, segments__departuretime__month=departuretime.month)
                except:
                    print('Filter by date failed.')
            pnr = pnr.filter(segments__air_segment_status=1)
            queries.append(pnr)
        
        for passenger in passengers:
            pnr = Pnr.objects.filter(passengers__passenger__name=passenger.name, passengers__passenger__surname=passenger.surname, passengers__passenger__designation=passenger.designation)
            queries.append(pnr)
        
        single_query = queries[0]
        for i in range(1, len(queries)):
            single_query = single_query.intersection(queries[i])
            
        return single_query.first()
    
    # save tst to ticket table
    def save_tst(self, content):
        passengers = self.get_passenger_tst(content)
        air_segments, flight_class = self.get_air_segment_tst(content, passengers)
        pnr = self.get_tst_related_pnr(passengers, air_segments)
        fare, tax, total = self.get_fares_tst(content)
        tst_number = self.get_header_info(content)[0]
        
        tickets = []
        order = 1
        # ticket = None
        
        try:
            if pnr is not None:     
                for passenger in passengers:
                    ticket = Ticket()
                    ticket_number = tst_number + '-' + str(order)
                    temp_ticket = Ticket.objects.filter(pnr=pnr, number=ticket_number).first()
                    temp_passenger = Passenger.objects.filter(passenger__pnr=pnr, name=passenger.name, surname=passenger.surname).first()
                    temp_ticket = Ticket.objects.filter(pnr=pnr, passenger=temp_passenger, ticket_type=TST_IDENTIFIER[0], number=ticket_number).first()
                    
                    ticket.pnr = pnr
                    ticket.transport_cost = fare
                    ticket.fare = fare
                    ticket.tax = tax
                    ticket.total = total
                    ticket.flightclass = flight_class
                    ticket.ticket_type = TST_IDENTIFIER[0]
                    ticket.number = ticket_number
                    ticket.passenger = temp_passenger
                    
                    if temp_ticket is not None:
                        temp_ticket.passenger = temp_passenger
                        temp_ticket.fare = fare
                        temp_ticket.tax = tax
                        temp_ticket.total = total
                        ticket = temp_ticket
                    
                    # if PNR has been emitted
                    if pnr.status_value == 0:
                        ticket.ticket_status = 0
                    
                    # save the tst
                    ticket.save()
                    
                    # Ticket passenger TST
                    temp_tst_passenger_checker = TicketPassengerTST.objects.filter(ticket=ticket, passenger=temp_passenger).first()
                    if temp_tst_passenger_checker is None:
                        temp_ticket_passenger_tst = TicketPassengerTST()
                        temp_ticket_passenger_tst.ticket = ticket
                        temp_ticket_passenger_tst.passenger = temp_passenger
                        temp_ticket_passenger_tst.save()
                    
                    # Ticket Passenger Segment
                    for segment in air_segments:
                        temp_ticket_passenger_segment = TicketPassengerSegment()
                        temp_segment = PnrAirSegments.objects.filter(pnr=pnr, codeorg=segment.codeorg, codedest=segment.codedest, servicecarrier=segment.servicecarrier, flightno=segment.flightno, air_segment_status=1).first()
                        temp_tst_segment_checker = TicketPassengerSegment.objects.filter(ticket=ticket, segment=temp_segment).first()
                        if temp_tst_segment_checker is None:
                            temp_ticket_passenger_segment.ticket = ticket
                            temp_ticket_passenger_segment.segment = temp_segment
                            temp_ticket_passenger_segment.save()
                    
                    tickets.append(ticket)
                    order += 1
                    
                    # save raw data
                    try:
                        RawData().save_raw_data(content, pnr, ticket)
                    except:
                        with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea (TST)) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
            else:
                raise Exception('No PNR matches this TST')
        except:
            traceback.print_exc()
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.now()))
                error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                traceback.print_exc(file=error_file)
                error_file.write('\n')
        
        return tickets
    
    # parse tst
    def parse_tst(self, content):
        tickets = self.save_tst(content)
        try:
            if len(tickets) > 0:    
                # update TKT if current TST matches
                for ticket in tickets:
                    temp_passenger_obj = ticket.passenger
                    temp_passenger_tst = TicketPassengerTST.objects.filter(passenger__id=temp_passenger_obj.id, ticket__number=ticket.number).all()
                    if len(temp_passenger_tst) == 1:
                        tst_ticket_segment = TicketPassengerSegment.objects.filter(ticket__id=ticket.id).all()
                        ticket_segment = TicketPassengerSegment.objects.filter(segment__id=tst_ticket_segment[0].segment.id, ticket__ticket_type=TICKET_IDENTIFIER[0], ticket__passenger=temp_passenger_obj).last()
                        if ticket_segment is not None:
                            temp_ticket = Ticket.objects.filter(id=ticket_segment.ticket.id).first()
                            if temp_ticket is not None:
                                temp_ticket.fare_type = 'F'
                                temp_ticket.transport_cost = ticket.transport_cost
                                temp_ticket.tax = ticket.tax
                                temp_ticket.total = ticket.total
                                temp_ticket.state = 0
                                if ticket.total == 0 and ticket.transport_cost == 0:
                                    temp_ticket.is_no_adc = True
                                if ticket.transport_cost == 0 and ticket.total > 0:
                                    temp_ticket.is_prime = True
                                print("_______ TST fare not matching ________")
                                # PBDZDI : TST fare not matching
                                # We always set total as the real cost
                                # Here we have a total greater than 0 so, we update the transport cost to equal to total
                                if ticket.total > 0 and ticket.transport_cost == 0 and ticket.tax == 0:
                                    temp_ticket.transport_cost = temp_ticket.total
                                
                                print("TST Checking...")  
                                print(f"{temp_ticket} {temp_ticket.transport_cost} {temp_ticket.tax} {temp_ticket.total}")
                                print(f"{ticket.transport_cost} {ticket.tax} {ticket.total}")  
                                
                                # 01 Mars 2024
                                # TMEX5V : TST fare not matching transport cost is greater that big total
                                # vérifier si le total du ticket est égal à zéro et que soit le coût de transport, soit la taxe, soit la somme du coût de transport et de la taxe est supérieure au total du ticket
                                if ticket.total == 0 and (ticket.transport_cost >= 0 or ticket.tax >= 0 or ticket.transport_cost + ticket.tax > ticket.total):
                                    temp_ticket.transport_cost = 0
                                    temp_ticket.tax = 0
                                    temp_ticket.total = 0
                                
                                # special agency processing
                                # if temp_ticket.issuing_agency is not None:
                                #     if temp_ticket.issuing_agency.code in SPECIAL_AGENCY_CODE:
                                #         temp_ticket.tax = ticket.tax + 10
                                #         temp_ticket.total = ticket.total + 10
                                # update ticket status based on is_issued_outside status
                                self.update_status_outside(temp_ticket)
                                # save ticket with cost
                                temp_ticket.save()
                                # update pnr state
                                temp_ticket.update_pnr_state(temp_ticket.pnr)
                    
                    # update t_pnr ticket missing status
                    ticket.pnr.update_tst_missing_status()            
        except:
            traceback.print_exc()
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.now()))
                error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                traceback.print_exc(file=error_file)
                error_file.write('\n')
        
