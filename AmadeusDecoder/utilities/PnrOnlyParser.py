'''
Created on 10 Sep 2022

@author: Famenontsoa
'''
import decimal
import os
import pytz
import traceback
from datetime import datetime
from datetime import timedelta
from django.db import transaction

import AmadeusDecoder.utilities.configuration_data as configs

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.user.Users import Office
from AmadeusDecoder.models.pnr.Passenger import Passenger
from AmadeusDecoder.models.pnrelements.PnrAirSegments import PnrAirSegments
from AmadeusDecoder.models.pnrelements.Airline import Airline
from AmadeusDecoder.models.pnrelements.Airport import Airport
from AmadeusDecoder.models.pnr.Contact import Contact
from AmadeusDecoder.models.pnr.PnrPassenger import PnrPassenger
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.TicketPassengerSegment import TicketPassengerSegment
from AmadeusDecoder.models.pnrelements.SpecialServiceRequestBase import SpecialServiceRequestBase
from AmadeusDecoder.models.pnrelements.SpecialServiceRequestPassenger import SpecialServiceRequestPassenger
from AmadeusDecoder.models.pnrelements.SpecialServiceRequestSegment import SpecialServiceRequestSegment
from AmadeusDecoder.models.pnrelements.SpecialServiceRequest import SpecialServiceRequest
from AmadeusDecoder.models.invoice.TicketSSR import TicketSSR
from AmadeusDecoder.models.pnrelements.ConfirmationDeadline import ConfirmationDeadline
from AmadeusDecoder.models.pnrelements.Remark import Remark
from AmadeusDecoder.models.pnrelements.PnrRemark import PnrRemark
from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.models.data.RawData import RawData
from AmadeusDecoder.models.invoice.CustomerAddress import CustomerAddress


# PNR_IDENTIFIER = ["RP"]
# PNR_TYPE = ["Altea"]
# DUPLICATE_PNR_IDENTIFIER = ["* RR"]
# SPLIT_PNR_IDENTIFIER = ["* SP"]
# TO_BE_EXCLUDED_LINE = ["OPERATED BY", "ETA", "FOR TAX/FEE"]
# CONTACT_TYPES = ["AP", "APE", "APN"]
# CONTACT_TYPE_NAMES = {'AP':'Phone', 'APE':'Email', 'APN':'Notification contact'}
# TICKET_LINE_IDENTIFIER = ["FA", "FHE"]
# SECOND_DEGREE_TICKET_LINE_IDENTIFIER = ["PAX", "INF"]
# REMARK_IDENTIFIER = ['RM', 'RC', 'RIR', 'RX', 'RCF', 'RQ', 'RIA', 
#                                 'RIS', 'RIT', 'RIU', 'RIF', 'RII', 'RIZ']
# PASSENGER_DESIGNATIONS = ['MR', 'MS', 'MRS', 'DR', 'ML', 'ADT', 'INF', 'YTH', 'MSTR']
# POSSIBLE_COST_CURRENCY = ['EUR', 'MGA', 'USD', 'MUR']
# AM_H_LINE_IDENTIFIER = ["AM/H"]

PNR_IDENTIFIER = configs.PNR_IDENTIFIER
PNR_TYPE = configs.MAIN_PNR_TYPE
DUPLICATE_PNR_IDENTIFIER = configs.DUPLICATE_PNR_IDENTIFIER
SPLIT_PNR_IDENTIFIER = configs.SPLIT_PNR_IDENTIFIER
TO_BE_EXCLUDED_LINE = configs.TO_BE_EXCLUDED_LINE
CONTACT_TYPES = configs.CONTACT_TYPES
CONTACT_TYPE_NAMES = configs.CONTACT_TYPE_NAMES
TICKET_LINE_IDENTIFIER = configs.TICKET_LINE_IDENTIFIER
SECOND_DEGREE_TICKET_LINE_IDENTIFIER = configs.SECOND_DEGREE_TICKET_LINE_IDENTIFIER
REMARK_IDENTIFIER = configs.REMARK_IDENTIFIER
PASSENGER_DESIGNATIONS = configs.PNR_PASSENGER_DESIGNATIONS
POSSIBLE_COST_CURRENCY = configs.POSSIBLE_COST_CURRENCY
AM_H_LINE_IDENTIFIER = configs.AM_H_LINE_IDENTIFIER

class PnrOnlyParser():
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
    
    # get basic data from pnr
    def get_pnr_data(self, file_content, email_date):
        pnr = Pnr()
        is_saved = False
        current_pnr_emitter = None
        
        pnrDetailRow = ''
        for i in range(len(file_content)):
            if(file_content[i].startswith(PNR_IDENTIFIER[0])):
                pnrDetailRow = file_content[i]
                break
            
        # new method
        header_with_no_space = []
        for detail_row in pnrDetailRow.split(' '):
            if detail_row != '':
                header_with_no_space.append(detail_row)
        
        user_gds_id = None
        pnr.number = header_with_no_space[-1]
        try:
            copying_agent = pnr.get_pnr_creator_user_copying()
            if copying_agent is not None:
                pnr.agent = copying_agent
            elif copying_agent is None:
                user_gds_id = header_with_no_space[len(header_with_no_space) - 3].split('/')[0]
                user_agent = User.objects.filter(gds_id=user_gds_id).first()
                if user_agent is not None:
                    pnr.agent = user_agent  
                else:
                    raise Exception('No agent found')
        except:
            pnr.agent_code = user_gds_id
        
        creation_date = datetime.strptime(header_with_no_space[-2].split('/')[0].strip(), '%d%b%y').date()
        # system_creation_date = datetime.now()
        
        temp_pnr = Pnr.objects.filter(number=pnr.number).first()
        if temp_pnr is not None:
            # if temp_pnr.state == 1:
            #    is_saved = False
            #else:
            #    is_saved = True
            is_saved = True
            temp_pnr.gds_creation_date = creation_date
            # temp_pnr.system_creation_date = datetime(system_creation_date.year, system_creation_date.month, system_creation_date.day, system_creation_date.hour, system_creation_date.minute, system_creation_date.second, system_creation_date.microsecond, pytz.UTC)
            temp_pnr.system_creation_date = email_date
            # temp_pnr.state = 0
            if Office.objects.filter(code=pnrDetailRow.split('/')[1]).first() is None:
                Office.objects.create(code=pnrDetailRow.split('/')[1])
            temp_pnr.agency = Office.objects.get(code=pnrDetailRow.split('/')[1])
            
            copying_agent = pnr.get_pnr_creator_user_copying()
            if copying_agent is not None:
                temp_pnr.agent = copying_agent
            elif copying_agent is None:
                user_gds_id = header_with_no_space[len(header_with_no_space) - 3].split('/')[0]
                user_agent = User.objects.filter(gds_id=user_gds_id).first()
                if user_agent is not None:
                    temp_pnr.agent = user_agent  
                else:
                    temp_pnr.agent_code = user_gds_id 
            temp_pnr.is_read = False
            
            # current pnr emitter
            try:
                current_pnr_emitter = User.objects.filter(gds_id=header_with_no_space[len(header_with_no_space) - 3].split('/')[0]).first()
            except:
                print("Current PNR has no emitter found")
            
            return temp_pnr, is_saved, current_pnr_emitter
        
        pnr.gds_creation_date = creation_date
        # pnr.system_creation_date = datetime(system_creation_date.year, system_creation_date.month, system_creation_date.day, system_creation_date.hour, system_creation_date.minute, system_creation_date.second, system_creation_date.microsecond, pytz.UTC)
        pnr.system_creation_date = email_date
        pnr.type = PNR_TYPE[0]
        if Office.objects.filter(code=pnrDetailRow.split('/')[1]).first() is None:
            Office.objects.create(code=pnrDetailRow.split('/')[1])
        pnr.agency = Office.objects.get(code=pnrDetailRow.split('/')[1])
        pnr.is_read = False
        if pnr.agent is not None:
            current_pnr_emitter = pnr.agent
        return pnr, False, current_pnr_emitter
    
    # Check if regular pnr line: a regular one always start with a number followed by a blank space or a full stop'''
    def is_regular_line(self, line):
        regular = True
        if(line.split(".")[0].isnumeric() == False):
            if(line.split(" ")[0].isnumeric() == False):
                regular = False
        
        if len(line) < 3:
            regular = False
        
        return regular
    
    # find line number
    def find_line_number(self, line):
        line_number = 0
        if line.split(' ')[0].isnumeric():
            line_number = line.split(' ')[0]
        elif line.split('.')[0].isnumeric():
            line_number = line.split('.')[0]
        return int(line_number)
    
    # start content from appropriated point when passengers are grouped
    def appropriated_start(self, normalized_file):
        upper_content = []
        new_file_start = []
        for i in range(len(normalized_file)):
            current_line = normalized_file[i]
            if current_line.split('.')[0] == '0':
                upper_content = normalized_file[0:i+1]
                new_file_start = normalized_file[i+1:]
                break
        
        return upper_content, new_file_start
    
    # check if the current line is the next of the previous
    def logic_sequence(self, normalized_file):
        sequence_wise_file = []
        for i in range(len(normalized_file)):
            if not normalized_file[i].startswith(SPLIT_PNR_IDENTIFIER[0]) and not normalized_file[i].startswith(DUPLICATE_PNR_IDENTIFIER[0]):
                if i > 0 and i < len(normalized_file):
                    previous_line = normalized_file[i-1]
                    
                    previous_line_number = self.find_line_number(previous_line)
                    current_line_number = self.find_line_number(normalized_file[i])
                    
                    if current_line_number - previous_line_number < 6 and current_line_number - previous_line_number > 0:
                        sequence_wise_file.append(normalized_file[i])
                    else:
                        # sequence_wise_file[-1] = sequence_wise_file[-1] + normalized_file[i]
                        normalized_file[i - 1] = normalized_file[i - 1] + normalized_file[i]
                        
                        normalized_file.pop(i)
                        sequence_wise_file = normalized_file
                        self.logic_sequence(normalized_file)
                        break
                else:
                    sequence_wise_file.append(normalized_file[i])
            else:
                sequence_wise_file.append(normalized_file[i])
        
        return sequence_wise_file
    
    # Get normal file without irregular line breaks
    def normalize_file(self, needed_content):
        new_content = []
        for i in range(len(needed_content)):
            if self.is_regular_line(needed_content[i]):
                new_content.append(needed_content[i])
            elif not self.is_regular_line(needed_content[i]) and (needed_content[i].startswith(SPLIT_PNR_IDENTIFIER[0]) or needed_content[i].startswith(DUPLICATE_PNR_IDENTIFIER[0])) :
                new_content.append(needed_content[i])
            elif self.is_regular_line(needed_content[i]) == False and len(new_content) > 0:
                # discard excluded line
                is_excluded = False
                for line in TO_BE_EXCLUDED_LINE:
                    if needed_content[i].startswith(line):
                        is_excluded = True
                        break
                if not is_excluded:
                    new_content[len(new_content) - 1] = new_content[len(new_content) - 1] + needed_content[i]
        
        upper_content, new_file_start = self.appropriated_start(new_content)
        if len(upper_content) > 0:
            temp_content = self.logic_sequence(new_file_start)
            return upper_content + temp_content
        new_content = self.logic_sequence(new_content)
        return new_content
    
    # Fetch all contacts on a pnr
    def get_contacts(self, pnr_content):
        contacts = []
        all_contact_lines = []
        all_contact_types = CONTACT_TYPES
        all_types = CONTACT_TYPE_NAMES
        
        for content in pnr_content:
            if(len(content.split(" ")) > 1 and content.split(" ")[0].isnumeric() == True):
                # all phone contacts and email
                if(content.split(" ")[1] in all_contact_types):
                    all_contact_lines.append(content)
        
        for line in all_contact_lines:
            temp_contact = Contact()
            data_line = line.split(" ")
            temp_contact.contacttype = all_types[data_line[1]]
            contact_value = ''
            for value in data_line[2:]:
                contact_value += ' ' + value
            temp_contact.value = contact_value
            temp_contact.owner = ''
            
            contacts.append(temp_contact)
        
        return contacts
    
    # check pnr status: 'Emis' ou 'Non emis'
    def get_pnr_status(self, pnr, normalized_file):
        pnr_status = 'Non émis'
        pnr_status_value = 1
        
        for line in normalized_file:
            temp = line.split(" ")
            if len(temp) > 2 and temp[0].isnumeric() == True:
                # all phone contacts and email
                for identifier in TICKET_LINE_IDENTIFIER:
                    if temp[1].startswith(identifier):
                        pnr_status = 'Emis'
                        pnr_status_value = 0
                        break
                if pnr_status_value == 0:
                    break
        
        pnr.status = pnr_status
        pnr.status_value = pnr_status_value
        pnr.save()
    
    # check if pnr is duplicated or splitted
    def get_split_duplicated_status(self, pnr, normalized_file):
        split_lines = []
        children_pnr = []
        duplicate_lines = []
        parent_pnr = []
        
        for line in normalized_file:
            if line.startswith(SPLIT_PNR_IDENTIFIER[0]):
                split_lines.append(line)
            elif line.startswith(DUPLICATE_PNR_IDENTIFIER[0]):
                duplicate_lines.append(line)
        
        if len(split_lines) > 0:
            pnr.is_parent = True
            pnr.is_splitted = True
            for temp_split_line in split_lines:
                if len(temp_split_line.split('-')) > 1:
                    children_pnr.append(temp_split_line.split('-')[1])
            pnr.children_pnr = children_pnr
        
        if len(duplicate_lines) > 0:
            pnr.is_parent = True
            pnr.is_duplicated = True
            for temp_duplicate_line in duplicate_lines:
                if len(temp_duplicate_line.split('-')) > 1:
                    parent_pnr.append(temp_duplicate_line.split('-')[1])
            pnr.parent_pnr = parent_pnr
            
    # get all remarks on PNR
    def get_remarks(self, pnr, normalized_file):
        all_possible_remarks = REMARK_IDENTIFIER
        all_pnr_remarks = []
        remark_lines = []
        
        for line in normalized_file:
            temp = line.split(" ")
            if temp[0].isnumeric():
                if temp[1] in all_possible_remarks:
                    remark_lines.append(line)
        
        for remark in remark_lines:
            space_split = remark.split(' ')
            temp_pnr_remark = PnrRemark()
            temp_remark = Remark.objects.filter(code=space_split[1]).first()
            remark_text = ''
            if temp_remark is not None:
                for text in space_split[2:]:
                    remark_text += text + ' '
                temp_pnr_remark.pnr = pnr
                temp_pnr_remark.remark = temp_remark
                temp_pnr_remark.remark_text = remark_text[:-1]
                all_pnr_remarks.append(temp_pnr_remark)
        
        return all_pnr_remarks
        
    # Get passengers
    def get_passengers(self, pnr_content):
        passenger_line = []
        order_line = []
        passengers = []
        # fetch all lines containing passengers
        for i in range(len(pnr_content)):
            temp_content_space_split = pnr_content[i].split("  ")
            temp_content_dot_split = pnr_content[i].split(".")
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
                # if the passenger is associated with an infant
                if len(line_split) > 1 and line.find('INF') > 0:
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
 
    def is_leap_year(self, year):
        """
        Check if a given year is a leap year.
        """
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def transform_date(self, date_input):
        try:
            # Extract year, month, and day from the input string
            year, month, day = map(int, date_input.split('-'))
            
            # Create a datetime object
            date_object = datetime(year, month, day)
            
            # Get the day and month in the desired format (e.g., 29FEB)
            day_month_format = date_object.strftime('%d%b').upper()
            
            return day_month_format
        except ValueError:
            # Handle the case where the input date is invalid
            return None

    def compare_dates(self, date_operation, date_segment_flight):
        """
        RP/DZAUU01A3/DZAUU01A3            JM/GS  16DEC23/2259Z   PGUI8Z
        1.ABDOU HADJI/SAANDATI MRS
        ## segment de vol
        2  KQ 255 Y 16DEC 6 DZANBO         FLWN \n
        3  KQ 112 Y 16DEC 6 NBOCDG         FLWN \n
        4  KQ 115 L 29FEB 4 CDGNBO HK1       2E 1920 0525+1 *1A/E* \n
        5  KQ 254 L 01MAR 5 NBODZA HK1       1A 1210 1440   *1A/E*

        date_operation (str): date de création automatique du PNR (16DEC23)
        date_segment_flight (str): date du vol dans le segment
        compare_dates (function): comparer la date de l'opération et la date du vol
        """

        try:
            # Cast date to string 
            date_operation = str(date_operation)

            # Extract the year from the operation date
            year_operation = int(date_operation.split("-")[0])
            
            # Define the date format for comparison
            date_format_operation = "%Y-%m-%d"
            date_format_segment_flight = "%d%b"
            
            
            # ity code ity de mety hisy onana @ 2028 indray
            if date_segment_flight != "29FEB":
                # Show log usefull if an errors occured
                print(f"Date operation : {date_operation}")
                print(f"Date segment flight : {date_segment_flight}")

                # Convert date strings to datetime objects for comparison
                date_operation = datetime.strptime(date_operation, date_format_operation)
                date_segment_flight = datetime.strptime(date_segment_flight, date_format_segment_flight)
                
                # Extract the month from the datetime objects
                number_month_operation = date_operation.month
                number_month_segment_flight = date_segment_flight.month

                # Compare months
                if number_month_operation <= number_month_segment_flight:
                    return year_operation
                else:
                    return year_operation + 1
            else:
                # Handle the case where the flight date is "29FEB"
                while not self.is_leap_year(year_operation):
                    year_operation += 1
                return year_operation
        except ValueError as e:
            print("Erreur lors de la comparaison des dates :", e)
            return datetime.datetime.now().year

    
    # get all flight segments
    def get_flight(self, pnr_content, pnr):
        yearOfOperation = pnr.gds_creation_date.year
        month_of_operation = pnr.gds_creation_date.month
        
        all_flight_lines = []
        all_flight_order = []
        flights = []
        flight_class = None
        is_open_status = False
        
        for line in pnr_content:
            if(len(line.split(" ")) > 1 and line.split(" ")[0].isnumeric() == True):
                if(line.split(" ")[1] == '' or line.split(" ")[1].endswith('SVC')): # because flight line always start with the line number followed by a space
                    all_flight_lines.append(line)
                    all_flight_order.append(line.split(" ")[0])
        
        segment = 0
        for flight in all_flight_lines:
            flight_info = flight.split(" ")
            temp_flight = PnrAirSegments()
            print('FLIGHT INFO', flight_info)
            # Segment is a flight
            if not flight_info[1].endswith('SVC') and not flight_info[1].endswith('OPEN') \
                and not flight_info[2].endswith('OPEN') and not flight_info[1].endswith('ARNK') and not flight_info[2].endswith('ARNK'):
                flown_checker = False
                # if airline code and flight number are separated with space
                # eg: AF 234, SA 223
                if(len(flight.split(" ")[2]) <= 2):
                    airline_code = flight_info[2]
                    if len(flight_info[3]) <= 3:
                        flight_number = flight_info[3]
                        flight_class = flight_info[4]
                        departure_airport = flight_info[7][0:3]
                        landing_airport = flight_info[7][3:]
                        hk_sa_index = 8
                        departure_time_index = 5
                    else:
                        flight_number = flight_info[3][0:3]
                        flight_class = flight_info[3][3:]
                        departure_airport = flight_info[6][0:3]
                        landing_airport = flight_info[6][3:]
                        hk_sa_index = 7
                        departure_time_index = 4
                    hk_sa = None
                    if(flight_info[len(flight_info) - 1] == 'FLWN'):
                        flown_checker = True
                        temp_flight.segment_state = 1
                        departure_time = datetime.strptime(flight_info[departure_time_index] + str(yearOfOperation) + ' ' + '00:00:00', '%d%b%Y %H:%M:%S')
                        landing_time = None
                    else:
                        hk_sa = flight_info[hk_sa_index]
                        # to loop the line from the last
                        index = len(flight_info) - 1
                        a = index
                        departure = ''
                        landing = ''
                        # almost all segment line ends with element like:  *1A/E* ,... 
                        # notice format: *...*
                        if(flight_info[a].startswith('*') or flight_info[a].endswith('*')):
                            while a >= 0:
                                if(flight_info[a - 1] != ''):
                                    departure = flight_info[a - 2]
                                    landing = flight_info[a - 1]
                                    break
                                a -= 1
                        else:
                            # some segment line does not follow this convention (*...*)
                            while a >= 0:
                                if flight_info[a-1] != '':
                                    if flight_info[a-1].isnumeric() and len(flight_info[a-1]) == 4:
                                        departure = flight_info[a-2]
                                        landing = flight_info[a-1]
                                        break
                                a -= 1

                        print("CORRECT YEAR OF OPERATION")
                        correct_year_of_operation = self.compare_dates(date_operation=pnr.gds_creation_date, date_segment_flight=flight_info[departure_time_index])
                        print(correct_year_of_operation)

                        departure_time = datetime.strptime(flight_info[departure_time_index] + str(correct_year_of_operation) + ' ' + departure[0:2] + ':' + departure[2:] + ':00', '%d%b%Y %H:%M:%S')
                        # sometimes, landing time has a '+' attribute in order to show that some days has to be added from the departure date
                        if(len(landing.split('+')) <= 1):
                            landing_time = datetime.strptime(flight_info[departure_time_index] + str(correct_year_of_operation) + ' ' + landing[0:2] + ':' + landing[2:] + ':00', '%d%b%Y %H:%M:%S')
                        else:
                            try:
                                landing_time = datetime.strptime(flight_info[departure_time_index] + str(correct_year_of_operation) + ' ' + landing.split('+')[0][0:2] + ':' + landing.split('+')[0][2:] + ':00', '%d%b%Y %H:%M:%S') + timedelta(days=int(landing.split('+')[1]))
                            except:
                                landing_time = None
                # if airline code and flight number are not separated with space
                # eg: AF6234, SA1223
                if(len(flight.split(" ")[2]) > 2):
                    airline_code = flight_info[2][0:2]
                    # flight_number = flight_info[2][2:]
                    # flight_class = flight_info[3]
                    # departure_airport = flight_info[6][0:3]
                    # landing_airport = flight_info[6][3:]
                    
                    if len(flight_info[2][2:]) <= 4:
                        flight_number = flight_info[2][2:]
                        flight_class = flight_info[3]
                        departure_airport = flight_info[6][0:3]
                        landing_airport = flight_info[6][3:]
                        hk_sa_index = 7
                        departure_time_index = 4
                    else:
                        flight_number = flight_info[2][2:6]
                        flight_class = flight_info[2][6:]
                        departure_airport = flight_info[5][0:3]
                        landing_airport = flight_info[5][3:]
                        hk_sa_index = 6
                        departure_time_index = 3
                    hk_sa = None
                    if(flight_info[len(flight_info) - 1] == 'FLWN'):
                        flown_checker = True
                        temp_flight.segment_state = 1
                        departure_time = datetime.strptime(flight_info[departure_time_index] + str(yearOfOperation) + ' ' + '00:00:00', '%d%b%Y %H:%M:%S')
                        landing_time = None
                    else:
                        # to loop the line from the last
                        hk_sa = flight_info[hk_sa_index]
                        index = len(flight_info) - 1
                        a = index
                        departure = ''
                        landing = ''
                        if(flight_info[a].startswith('*') or flight_info[a].endswith('*')):
                            while True:
                                if(flight_info[a - 1] != ''):
                                    departure = flight_info[a - 2]
                                    landing = flight_info[a - 1]
                                    break
                                a -= 1
                        else:
                            departure = flight_info[a - 1]
                            landing = flight_info[a]
                        departure_time = datetime.strptime(flight_info[departure_time_index] + str(yearOfOperation) + ' ' + departure[0:2] + ':' + departure[2:] + ':00', '%d%b%Y %H:%M:%S')
                        # sometimes, landing time has a '+' attribute in order to show that some days has to be added from the departure date
                        if(len(landing.split('+')) <= 1):
                            landing_time = datetime.strptime(flight_info[departure_time_index] + str(yearOfOperation) + ' ' + landing[0:2] + ':' + landing[2:] + ':00', '%d%b%Y %H:%M:%S')
                        else:
                            try:
                                landing_time = datetime.strptime(flight_info[departure_time_index] + str(yearOfOperation) + ' ' + landing.split('+')[0][0:2] + ':' + landing.split('+')[0][2:] + ':00', '%d%b%Y %H:%M:%S') + timedelta(days=int(landing.split('+')[1]))
                            except:
                                landing_time = None
                
                temp_flight.servicecarrier = Airline.objects.filter(iata=airline_code).first()
                temp_flight.flightno = flight_number
                try:
                    temp_flight.codeorg = Airport.objects.get(iata_code=departure_airport)
                except:
                    Airport.objects.create(name='Unknown', iata_code=departure_airport)
                    temp_flight.codeorg = Airport.objects.get(iata_code=departure_airport)
                try:
                    temp_flight.codedest = Airport.objects.get(iata_code=landing_airport)
                except:
                    Airport.objects.create(name='Unknown', iata_code=landing_airport)
                    temp_flight.codedest = Airport.objects.get(iata_code=landing_airport)
                temp_flight.amanameorg = ''
                temp_flight.amanamedest = ''
                temp_flight.segment_hk_sa = hk_sa
                
                if departure_time is not None:
                    temp_year = departure_time.year
                    if not flown_checker:
                        temp_year = self.compare_dates(date_operation=pnr.gds_creation_date, date_segment_flight=flight_info[departure_time_index])
                    temp_flight.departuretime = datetime(temp_year, departure_time.month, departure_time.day, departure_time.hour, departure_time.minute, departure_time.second, departure_time.microsecond, pytz.UTC)
                if landing_time is not None:
                    temp_flight.arrivaltime = datetime(temp_year, landing_time.month, landing_time.day, landing_time.hour, landing_time.minute, landing_time.second, landing_time.microsecond, pytz.UTC)
                # segment is a flight END
            # Segment is a SVC
            elif flight_info[1].endswith('SVC'):
                flight_class = 'Y'
                airline_code = flight_info[2]
                other_segment_description = ''
                departure_time = None
                if len(flight_info) > 3:
                    for l in range (3, len(flight_info)):
                        if flight_info[l] != '':
                            other_segment_description += flight_info[l] + ' '
                    temp_flight.other_segment_description = other_segment_description
                # date
                try:
                    for info in flight_info:
                        if len(info.split('-')) > 1:
                            try:
                                departure_time = datetime.strptime(info.split('-')[0] + str(yearOfOperation) + ' ' + '00:00:00', '%d%b%Y %H:%M:%S')
                                temp_flight.departuretime = datetime(departure_time.year, departure_time.month, departure_time.day, departure_time.hour, departure_time.minute, departure_time.second, departure_time.microsecond, pytz.UTC)
                            except:
                                print('SVC date parsing: attempt no 1 failed !')
                    # try if date can be found at the end of the SVC line when no description has been given
                    if departure_time is None:
                        try:
                            departure_time = datetime.strptime(flight_info[-1] + str(yearOfOperation) + ' ' + '00:00:00', '%d%b%Y %H:%M:%S')
                            temp_flight.departuretime = datetime(departure_time.year, departure_time.month, departure_time.day, departure_time.hour, departure_time.minute, departure_time.second, departure_time.microsecond, pytz.UTC)
                        except:
                            print('SVC date parsing: attempt no 2 failed !')
                except:
                    pass
                if departure_time is None:
                    departure_time = datetime.now()
                temp_flight.departuretime = datetime(departure_time.year, departure_time.month, departure_time.day, departure_time.hour, departure_time.minute, departure_time.second, departure_time.microsecond, pytz.UTC)
            
                try:
                    temp_flight.servicecarrier = Airline.objects.filter(iata=airline_code).first()
                except:
                    pass
                temp_flight.segment_type = 'SVC'
            # Segment is open
            elif flight_info[1].endswith('OPEN') or flight_info[2].endswith('OPEN'):
                is_open_status = True
                if flight_info[1].endswith('OPEN'):
                    service_carrier_index = 1
                elif flight_info[2].endswith('OPEN'):
                    service_carrier_index = 2
                temp_flight.servicecarrier = Airline.objects.filter(iata=flight_info[service_carrier_index].removesuffix('OPEN')).first()
                temp_flight.flightclass = flight_info[service_carrier_index+1]
                org_dest = flight_info[-1]
                try:
                    temp_flight.codeorg = Airport.objects.get(iata_code=org_dest[0:3])
                except:
                    pass
                try:
                    temp_flight.codedest = Airport.objects.get(iata_code=org_dest[3:])
                except:
                    pass
            # Segment is ARNK
            elif flight_info[1].endswith('ARNK') or flight_info[2].endswith('ARNK'):
                temp_flight.segment_type = 'ARNK'
                temp_airline = Airline.objects.filter(iata='Unknown').first()
                if temp_airline is None:
                    temp_airline = Airline()
                    temp_airline.iata = 'Unknown'
                    temp_airline.save()
                temp_flight.servicecarrier = temp_airline
            
            temp_flight.is_open = is_open_status
            temp_flight.pnr = pnr
            temp_flight.segmentorder = 'S' + str(all_flight_order[segment])
            temp_flight.flightclass = flight_class
            flights.append(temp_flight)
            segment += 1
                        
        return flights, flight_class
    
    # get all special service request(ssr)
    def get_all_ssr(self, normalized_file, pnr, passengers, segments):
        ssr_lines = []
        ssr_bases = []
        ssr_passengers = []
        ssr_segments = []
        
        for line in normalized_file:
            temp = line.split(" ")
            if len(temp) > 2 and temp[0].isnumeric() == True:
                if temp[1].endswith('SSR'):
                    ssr_lines.append(line)
        
        for ssr in ssr_lines:
            ssr_base = SpecialServiceRequestBase()
            
            info_part = ssr.split(' ')[2:]
            ssr_obj = SpecialServiceRequest.objects.filter(code = info_part[0]).first()
            if ssr_obj is None:
                temp_ssr_obj = SpecialServiceRequest()
                temp_ssr_obj.code = info_part[0]
                temp_ssr_obj.save()
                ssr_obj = temp_ssr_obj
                
            # ssr text (free flow text)
            ssr_text = ''
            for text in info_part:
                ssr_text += text + ' '
            
            # get all related passengers and segments
            related_passengers = []
            related_segments = []
            no_passenger_assigned = True
            for part in info_part[1:]:
                comma_split = part.split(',')
                for temp in comma_split:
                    slash_split = temp.split('/')
                    for slash_part in slash_split:
                        if len(slash_part) > 1 and len(slash_part) < 4:
                            if (slash_part[0] == 'P' or slash_part[0] == 'S') and slash_part[1].isnumeric():
                                if len(slash_part.split('-')) > 1:
                                    temp_sliced_part = slash_part.split('-')
                                    start_segment = int(temp_sliced_part[0][1:])
                                    end_segment = int(temp_sliced_part[len(temp_sliced_part) - 1])
                                    
                                    a = start_segment
                                    while a <= end_segment:
                                        if slash_part[0] == 'P':
                                            for passenger in passengers:
                                                if passenger.order == 'P' + str(a):
                                                    related_passengers.append(passenger)
                                        elif slash_part[0] == 'S':
                                            for segment in segments:
                                                if segment.segmentorder == 'S' + str(a):
                                                    related_segments.append(segment)
                                        a += 1
                                else:
                                    if slash_part[0] == 'P':
                                        no_passenger_assigned = False
                                        for passenger in passengers:
                                            if passenger.order == 'P' + slash_part[1]:
                                                related_passengers.append(passenger)
                                    elif slash_part[0] == 'S':
                                        for segment in segments:
                                            if segment.segmentorder == 'S' + slash_part[1]:
                                                related_segments.append(segment)
                                
            if len(passengers) == 1 and no_passenger_assigned:
                related_passengers.append(passengers[0])
            
            # assigning object to ssr_base  
            ssr_base.ssr = ssr_obj
            ssr_base.pnr = pnr
            ssr_base.ssr_text = ssr_text
            ssr_base.order_line = 'E' + ssr.split(' ')[0]
            ssr_bases.append(ssr_base)
            # ssr passengers
            for temp_passenger in related_passengers:
                temp_ssr_passenger = SpecialServiceRequestPassenger()
                temp_ssr_passenger.parent_ssr = ssr_base
                temp_ssr_passenger.passenger = temp_passenger
                ssr_passengers.append(temp_ssr_passenger)
            # ssr segments
            for temp_segment in related_segments:
                temp_ssr_segment = SpecialServiceRequestSegment()
                temp_ssr_segment.parent_ssr = ssr_base
                temp_ssr_segment.segment = temp_segment
                ssr_segments.append(temp_ssr_segment)
        
        return ssr_bases, ssr_passengers, ssr_segments
    
    # get deadline dates for unconfirmed PNRs
    def get_confirmation_deadline(self, normalized_file, pnr, segments, ssrs):
        year_of_operation = pnr.gds_creation_date.year
        confirmation_deadlines = []
        opw_lines = []
        opc_lines = []
        
        # Possible format:
        # Format 1: 7 OPW-09MAY:1900/1C7/MS REQUIRES TICKET ON OR BEFORE 12MAY:1900/S2
        # Format 2: 10 OPW CAIMxxxxx-21MAY:0000/1C7/MS REQUIRES TICKET ON OR BEFORE 22MAY:0000/S2
        
        for line in normalized_file:
            temp = line.split(" ")
            if len(temp) > 2 and temp[0].isnumeric():
                if temp[1].startswith('OPW'):
                    opw_lines.append(line)
                elif temp[1].startswith('OPC'):
                    opc_lines.append(line)
        
        # parse opw first
        for opw in opw_lines:
            opw_part = opw.split(' ')[1:]
            date_time = None
            date_type = 'OPW'
            free_flow_text = ''
            if opw_part[0] == 'OPW':
                date_part = opw_part[1].split('-')[1]
                date_split = date_part.split('/')[0]
                date_time_split = date_split.split(':')
                date = date_time_split[0] + str(year_of_operation)
                time = date_time_split[1][0:2] + ':' + date_time_split[1][2:] + ':00' 
                date_time = date + ' ' + time
                date_time = datetime.strptime(date_time, '%d%b%Y %H:%M:%S')
                for text in opw_part[2:]:
                    free_flow_text += text + ' ' 
                
                for text in opw_part[2:]:
                    slash_split = text.split('/')
                    for temp_slash_split in slash_split:
                        if (temp_slash_split.startswith('S') or temp_slash_split.startswith('E')) and temp_slash_split[1].isnumeric():
                            # segment group S1,4
                            if len(temp_slash_split.split('-')) > 1 and len(temp_slash_split.split(',')) == 1:
                                temp_sliced_part_1 = temp_slash_split.split('-')
                                start_segment = int(temp_sliced_part_1[0][1:])
                                end_segment = int(temp_sliced_part_1[len(temp_sliced_part_1) - 1])
                                
                                a = start_segment
                                while a <= end_segment:
                                    temp_conf = ConfirmationDeadline()
                                    temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                    temp_conf.free_flow_text = free_flow_text
                                    temp_conf.type = date_type
                                    if temp_slash_split.startswith('S'):
                                        for segment in segments:
                                            if segment.segmentorder == 'S' + str(a):
                                                temp_conf.segment = segment
                                        confirmation_deadlines.append(temp_conf)
                                    elif temp_slash_split.startswith('E'):
                                        for ssr in ssrs:
                                            if ssr.order_line == 'E' + str(a):
                                                temp_conf.ssr = ssr
                                        confirmation_deadlines.append(temp_conf)
                                    a += 1
                            # segment selection S1,2,3
                            elif len(temp_slash_split.split(',')) > 1 and len(temp_slash_split.split('-')) == 1:
                                temp_sliced_part = temp_slash_split.split(',')
                                first_segment = int(temp_sliced_part[0][1:])
                                temp_sliced_part[0] = first_segment
                                
                                a = 0
                                while a < len(temp_sliced_part):
                                    temp_order_count = temp_sliced_part[a]
                                    temp_conf = ConfirmationDeadline()
                                    temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                    temp_conf.free_flow_text = free_flow_text
                                    temp_conf.type = date_type
                                    if first_segment.startswith('S'):
                                        for segment in segments:
                                            if segment.segmentorder == 'S' + str(temp_order_count):
                                                temp_conf.segment = segment
                                        confirmation_deadlines.append(temp_conf)
                                    elif first_segment.startswith('E'):
                                        for ssr in ssrs:
                                            if ssr.order_line == 'E' + str(temp_order_count):
                                                temp_conf.ssr = ssr
                                        confirmation_deadlines.append(temp_conf)
                                    a += 1
                            # segment selection S1,7-9 or S1-3,7-9
                            elif len(temp_slash_split.split('-')) > 1 and len(temp_slash_split.split(',')) > 1:
                                segment_group = temp_slash_split.split(',')
                                first_segment = segment_group[0]
                                for group in segment_group:
                                    temp_sliced_part = group.split('-')
                                    if group.startswith('S'):
                                        start_segment = int(temp_sliced_part[0][1:])
                                    else:
                                        start_segment = int(temp_sliced_part[0])
                                    end_segment = int(temp_sliced_part[len(temp_sliced_part) - 1])
                                    
                                    a = start_segment
                                    while a <= end_segment:
                                        temp_order_count = a
                                        temp_conf = ConfirmationDeadline()
                                        temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                        temp_conf.free_flow_text = free_flow_text
                                        temp_conf.type = date_type
                                        if first_segment.startswith('S'):
                                            for segment in segments:
                                                if segment.segmentorder == 'S' + str(temp_order_count):
                                                    temp_conf.segment = segment
                                            confirmation_deadlines.append(temp_conf)
                                        elif first_segment.startswith('E'):
                                            for ssr in ssrs:
                                                if ssr.order_line == 'E' + str(temp_order_count):
                                                    temp_conf.ssr = ssr
                                            confirmation_deadlines.append(temp_conf)
                                        a += 1
                            # normal S1
                            else:
                                temp_conf = ConfirmationDeadline()
                                temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                temp_conf.free_flow_text = free_flow_text
                                temp_conf.type = date_type
                                if temp_slash_split.startswith('S'):
                                    for segment in segments:
                                        if segment.segmentorder == temp_slash_split:
                                            temp_conf.segment = segment
                                    confirmation_deadlines.append(temp_conf)
                                elif temp_slash_split.startswith('E'):
                                    for ssr in ssrs:
                                        if ssr.order_line == temp_slash_split:
                                            temp_conf.ssr = ssr
                                    confirmation_deadlines.append(temp_conf)
            else:
                date_part = opw_part[0].split('-')[1]
                date_split = date_part.split('/')[0]
                date_time_split = date_split.split(':')
                date = date_time_split[0] + str(year_of_operation)
                time = date_time_split[1][0:2] + ':' + date_time_split[1][2:] + ':00' 
                date_time = date + ' ' + time
                date_time = datetime.strptime(date_time, '%d%b%Y %H:%M:%S')
                for text in opw_part[1:]:
                    free_flow_text += text + ' ' 
                
                for text in opw_part[1:]:
                    slash_split = text.split('/')
                    for temp_slash_split in slash_split:
                        if (temp_slash_split.startswith('S') or temp_slash_split.startswith('E')) and temp_slash_split[1].isnumeric():
                            # segment group S1,4
                            if len(temp_slash_split.split('-')) > 1 and len(temp_slash_split.split(',')) == 1:
                                temp_sliced_part_1 = temp_slash_split.split('-')
                                start_segment = int(temp_sliced_part_1[0][1:])
                                end_segment = int(temp_sliced_part_1[len(temp_sliced_part_1) - 1])
                                
                                a = start_segment
                                while a <= end_segment:
                                    temp_conf = ConfirmationDeadline()
                                    temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                    temp_conf.free_flow_text = free_flow_text
                                    temp_conf.type = date_type
                                    if temp_slash_split.startswith('S'):
                                        for segment in segments:
                                            if segment.segmentorder == 'S' + str(a):
                                                temp_conf.segment = segment
                                        confirmation_deadlines.append(temp_conf)
                                    elif temp_slash_split.startswith('E'):
                                        for ssr in ssrs:
                                            if ssr.order_line == 'E' + str(a):
                                                temp_conf.ssr = ssr
                                        confirmation_deadlines.append(temp_conf)
                                    a += 1
                            # segment selection S1,2,3
                            elif len(temp_slash_split.split(',')) > 1 and len(temp_slash_split.split('-')) == 1:
                                temp_sliced_part = temp_slash_split.split(',')
                                first_segment = temp_sliced_part[0]
                                temp_sliced_part[0] = first_segment[1:]
                                
                                a = 0
                                while a < len(temp_sliced_part):
                                    temp_order_count = temp_sliced_part[a]
                                    temp_conf = ConfirmationDeadline()
                                    temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                    temp_conf.free_flow_text = free_flow_text
                                    temp_conf.type = date_type
                                    if first_segment.startswith('S'):
                                        for segment in segments:
                                            if segment.segmentorder == 'S' + str(temp_order_count):
                                                temp_conf.segment = segment
                                        confirmation_deadlines.append(temp_conf)
                                    elif first_segment.startswith('E'):
                                        for ssr in ssrs:
                                            if ssr.order_line == 'E' + str(temp_order_count):
                                                temp_conf.ssr = ssr
                                        confirmation_deadlines.append(temp_conf)
                                    a += 1
                            # segment selection S1,7-9 or S1-3,7-9
                            elif len(temp_slash_split.split('-')) > 1 and len(temp_slash_split.split(',')) > 1:
                                segment_group = temp_slash_split.split(',')
                                first_segment = segment_group[0]
                                for group in segment_group:
                                    temp_sliced_part = group.split('-')
                                    if group.startswith('S'):
                                        start_segment = int(temp_sliced_part[0][1:])
                                    else:
                                        start_segment = int(temp_sliced_part[0])
                                    end_segment = int(temp_sliced_part[len(temp_sliced_part) - 1].removeprefix('S').removeprefix('E'))
                        
                                    a = start_segment
                                    while a <= end_segment:
                                        temp_order_count = a
                                        temp_conf = ConfirmationDeadline()
                                        temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                        temp_conf.free_flow_text = free_flow_text
                                        temp_conf.type = date_type
                                        if first_segment.startswith('S'):
                                            for segment in segments:
                                                if segment.segmentorder == 'S' + str(temp_order_count):
                                                    temp_conf.segment = segment
                                            confirmation_deadlines.append(temp_conf)
                                        elif first_segment.startswith('E'):
                                            for ssr in ssrs:
                                                if ssr.order_line == 'E' + str(temp_order_count):
                                                    temp_conf.ssr = ssr
                                            confirmation_deadlines.append(temp_conf)
                                        a += 1
                            # normal
                            else:
                                temp_conf = ConfirmationDeadline()
                                temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                temp_conf.free_flow_text = free_flow_text
                                temp_conf.type = date_type
                                if temp_slash_split.startswith('S'):
                                    for segment in segments:
                                        if segment.segmentorder == temp_slash_split:
                                            temp_conf.segment = segment
                                    confirmation_deadlines.append(temp_conf)
                                elif temp_slash_split.startswith('E'):
                                    for ssr in ssrs:
                                        if ssr.order_line == temp_slash_split:
                                            temp_conf.ssr = ssr
                                    confirmation_deadlines.append(temp_conf)
        
        # parse opc now
        for opc in opc_lines:
            opc_part = opc.split(' ')[1:]
            date_time = None
            date_type = 'OPC'
            free_flow_text = ''
            if opc_part[0] == 'OPC':
                date_part = opc_part[1].split('-')[1]
                date_split = date_part.split('/')[0]
                date_time_split = date_split.split(':')
                date = date_time_split[0] + str(year_of_operation)
                time = date_time_split[1][0:2] + ':' + date_time_split[1][2:] + ':00' 
                date_time = date + ' ' + time
                date_time = datetime.strptime(date_time, '%d%b%Y %H:%M:%S')
                for text in opc_part[2:]:
                    free_flow_text += text + ' ' 
                
                for text in opc_part[2:]:
                    slash_split = text.split('/')
                    for temp_slash_split in slash_split:
                        if (temp_slash_split.startswith('S') or temp_slash_split.startswith('E')) and temp_slash_split[1].isnumeric():
                            # segment group S1,4
                            if len(temp_slash_split.split('-')) > 1 and len(temp_slash_split.split(',')) == 1:
                                temp_sliced_part_1 = temp_slash_split.split('-')
                                start_segment = int(temp_sliced_part_1[0][1:])
                                end_segment = int(temp_sliced_part_1[len(temp_sliced_part_1) - 1])
                                
                                a = start_segment
                                while a <= end_segment:
                                    temp_conf = ConfirmationDeadline()
                                    temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                    temp_conf.free_flow_text = free_flow_text
                                    temp_conf.type = date_type
                                    if temp_slash_split.startswith('S'):
                                        for segment in segments:
                                            if segment.segmentorder == 'S' + str(a):
                                                temp_conf.segment = segment
                                        confirmation_deadlines.append(temp_conf)
                                    elif temp_slash_split.startswith('E'):
                                        for ssr in ssrs:
                                            if ssr.order_line == 'E' + str(a):
                                                temp_conf.ssr = ssr
                                        confirmation_deadlines.append(temp_conf)
                                    a += 1
                            # segment selection S1,2,3
                            elif len(temp_slash_split.split(',')) > 1 and len(temp_slash_split.split('-')) == 1:
                                temp_sliced_part = temp_slash_split.split(',')
                                first_segment = temp_sliced_part[0]
                                temp_sliced_part[0] = first_segment[1:]
                                
                                a = 0
                                while a < len(temp_sliced_part):
                                    temp_order_count = temp_sliced_part[a]
                                    temp_conf = ConfirmationDeadline()
                                    temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                    temp_conf.free_flow_text = free_flow_text
                                    temp_conf.type = date_type
                                    if first_segment.startswith('S'):
                                        for segment in segments:
                                            if segment.segmentorder == 'S' + str(temp_order_count):
                                                temp_conf.segment = segment
                                        confirmation_deadlines.append(temp_conf)
                                    elif first_segment.startswith('E'):
                                        for ssr in ssrs:
                                            if ssr.order_line == 'E' + str(temp_order_count):
                                                temp_conf.ssr = ssr
                                        confirmation_deadlines.append(temp_conf)
                                    a += 1
                            # segment selection S1,7-9 or S1-3,7-9
                            elif len(temp_slash_split.split('-')) > 1 and len(temp_slash_split.split(',')) > 1:
                                segment_group = temp_slash_split.split(',')
                                first_segment = segment_group[0]
                                for group in segment_group:
                                    temp_sliced_part = group.split('-')
                                    if group.startswith('S'):
                                        start_segment = int(temp_sliced_part[0][1:])
                                    else:
                                        start_segment = int(temp_sliced_part[0])
                                    end_segment = int(temp_sliced_part[len(temp_sliced_part) - 1])
                                    
                                    a = start_segment
                                    while a <= end_segment:
                                        temp_order_count = a
                                        temp_conf = ConfirmationDeadline()
                                        temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                        temp_conf.free_flow_text = free_flow_text
                                        temp_conf.type = date_type
                                        if first_segment.startswith('S'):
                                            for segment in segments:
                                                if segment.segmentorder == 'S' + str(temp_order_count):
                                                    temp_conf.segment = segment
                                            confirmation_deadlines.append(temp_conf)
                                        elif first_segment.startswith('E'):
                                            for ssr in ssrs:
                                                if ssr.order_line == 'E' + str(temp_order_count):
                                                    temp_conf.ssr = ssr
                                            confirmation_deadlines.append(temp_conf)
                                        a += 1
                            # normal S1
                            else:
                                temp_conf = ConfirmationDeadline()
                                temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                temp_conf.free_flow_text = free_flow_text
                                temp_conf.type = date_type
                                if temp_slash_split.startswith('S'):
                                    for segment in segments:
                                        if segment.segmentorder == temp_slash_split:
                                            temp_conf.segment = segment
                                    confirmation_deadlines.append(temp_conf)
                                elif temp_slash_split.startswith('E'):
                                    for ssr in ssrs:
                                        if ssr.order_line == temp_slash_split:
                                            temp_conf.ssr = ssr
                                    confirmation_deadlines.append(temp_conf)
            else:
                date_part = opc_part[0].split('-')[1]
                date_split = date_part.split('/')[0]
                date_time_split = date_split.split(':')
                date = date_time_split[0] + str(year_of_operation)
                time = date_time_split[1][0:2] + ':' + date_time_split[1][2:] + ':00' 
                date_time = date + ' ' + time
                date_time = datetime.strptime(date_time, '%d%b%Y %H:%M:%S')
                for text in opc_part[1:]:
                    free_flow_text += text + ' ' 
                
                for text in opc_part[1:]:
                    slash_split = text.split('/')
                    for temp_slash_split in slash_split:
                        if (temp_slash_split.startswith('S') or temp_slash_split.startswith('E')) and temp_slash_split[1].isnumeric():
                            # segment group S1,4
                            if len(temp_slash_split.split('-')) > 1 and len(temp_slash_split.split(',')) == 1:
                                temp_sliced_part_1 = temp_slash_split.split('-')
                                start_segment = int(temp_sliced_part_1[0][1:])
                                end_segment = int(temp_sliced_part_1[len(temp_sliced_part_1) - 1])
                                
                                a = start_segment
                                while a <= end_segment:
                                    temp_conf = ConfirmationDeadline()
                                    temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                    temp_conf.free_flow_text = free_flow_text
                                    temp_conf.type = date_type
                                    if temp_slash_split.startswith('S'):
                                        for segment in segments:
                                            if segment.segmentorder == 'S' + str(a):
                                                temp_conf.segment = segment
                                        confirmation_deadlines.append(temp_conf)
                                    elif temp_slash_split.startswith('E'):
                                        for ssr in ssrs:
                                            if ssr.order_line == 'E' + str(a):
                                                temp_conf.ssr = ssr
                                        confirmation_deadlines.append(temp_conf)
                                    a += 1
                            # segment selection S1,2,3
                            elif len(temp_slash_split.split(',')) > 1 and len(temp_slash_split.split('-')) == 1:
                                temp_sliced_part = temp_slash_split.split(',')
                                first_segment = temp_sliced_part[0]
                                temp_sliced_part[0] = first_segment[1:]
                                
                                a = 0
                                while a < len(temp_sliced_part):
                                    temp_order_count = temp_sliced_part[a]
                                    temp_conf = ConfirmationDeadline()
                                    temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                    temp_conf.free_flow_text = free_flow_text
                                    temp_conf.type = date_type
                                    if first_segment.startswith('S'):
                                        for segment in segments:
                                            if segment.segmentorder == 'S' + str(temp_order_count):
                                                temp_conf.segment = segment
                                        confirmation_deadlines.append(temp_conf)
                                    elif first_segment.startswith('E'):
                                        for ssr in ssrs:
                                            if ssr.order_line == 'E' + str(temp_order_count):
                                                temp_conf.ssr = ssr
                                        confirmation_deadlines.append(temp_conf)
                                    a += 1
                            # segment selection S1,7-9 or S1-3,7-9
                            elif len(temp_slash_split.split('-')) > 1 and len(temp_slash_split.split(',')) > 1:
                                segment_group = temp_slash_split.split(',')
                                first_segment = segment_group[0]
                                for group in segment_group:
                                    temp_sliced_part = group.split('-')
                                    if group.startswith('S'):
                                        start_segment = int(temp_sliced_part[0][1:])
                                    else:
                                        start_segment = int(temp_sliced_part[0])
                                    end_segment = int(temp_sliced_part[len(temp_sliced_part) - 1].removeprefix('S').removeprefix('E'))
                        
                                    a = start_segment
                                    while a <= end_segment:
                                        temp_order_count = a
                                        temp_conf = ConfirmationDeadline()
                                        temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                        temp_conf.free_flow_text = free_flow_text
                                        temp_conf.type = date_type
                                        if first_segment.startswith('S'):
                                            for segment in segments:
                                                if segment.segmentorder == 'S' + str(temp_order_count):
                                                    temp_conf.segment = segment
                                            confirmation_deadlines.append(temp_conf)
                                        elif first_segment.startswith('E'):
                                            for ssr in ssrs:
                                                if ssr.order_line == 'E' + str(temp_order_count):
                                                    temp_conf.ssr = ssr
                                            confirmation_deadlines.append(temp_conf)
                                        a += 1
                            # normal
                            else:
                                temp_conf = ConfirmationDeadline()
                                temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                temp_conf.free_flow_text = free_flow_text
                                temp_conf.type = date_type
                                if temp_slash_split.startswith('S'):
                                    for segment in segments:
                                        if segment.segmentorder == temp_slash_split:
                                            temp_conf.segment = segment
                                    confirmation_deadlines.append(temp_conf)
                                elif temp_slash_split.startswith('E'):
                                    for ssr in ssrs:
                                        if ssr.order_line == temp_slash_split:
                                            temp_conf.ssr = ssr
                                    confirmation_deadlines.append(temp_conf)
        return confirmation_deadlines
            
    
    # get ticket on issued pnr
    def ticket_on_issued_pnr(self, normalized_file, pnr, passengers, segments, ssrs, flight_class):
        tickets = []
        tickets_segments = []
        tickets_ssrs = []
        ticket_lines = []
        header_part_indexes = []
        
        for line in normalized_file:
            temp = line.split(" ")
            if len(temp) > 2 and temp[0].isnumeric():
                if temp[1] in TICKET_LINE_IDENTIFIER and temp[2] in SECOND_DEGREE_TICKET_LINE_IDENTIFIER:
                    ticket_lines.append(line)
                    header_part_indexes.append(3)
                elif temp[1] in TICKET_LINE_IDENTIFIER and temp[2] not in SECOND_DEGREE_TICKET_LINE_IDENTIFIER:
                    ticket_lines.append(line)
                    header_part_indexes.append(2)
        
        for ticket_line_index in range(len(ticket_lines)):
            temp_ticket = Ticket()
            
            ticket = ticket_lines[ticket_line_index]
            header_part = ticket.split(' ')[0:header_part_indexes[ticket_line_index]]
            print('Normalized file: ', header_part)
            info_part = ticket.split(' ')[header_part_indexes[ticket_line_index]:]
            # ticket number can be: 760-9010406291 or 760-2404573845-46
            temp_ticket_number_str = info_part[0].split('/')[0]
            # if like 760-9010406291
            if len(temp_ticket_number_str.split('-')) < 3:
                temp_ticket.number = temp_ticket_number_str.replace('-', '')
            # if like 760-2404573845-46
            else:
                temp_ticket.number = temp_ticket_number_str.replace('-', '', 1)
            for part in info_part:
                temp_part = part.split('/')
                for part_slice in temp_part:
                    if part_slice.startswith('P'):
                        # save to related_passenger_order field
                        temp_ticket.related_passenger_order = part_slice
                        for passenger in passengers:
                            if passenger.order == part_slice:
                                # if the passenger is not an INF associated with a parent passenger
                                
                                if header_part[header_part_indexes[ticket_line_index] - 1] != 'INF':
                                    if passenger.types != 'INF_ASSOC':
                                        temp_ticket.passenger = passenger
                                elif header_part[header_part_indexes[ticket_line_index] - 1] == 'INF':
                                    if passenger.types == 'INF_ASSOC':
                                        temp_ticket.passenger = passenger
                                        temp_ticket.passenger_type = 'INF'
                    elif (part_slice.startswith('S') or part_slice.startswith('E')) and part_slice[1].isnumeric():
                        # segment group S1-4
                        if len(part_slice.split('-')) > 1 and len(part_slice.split(',')) == 1:
                            temp_sliced_part = part_slice.split('-')
                            start_segment = int(temp_sliced_part[0][1:])
                            end_segment = int(temp_sliced_part[len(temp_sliced_part) - 1])
                            
                            a = start_segment
                            while a <= end_segment:
                                if part_slice.startswith('S'):
                                    temp_ticket_segment = TicketPassengerSegment()
                                    temp_ticket_segment.ticket = temp_ticket
                                    for segment in segments:
                                        if segment.segmentorder == 'S' + str(a):
                                            temp_ticket_segment.segment = segment
                                    tickets_segments.append(temp_ticket_segment)
                                elif part_slice.startswith('E'):
                                    temp_ticket_ssr = TicketSSR()
                                    temp_ticket_ssr.ticket = temp_ticket
                                    for ssr in ssrs:
                                        if ssr.order_line == 'E' + str(a):
                                            temp_ticket_ssr.ssr = ssr
                                    tickets_ssrs.append(temp_ticket_ssr)
                                a += 1
                        # segment selection S1,2,3
                        elif len(part_slice.split(',')) > 1 and len(part_slice.split('-')) == 1:
                            temp_sliced_part = part_slice.split(',')
                            first_segment = int(temp_sliced_part[0][1:])
                            temp_sliced_part[0] = first_segment
                            
                            a = 0
                            while a < len(temp_sliced_part):
                                temp_order_count = temp_sliced_part[a]
                                if part_slice.startswith('S'):
                                    temp_ticket_segment = TicketPassengerSegment()
                                    temp_ticket_segment.ticket = temp_ticket
                                    for segment in segments:
                                        if segment.segmentorder == 'S' + str(temp_order_count):
                                            temp_ticket_segment.segment = segment
                                    tickets_segments.append(temp_ticket_segment)
                                elif part_slice.startswith('E'):
                                    temp_ticket_ssr = TicketSSR()
                                    temp_ticket_ssr.ticket = temp_ticket
                                    for ssr in ssrs:
                                        if ssr.order_line == 'E' + str(temp_order_count):
                                            temp_ticket_ssr.ssr = ssr
                                    tickets_ssrs.append(temp_ticket_ssr)
                                a += 1
                        # segment selection S1-3,7-9
                        elif len(part_slice.split('-')) > 1 and len(part_slice.split(',')) > 1:
                            segment_group = part_slice.split(',')
                            for group in segment_group:
                                temp_sliced_part = group.split('-')
                                if group.startswith('S'):
                                    start_segment = int(temp_sliced_part[0][1:])
                                else:
                                    start_segment = int(temp_sliced_part[0])
                                end_segment = int(temp_sliced_part[len(temp_sliced_part) - 1].removeprefix('S'))
                                
                                a = start_segment
                                while a <= end_segment:
                                    if part_slice.startswith('S'):
                                        temp_ticket_segment = TicketPassengerSegment()
                                        temp_ticket_segment.ticket = temp_ticket
                                        for segment in segments:
                                            if segment.segmentorder == 'S' + str(a):
                                                temp_ticket_segment.segment = segment
                                        tickets_segments.append(temp_ticket_segment)
                                    elif part_slice.startswith('E'):
                                        temp_ticket_ssr = TicketSSR()
                                        temp_ticket_ssr.ticket = temp_ticket
                                        for ssr in ssrs:
                                            if ssr.order_line == 'E' + str(a):
                                                temp_ticket_ssr.ssr = ssr
                                        tickets_ssrs.append(temp_ticket_ssr)
                                    a += 1
                        else:
                            if part_slice.startswith('S'):
                                temp_ticket_segment = TicketPassengerSegment()
                                temp_ticket_segment.ticket = temp_ticket
                                for segment in segments:
                                    if segment.segmentorder == part_slice:
                                        temp_ticket_segment.segment = segment
                                tickets_segments.append(temp_ticket_segment)
                            elif part_slice.startswith('E'):
                                temp_ticket_ssr = TicketSSR()
                                temp_ticket_ssr.ticket = temp_ticket
                                for ssr in ssrs:
                                    if ssr.order_line == part_slice:
                                        temp_ticket_ssr.ssr = ssr
                                tickets_ssrs.append(temp_ticket_ssr)
            temp_ticket.pnr = pnr
            temp_ticket.flightclass = flight_class
            temp_ticket.state = 2
            temp_ticket.ticket_type = 'TKT'
            if pnr.agent is not None:
                ticket_emitter = User.objects.filter(gds_id=pnr.agent.gds_id).first()
                temp_ticket.emitter = ticket_emitter
            if len(passengers) == 1:
                temp_ticket.passenger = passengers[0]
            elif len(passengers) == 2:
                if passengers[0].types == 'INF_ASSOC' or passengers[1].types == 'INF_ASSOC':
                    if header_part[2] == 'INF':
                        if passengers[0].types == 'INF_ASSOC':
                            temp_ticket.passenger = passengers[0]
                        else:
                            temp_ticket.passenger = passengers[1]
                    else:
                        if passengers[0].types != 'INF_ASSOC':
                            temp_ticket.passenger = passengers[0]
                        else:
                            temp_ticket.passenger = passengers[1]
            
            # segment when it has not been mentioned
            if len(segments) == 1 and header_part[1] != 'FA':
                temp_ticket_segment = TicketPassengerSegment()
                temp_ticket_segment.ticket = temp_ticket
                temp_ticket_segment.segment = segments[0]
                tickets_segments.append(temp_ticket_segment)
            
            # is not fa status
            if header_part[1] != 'FA':
                temp_ticket.is_not_fa_line = True
            
            # ticket issuing_date and ticket issuing_office
            _currencies_ = POSSIBLE_COST_CURRENCY
            issuing_date_str = ''
            issuing_date = None
            issuing_office = None
            info_part_split = info_part[0].split('/')
            transport_cost = 0
            ticket_total = 0
            is_pnr_archived = False
            is_no_adc = False
            try:
                if info_part_split[1].startswith('DT'):
                    temp_ticket.ticket_type = 'EMD'
                elif info_part_split[1].startswith('ET'):
                    temp_ticket.ticket_type = 'TKT'
                elif info_part_split[1].startswith('DR'):
                    temp_ticket.number = temp_ticket.number + '-R'
                    temp_ticket.ticket_type = 'EMD'
                    temp_ticket.is_refund = True
                elif info_part_split[1].startswith('ER'):
                    temp_ticket.number = temp_ticket.number + '-R'
                    temp_ticket.ticket_type = 'TKT'
                    temp_ticket.is_refund = True
                    
                if info_part_split[2][0:3] not in _currencies_:
                    issuing_date_str = info_part_split[2]
                    try:
                        temp_office = Office.objects.filter(code=info_part_split[3]).first()
                    except:
                        pass
                elif info_part_split[2][0:3] in _currencies_:
                    issuing_date_str = info_part_split[3]
                    try:
                        temp_office = Office.objects.filter(code=info_part_split[4]).first()
                        if self.get_is_archived():
                            transport_cost = decimal.Decimal(info_part_split[2][3:])
                            ticket_total = decimal.Decimal(info_part_split[2][3:])
                            is_pnr_archived = True
                        # is no adc status
                        if decimal.Decimal(info_part_split[2][3:]) == 0:
                            is_no_adc = True
                    except:
                        pass
                
                issuing_date = datetime.strptime(issuing_date_str, '%d%b%y').date()
                if temp_office is not None:
                    issuing_office = temp_office
            except:
                pass
            
            # to be re-considered later
            temp_ticket.transport_cost = transport_cost
            temp_ticket.total = ticket_total
            temp_ticket.issuing_date = issuing_date
            temp_ticket.issuing_agency = issuing_office
            temp_ticket.is_no_adc = is_no_adc
            
            if is_no_adc or (is_pnr_archived and ticket_total > 0):
                temp_ticket.state = 0
            
            tickets.append(temp_ticket)
        
        return tickets, tickets_segments, tickets_ssrs
    
    # get credit note
    def get_credit_note(self, normalized_file, pnr, passengers, segments, ssrs, flight_class):
        tickets = []
        tickets_segments = []
        tickets_ssrs = []
        ticket_lines = []
        
        for line in normalized_file:
            temp = line.split(" ")
            if len(temp) > 2 and temp[0].isnumeric():
                if temp[1] == 'FO' and (temp[2] == 'PAX' or temp[2] == 'INF'):
                    ticket_lines.append(line)
        
        for ticket in ticket_lines:
            temp_ticket = Ticket()
            header_part = ticket.split(' ')[0:3]
            info_part = ticket.split(' ')[3:]
            # credit note number part can be: 923-5251648252DZA01OCT22
            temp_ticket_number_str = info_part[0].split('/')[0].replace('-', '')
            ticket_number = ''
            for number in temp_ticket_number_str:
                if not number.isnumeric():
                    break
                ticket_number += number
            temp_ticket.number = ticket_number    
            
            print('FO NUMBER', ticket_number)
            
            for part in info_part:
                temp_part = part.split('/')
                for part_slice in temp_part:
                    if part_slice.startswith('P'):
                        for passenger in passengers:
                            if passenger.order == part_slice:
                                # if the passenger is not an INF associated with a parent passenger
                                if header_part[2] != 'INF':
                                    if passenger.types != 'INF_ASSOC':
                                        temp_ticket.passenger = passenger
                                elif header_part[2] == 'INF':
                                    if passenger.types == 'INF_ASSOC':
                                        temp_ticket.passenger = passenger
                                        temp_ticket.passenger_type = 'INF'
                    elif (part_slice.startswith('S') or part_slice.startswith('E')) and part_slice[1].isnumeric():
                        # segment group S1-4
                        if len(part_slice.split('-')) > 1 and len(part_slice.split(',')) == 1:
                            temp_sliced_part = part_slice.split('-')
                            start_segment = int(temp_sliced_part[0][1:])
                            end_segment = int(temp_sliced_part[len(temp_sliced_part) - 1])
                            
                            a = start_segment
                            while a <= end_segment:
                                if part_slice.startswith('S'):
                                    temp_ticket_segment = TicketPassengerSegment()
                                    temp_ticket_segment.ticket = temp_ticket
                                    for segment in segments:
                                        if segment.segmentorder == 'S' + str(a):
                                            temp_ticket_segment.segment = segment
                                    tickets_segments.append(temp_ticket_segment)
                                elif part_slice.startswith('E'):
                                    temp_ticket_ssr = TicketSSR()
                                    temp_ticket_ssr.ticket = temp_ticket
                                    for ssr in ssrs:
                                        if ssr.order_line == 'E' + str(a):
                                            temp_ticket_ssr.ssr = ssr
                                    tickets_ssrs.append(temp_ticket_ssr)
                                a += 1
                        # segment selection S1,2,3
                        elif len(part_slice.split(',')) > 1 and len(part_slice.split('-')) == 1:
                            temp_sliced_part = part_slice.split(',')
                            first_segment = int(temp_sliced_part[0][1:])
                            temp_sliced_part[0] = first_segment
                            
                            a = 0
                            while a < len(temp_sliced_part):
                                temp_order_count = temp_sliced_part[a]
                                if part_slice.startswith('S'):
                                    temp_ticket_segment = TicketPassengerSegment()
                                    temp_ticket_segment.ticket = temp_ticket
                                    for segment in segments:
                                        if segment.segmentorder == 'S' + str(temp_order_count):
                                            temp_ticket_segment.segment = segment
                                    tickets_segments.append(temp_ticket_segment)
                                elif part_slice.startswith('E'):
                                    temp_ticket_ssr = TicketSSR()
                                    temp_ticket_ssr.ticket = temp_ticket
                                    for ssr in ssrs:
                                        if ssr.order_line == 'E' + str(temp_order_count):
                                            temp_ticket_ssr.ssr = ssr
                                    tickets_ssrs.append(temp_ticket_ssr)
                                a += 1
                        # segment selection S1-3,7-9
                        elif len(part_slice.split('-')) > 1 and len(part_slice.split(',')) > 1:
                            segment_group = part_slice.split(',')
                            for group in segment_group:
                                temp_sliced_part = group.split('-')
                                if group.startswith('S'):
                                    start_segment = int(temp_sliced_part[0][1:])
                                else:
                                    start_segment = int(temp_sliced_part[0])
                                end_segment = int(temp_sliced_part[len(temp_sliced_part) - 1])
                                
                                a = start_segment
                                while a <= end_segment:
                                    if part_slice.startswith('S'):
                                        temp_ticket_segment = TicketPassengerSegment()
                                        temp_ticket_segment.ticket = temp_ticket
                                        for segment in segments:
                                            if segment.segmentorder == 'S' + str(a):
                                                temp_ticket_segment.segment = segment
                                        tickets_segments.append(temp_ticket_segment)
                                    elif part_slice.startswith('E'):
                                        temp_ticket_ssr = TicketSSR()
                                        temp_ticket_ssr.ticket = temp_ticket
                                        for ssr in ssrs:
                                            if ssr.order_line == 'E' + str(a):
                                                temp_ticket_ssr.ssr = ssr
                                        tickets_ssrs.append(temp_ticket_ssr)
                                    a += 1
                        else:
                            if part_slice.startswith('S'):
                                temp_ticket_segment = TicketPassengerSegment()
                                temp_ticket_segment.ticket = temp_ticket
                                for segment in segments:
                                    if segment.segmentorder == part_slice:
                                        temp_ticket_segment.segment = segment
                                tickets_segments.append(temp_ticket_segment)
                            elif part_slice.startswith('E'):
                                temp_ticket_ssr = TicketSSR()
                                temp_ticket_ssr.ticket = temp_ticket
                                for ssr in ssrs:
                                    if ssr.order_line == part_slice:
                                        temp_ticket_ssr.ssr = ssr
                                tickets_ssrs.append(temp_ticket_ssr)
            temp_ticket.pnr = pnr
            temp_ticket.flightclass = flight_class
            temp_ticket.state = 0
            temp_ticket.ticket_type = 'CREDIT_NOTE'
            if pnr.agent is not None:
                ticket_emitter = User.objects.filter(gds_id=pnr.agent.gds_id).first()
                temp_ticket.emitter = ticket_emitter
            if len(passengers) == 1:
                temp_ticket.passenger = passengers[0]
            elif len(passengers) == 2:
                if passengers[0].types == 'INF_ASSOC' or passengers[1].types == 'INF_ASSOC':
                    if header_part[2] == 'INF':
                        if passengers[0].types == 'INF_ASSOC':
                            temp_ticket.passenger = passengers[0]
                        else:
                            temp_ticket.passenger = passengers[1]
                    else:
                        if passengers[0].types != 'INF_ASSOC':
                            temp_ticket.passenger = passengers[0]
                        else:
                            temp_ticket.passenger = passengers[1]
            
            tickets.append(temp_ticket)
            
        # return tickets, tickets_segments, tickets_ssrs
        return [], [], []
    
    # parse am/ah
    def get_am_ah(self, normalized_file, pnr, passengers):
        customer_addresses = []
        addresses_lines = []
        
        for line in normalized_file:
            temp = line.split(' ')
            if len(temp) > 2 and temp[0].isnumeric():
                if temp[1].startswith(AM_H_LINE_IDENTIFIER[0]):
                    addresses_lines.append(line)
                    
        for address in addresses_lines:
            address_part = address.split(' ')[2:]
            
            temp_customer_address = CustomerAddress()
            
            address_text = ''
            passenger_part = ''
            
            for i in range(len(address_part)):
                temp_address_part_split = address_part[i].split('/')
                
                if i == len(address_part)-1 and len(temp_address_part_split) > 1:
                    if temp_address_part_split[-1].startswith('P'):
                        address_text += ' '
                        passenger_part = temp_address_part_split[-1]
                        for j in range(len(temp_address_part_split) - 1):
                            address_text += '/' + temp_address_part_split[j]
                else:
                    address_text += ' ' + address_part[i]
            
            address_text = address_text.replace('/', ' ')
            temp_customer_address.address = address_text
            temp_customer_address.pnr = pnr
            
            for passenger in passengers:
                if passenger.order == passenger_part.strip():
                    temp_customer_address.passenger = passenger
            
            if len(passengers) == 1:
                temp_customer_address.passenger = passengers[0]
            elif len(passengers) == 2:
                if passengers[0].types == 'INF_ASSOC' or passengers[1].types == 'INF_ASSOC':
                    if passengers[0].types == 'INF_ASSOC':
                        temp_customer_address.passenger = passengers[0]
                    else:
                        temp_customer_address.passenger = passengers[1]
            
            customer_addresses.append(temp_customer_address)
        
        return customer_addresses
    
    # save data
    def parse_pnr(self, contents, needed_content, email_date, all_content_information):
        print(self.get_path())
        print('PNR FILE DETECTED')
        sid = transaction.savepoint()
        with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
            try:
                normalized_file = self.normalize_file(needed_content)
                # pnr
                pnr, is_saved, current_pnr_emitter = self.get_pnr_data(contents, email_date)
                # split or duplication
                self.get_split_duplicated_status(pnr, normalized_file)
                if pnr.status == 'Emis':
                    pnr.state = 2 # Billets manquants
                elif pnr.status == 'Non émis':
                    pnr.state = 3 # Tst manquants
                # is archived status
                pnr.is_archived = self.get_is_archived()
                    
                pnr.save()
                
                # save raw data
                try:
                    RawData().save_raw_data(all_content_information, pnr, None)
                except:
                    traceback.print_exc()
                    error_file.write('{}: \n'.format(datetime.now()))
                    error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                    traceback.print_exc(file=error_file)
                    error_file.write('\n')
                
                # pnr elements
                # passengers
                passengers = self.get_passengers(normalized_file)
                # air segments
                air_segments, flight_class = self.get_flight(normalized_file, pnr)
                # update all old air segments
                try:
                    PnrAirSegments().update_segment_status(pnr, air_segments)
                except:
                    traceback.print_exc()
                    error_file.write('{}: \n'.format(datetime.now()))
                    error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                    traceback.print_exc(file=error_file)
                    error_file.write('\n')
                # special services request (SSR)
                ssr_bases, ssr_passengers, ssr_segments = self.get_all_ssr(normalized_file, pnr, passengers, air_segments)
                # contacts
                contacts = self.get_contacts(normalized_file)
                # opw and opc if non issued pnr
                confirmation_deadlines = self.get_confirmation_deadline(normalized_file, pnr, air_segments, ssr_bases)
                # remarks
                pnr_remarks = self.get_remarks(pnr, normalized_file)
                # customers' addresses
                customer_addresses = self.get_am_ah(normalized_file, pnr, passengers)
                
                if len(air_segments) > 0 or len(ssr_bases) > 0 or len(contacts) > 0 or len(confirmation_deadlines) > 0 or len(pnr_remarks) > 0:
                    # check pnr confirmation or emission
                    self.get_pnr_status(pnr, normalized_file)
                # credit notes
                # credit_notes, credit_notes_related_segment, creadit_notes_related_ssrs = self.get_credit_note(normalized_file, pnr, passengers, air_segments, ssr_bases, flight_class)
                # tickets on issued pnr
                if pnr.status == 'Emis':
                    tickets, tickets_segments, tickets_ssrs  = self.ticket_on_issued_pnr(normalized_file, pnr, passengers, air_segments, ssr_bases, flight_class)
                
                # pnr is not saved ------ Insert
                if not is_saved:
                    # passengers
                    for passenger in passengers:
                        passenger.save()
                        pnr_passenger = PnrPassenger(pnr=pnr, passenger=passenger)
                        pnr_passenger.save()
                    # air segments
                    for segment in air_segments:
                        try:
                            segment.save()
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    # special services request (SSR)
                    for ssr_base in ssr_bases:
                        try:
                            ssr_base.save()
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    for ssr_passenger in ssr_passengers:
                        try:
                            ssr_passenger.save()
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    for ssr_segment in ssr_segments:
                        try:
                            ssr_segment.save()
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    # contacts
                    for contact in contacts:
                        contact.pnr = pnr
                        try:
                            contact.save()
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    # opw and opc if non issued pnr  
                    for deadline in confirmation_deadlines:
                        try:
                            deadline.save()
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    # remarks
                    for remark in pnr_remarks:
                        try:
                            remark.save()
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    # customers' addresses
                    for address in customer_addresses:
                        try:
                            address.save()
                        except:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    
                    # credit notes
                    # credit_notes, credit_notes_related_segment, creadit_notes_related_ssrs = self.get_credit_note(normalized_file, pnr, passengers, air_segments, ssr_bases, flight_class)
                    # for credit_note in credit_notes:
                    #     credit_note_obj = Ticket.objects.filter(number=credit_note.number).first()
                    #     if credit_note_obj is None:
                    #         try:
                    #             credit_note.save()
                    #             print('saved (Credit note): ' + credit_note.number)
                    #         except:
                    #             traceback.print_exc()
                    #             error_file.write('{}: \n'.format(datetime.now()))
                    #             error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                    #             traceback.print_exc(file=error_file)
                    #             error_file.write('\n')
                    # for credit_note_segment in credit_notes_related_segment:
                    #     if TicketPassengerSegment.objects.filter(segment_id=credit_note_segment.segment_id).filter(ticket_id=credit_note_segment.ticket_id).first() is None:
                    #         temp_ticket = Ticket.objects.filter(number=credit_note_segment.ticket.number).first()
                    #         credit_note_segment.ticket = temp_ticket
                    #         credit_note_segment.save()
                    #     else:
                    #         temp_ticket = Ticket.objects.filter(number=credit_note_segment.ticket.number).first()
                    #         credit_note_segment.ticket = temp_ticket
                    #         try:
                    #             credit_note_segment.save()
                    #         except Exception as e:
                    #             error_file.write('{}: \n'.format(datetime.now()))
                    #             error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                    #             traceback.print_exc(file=error_file)
                    #             error_file.write('\n')
                    # for credit_note_ssr in creadit_notes_related_ssrs:
                    #     if TicketSSR.objects.filter(ssr_id=credit_note_ssr.ssr_id).filter(ticket_id=credit_note_ssr.ticket_id).first() is None:
                    #         credit_note_ssr.ticket = Ticket.objects.filter(number=credit_note_ssr.ticket.number).first()
                    #         credit_note_ssr.save()
                    #     else:
                    #         credit_note_ssr.ticket = Ticket.objects.filter(number=credit_note_ssr.ticket.number).first()
                    #         try:
                    #             credit_note_ssr.save()
                    #         except Exception as e:
                    #             error_file.write('{}: \n'.format(datetime.now()))
                    #             error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                    #             traceback.print_exc(file=error_file)
                    #             error_file.write('\n')
                    # tickets if issued pnr
                    if pnr.status == 'Emis':
                        for ticket in tickets:
                            # check if ticket has already been saved
                            ticket_obj = Ticket.objects.filter(number=ticket.number).first()
                            # ticket has not been saved yet
                            if ticket_obj is None:
                                try:
                                    if ticket.issuing_date is not None:
                                        ticket.update_ticket_state_status(pnr, ticket.issuing_date, pnr.gds_creation_date)
                                    # ticket emitter
                                    ticket.get_issuing_user_different_creator()
                                    if ticket.emitter is None and current_pnr_emitter is not None:
                                        ticket.emitter = current_pnr_emitter
                                    # refund case
                                    if ticket.is_refund:
                                        temp_ticket_obj = Ticket.objects.filter(number=ticket.number.removesuffix('-R')).first()
                                        if temp_ticket_obj is not None:
                                            if temp_ticket_obj.transport_cost < 0 or temp_ticket_obj.total < 0:
                                                temp_ticket_obj.transport_cost = -1 * temp_ticket_obj.transport_cost
                                                temp_ticket_obj.tax = -1 * temp_ticket_obj.tax
                                                temp_ticket_obj.total = -1 * temp_ticket_obj.total
                                                temp_ticket_obj.save()
                                            
                                            ticket.transport_cost = -1 * temp_ticket_obj.transport_cost
                                            ticket.tax = -1 * temp_ticket_obj.tax
                                            ticket.total = -1 * temp_ticket_obj.total
                                            ticket.passenger = temp_ticket_obj.passenger
                                        else:
                                            temp_ticket_source = Ticket()
                                            temp_ticket_source.number = ticket.number.removesuffix('-R')
                                            temp_ticket_source.passenger = ticket.passenger
                                            temp_ticket_source.related_passenger_order = ticket.related_passenger_order
                                            temp_ticket_source.pnr = pnr
                                            temp_ticket_source.ticket_type = ticket.ticket_type
                                            temp_ticket_source.save()
                                                
                                    ticket.save()
                                    # check subcontractor
                                    ticket.process_subcontract()
                                    print('saved: ' + ticket.number)
                                except Exception:
                                    traceback.print_exc()
                                    error_file.write('{}: \n'.format(datetime.now()))
                                    error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                                    traceback.print_exc(file=error_file)
                                    error_file.write('\n')
                            # ticket has been already saved
                            else:
                                # ticket email received
                                if ticket_obj.state == 1:
                                    ticket_obj.state = 0
                                    ticket_obj.passenger = ticket.passenger
                                    ticket_obj.related_passenger_order = ticket.related_passenger_order
                                    if pnr.agent is not None:
                                        ticket_obj.emitter = pnr.agent
                                    if ticket.issuing_date is not None:
                                        ticket_obj.update_ticket_state_status(pnr, ticket.issuing_date, pnr.gds_creation_date)
                                    # issuing office
                                    ticket_obj.issuing_agency = ticket.issuing_agency
                                    # ticket type
                                    ticket_obj.ticket_type = ticket.ticket_type
                                    if self.get_is_archived():
                                        # ticket cost on archived PNR
                                        ticket_obj.transport_cost = ticket.transport_cost - ticket_obj.tax
                                        ticket_obj.total = ticket.total
                                    # ticket emitter
                                    ticket_obj.get_issuing_user_different_creator()
                                    if ticket_obj.emitter is None and current_pnr_emitter is not None:
                                        ticket_obj.emitter = current_pnr_emitter
                                    # refund case
                                    if ticket.is_refund:
                                        ticket_obj.is_refund = True
                                        if ticket_obj.transport_cost >= 0:
                                            ticket_obj.transport_cost = -1 * ticket_obj.transport_cost
                                            ticket_obj.tax = -1 * ticket_obj.tax
                                            ticket_obj.total = -1 * ticket_obj.total
                                    ticket_obj.save()
                                    # check subcontractor
                                    ticket_obj.process_subcontract()
                        for ticket_ssr in tickets_ssrs:
                            if TicketSSR.objects.filter(ssr_id=ticket_ssr.ssr_id).filter(ticket_id=ticket_ssr.ticket_id).first() is None:
                                ticket_ssr.ticket = Ticket.objects.filter(number=ticket_ssr.ticket.number).first()
                                ticket_ssr.save()
                            else:
                                ticket_ssr.ticket = Ticket.objects.filter(number=ticket_ssr.ticket.number).first()
                                try:
                                    ticket_ssr.save()
                                except Exception as e:
                                    error_file.write('{}: \n'.format(datetime.now()))
                                    error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                                    traceback.print_exc(file=error_file)
                                    error_file.write('\n')
                        for ticket_segment in tickets_segments:
                            temp_ticket = None
                            if TicketPassengerSegment.objects.filter(segment_id=ticket_segment.segment_id).filter(ticket_id=ticket_segment.ticket_id).first() is None:
                                temp_ticket = Ticket.objects.filter(number=ticket_segment.ticket.number).first()
                                ticket_segment.ticket = temp_ticket
                                ticket_segment.save()
                            else:
                                temp_ticket = Ticket.objects.filter(number=ticket_segment.ticket.number).first()
                                ticket_segment.ticket = temp_ticket
                                try:
                                    ticket_segment.save()
                                except Exception as e:
                                    error_file.write('{}: \n'.format(datetime.now()))
                                    error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                                    traceback.print_exc(file=error_file)
                                    error_file.write('\n')
                            # update is_regional status
                            if temp_ticket is not None:
                                temp_ticket.get_set_regional_status()
                                temp_ticket.save()
                        # update ticket status
                        try:
                            Ticket().update_ticket_status_FLOWN(pnr)
                        except Exception as e:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                        # update ticket status: new ticket line inserted 2 days or more later
                        try:
                            Ticket().update_ticket_status_new_line(pnr)
                        except:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                        # udpate ticket status and state after checking their issuing office
                        try:
                            Ticket().update_ticket_status_from_office(pnr)
                        except:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                        # update PNR state
                        try:
                            Ticket().update_pnr_state(pnr)
                        except:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                # pnr is saved ---------- Update
                elif is_saved:
                    temp_pnr = Pnr.objects.filter(number=pnr.number).first()
                    # update pnr state to check if TST arrived or not
                    if temp_pnr.status == 'Non émis':
                        try:
                            temp_pnr.update_tst_missing_status()
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    # passengers
                    # compare and delete
                    try:
                        Passenger().compare_and_delete(temp_pnr, passengers)
                    except:
                        traceback.print_exc()
                        error_file.write('{}: \n'.format(datetime.now()))
                        error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                        traceback.print_exc(file=error_file)
                        error_file.write('\n')
                    for passenger in passengers:
                        temp_passenger = passenger.get_passenger_by_pnr_passenger(pnr)
                        print('PASSENGER', temp_passenger)
                        if temp_passenger is None:
                            passenger.save()
                            try:
                                passenger.update_ticket_passenger(temp_pnr)
                            except:
                                traceback.print_exc()
                                error_file.write('{}: \n'.format(datetime.now()))
                                error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                                traceback.print_exc(file=error_file)
                                error_file.write('\n')
                            pnr_passenger = PnrPassenger(pnr=pnr, passenger=passenger)
                            pnr_passenger.save()
                    # air segments
                    for segment in air_segments:
                        try:
                            temp_segment = segment.get_air_segment_by_air_segment(pnr)
                            if temp_segment is None:
                                segment.save()
                            else:
                                try:
                                    temp_segment.departuretime = segment.departuretime if segment.departuretime is not None else None
                                    temp_segment.arrivaltime = segment.arrivaltime if segment.arrivaltime is not None else None
                                    temp_segment.air_segment_status = 1
                                    temp_segment.segment_state = segment.segment_state
                                    temp_segment.segmentorder = segment.segmentorder
                                    temp_segment.save()
                                except:
                                    traceback.print_exc()
                                
                        except Exception:
                            traceback.print_exc()
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    # special services request (SSR)
                    for ssr_base in ssr_bases:
                        temp_ssr_base = ssr_base.get_ssr_base_by_text_ssr_pnr(pnr)
                        try:
                            if temp_ssr_base is None:
                                ssr_base.save()
                            else:
                                temp_ssr_base.order_line = ssr_base.order_line
                                temp_ssr_base.save()
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    for ssr_passenger in ssr_passengers:
                        temp_parent_ssr_base = SpecialServiceRequestBase.objects.filter(pnr=temp_pnr, order_line=ssr_passenger.parent_ssr.order_line).first()
                        temp_passenger_ssr = Passenger.objects.filter(name=ssr_passenger.passenger.name, surname=ssr_passenger.passenger.surname, designation=ssr_passenger.passenger.designation, passenger__pnr=temp_pnr).first()
                        temp_ssr_passenger = ssr_passenger.get_ssr_passenger_by_parent_passenger(temp_parent_ssr_base, temp_passenger_ssr)
                        try:
                            if temp_ssr_passenger is None:
                                ssr_passenger.parent_ssr = temp_parent_ssr_base
                                ssr_passenger.passenger = temp_passenger_ssr
                                ssr_passenger.save()
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    for ssr_segment in ssr_segments:
                        temp_parent_ssr_base = SpecialServiceRequestBase.objects.filter(pnr=temp_pnr, order_line=ssr_segment.parent_ssr.order_line).first()
                        temp_segment_ssr = PnrAirSegments.objects.filter(pnr=temp_pnr, flightno=ssr_segment.segment.flightno, segmentorder=ssr_segment.segment.segmentorder).first()
                        temp_ssr_segment = ssr_segment.get_ssr_segment_by_parent_segment(temp_parent_ssr_base, temp_segment_ssr)
                        try:
                            if temp_ssr_segment is None:
                                ssr_segment.parent_ssr = temp_parent_ssr_base
                                ssr_segment.segment = temp_segment_ssr
                                ssr_segment.save()
                        except Exception:
                            traceback.print_exc()
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    # contacts
                    for contact in contacts:
                        contact.pnr = pnr
                        temp_contact = contact.get_contact()
                        try:
                            if temp_contact is None:
                                contact.save()
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    # opw and opc if non issued pnr  
                    for deadline in confirmation_deadlines:
                        temp_deadline = deadline.get_confirmation_deadline_by_segment_ssr_type()
                        try:
                            if temp_deadline is None:
                                if deadline.ssr is not None:
                                    temp_ssr = SpecialServiceRequestBase.objects.filter(pnr=temp_pnr, ssr_text=deadline.ssr.ssr_text, order_line=deadline.ssr.order_line).first()
                                    deadline.ssr = temp_ssr
                                if deadline.segment is not None:
                                    temp_segment = PnrAirSegments.objects.filter(pnr=temp_pnr, flightno=deadline.segment.flightno, segmentorder=deadline.segment.segmentorder).first()
                                    deadline.segment = temp_segment
                                deadline.save()
                            else:
                                if temp_deadline.doc_date != deadline.doc_date:
                                    temp_deadline.doc_date = deadline.doc_date
                                temp_deadline.save()
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    # delete OPC or OPW if it has been removed
                    try:
                        ConfirmationDeadline().delete_confirmation_deadline(pnr, confirmation_deadlines)
                    except Exception:
                        error_file.write('{}: \n'.format(datetime.now()))
                        error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                        traceback.print_exc(file=error_file)
                        error_file.write('\n')
                    # remarks
                    for remark in pnr_remarks:
                        temp_remark = remark.get_pnr_remark()
                        try:
                            if temp_remark is None:
                                remark.save()
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    # customers' addresses
                    for address in customer_addresses:
                        try:
                            temp_address = address.get_customer_address   
                            if temp_address is None:
                                address.save()
                        except:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                    # credit notes
                    # credit_notes, credit_notes_related_segment, creadit_notes_related_ssrs = self.get_credit_note(normalized_file, pnr, passengers, air_segments, ssr_bases, flight_class)
                    # for credit_note in credit_notes:
                    #     credit_note_obj = Ticket.objects.filter(number=credit_note.number).first()
                    #     if credit_note_obj is None:
                    #         try:
                    #             credit_note.passenger = Passenger.objects.filter(name=credit_note.passenger.name, surname=credit_note.passenger.surname, designation=credit_note.passenger.designation, passenger__pnr=temp_pnr).first()
                    #             credit_note.save()
                    #             print('saved (Credit note): ' + credit_note.number)
                    #         except:
                    #             traceback.print_exc()
                    #             error_file.write('{}: \n'.format(datetime.now()))
                    #             error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                    #             traceback.print_exc(file=error_file)
                    #             error_file.write('\n')
                    # for credit_note_segment in credit_notes_related_segment:
                    #     temp_segment = PnrAirSegments.objects.filter(segmentorder=credit_note_segment.segment.segmentorder, pnr=temp_pnr, air_segment_status=1).first()
                    #     temp_ticket = Ticket.objects.filter(number=credit_note_segment.ticket.number).first()
                    #     if temp_segment is not None:
                    #         temp_ticket_passenger_segment = TicketPassengerSegment.objects.filter(segment=temp_segment, ticket=temp_ticket).first()
                    #         if temp_ticket_passenger_segment is None:
                    #             credit_note_segment.segment = temp_segment
                    #             credit_note_segment.ticket = temp_ticket
                    #             try:
                    #                 credit_note_segment.save()
                    #             except Exception as e:
                    #                 error_file.write('{}: \n'.format(datetime.now()))
                    #                 error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                    #                 traceback.print_exc(file=error_file)
                    #                 error_file.write('\n')
                    # for credit_note_ssr in creadit_notes_related_ssrs:
                    #     temp_ssr_base = SpecialServiceRequestBase.objects.filter(order_line=credit_note_ssr.ssr.order_line, pnr=temp_pnr).first()
                    #     temp_ticket = Ticket.objects.filter(number=credit_note_ssr.ticket.number).first()
                    #     if temp_ssr_base is not None:
                    #         temp_ticket_ssr = TicketSSR.objects.filter(ssr=temp_ssr_base, ticket=temp_ticket).first()
                    #         if temp_ticket_ssr is None:
                    #             credit_note_ssr.ssr = temp_ssr_base
                    #             credit_note_ssr.ticket = temp_ticket
                    #             try:
                    #                 credit_note_ssr.save()
                    #             except Exception as e:
                    #                 error_file.write('{}: \n'.format(datetime.now()))
                    #                 error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                    #                 traceback.print_exc(file=error_file)
                    #                 error_file.write('\n')
                    # tickets if issued pnr
                    if pnr.status == 'Emis':
                        # update ticket status if the PNR has been reissued with different ticket(s)
                        try:
                            if len(air_segments) > 0 or len(ssr_bases) > 0 or len(contacts) > 0 or len(confirmation_deadlines) > 0 or len(pnr_remarks) > 0:
                                Ticket().update_ticket_status_PNR_reissued(pnr, tickets)
                        except Exception:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                            
                        for ticket in tickets:
                            ticket_obj = Ticket.objects.filter(number=ticket.number).first()
                            # ticket has not been saved yet # PNR Previously not emitted
                            if ticket_obj is None:
                                try:
                                    # when passengers are grouped ticket.passenger will be None
                                    if ticket.passenger is not None:
                                        ticket.passenger = Passenger.objects.filter(name=ticket.passenger.name, surname=ticket.passenger.surname, designation=ticket.passenger.designation, passenger__pnr=temp_pnr).first()
                                        if ticket.issuing_date is not None:
                                            ticket.update_ticket_state_status(temp_pnr, ticket.issuing_date, temp_pnr.gds_creation_date)
                                    # ticket emitter
                                    ticket.get_issuing_user_different_creator()
                                    if ticket.emitter is None and current_pnr_emitter is not None:
                                        ticket.emitter = current_pnr_emitter
                                    # refund case
                                    if ticket.is_refund:
                                        temp_ticket_obj = Ticket.objects.filter(number=ticket.number.removesuffix('-R')).first()
                                        if temp_ticket_obj is not None:
                                            if temp_ticket_obj.transport_cost < 0 or temp_ticket_obj.total < 0:
                                                temp_ticket_obj.transport_cost = -1 * temp_ticket_obj.transport_cost
                                                temp_ticket_obj.tax = -1 * temp_ticket_obj.tax
                                                temp_ticket_obj.total = -1 * temp_ticket_obj.total
                                                temp_ticket_obj.save()
                                            
                                            ticket.transport_cost = -1 * temp_ticket_obj.transport_cost
                                            ticket.tax = -1 * temp_ticket_obj.tax
                                            ticket.total = -1 * temp_ticket_obj.total
                                            ticket.passenger = temp_ticket_obj.passenger
                                        else:
                                            temp_ticket_source = Ticket()
                                            temp_ticket_source.number = ticket.number.removesuffix('-R')
                                            temp_ticket_source.passenger = ticket.passenger
                                            temp_ticket_source.related_passenger_order = ticket.related_passenger_order
                                            temp_ticket_source.pnr = pnr
                                            temp_ticket_source.ticket_type = ticket.ticket_type
                                            temp_ticket_source.save()
                                    ticket.save()
                                    # check subcontractor
                                    ticket.process_subcontract()
                                    print('saved: ' + ticket.number)
                                except Exception:
                                    traceback.print_exc()
                                    error_file.write('{}: \n'.format(datetime.now()))
                                    error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                                    traceback.print_exc(file=error_file)
                                    error_file.write('\n')
                            # ticket has been already saved # PNR is reissued
                            else:
                                try:
                                    ticket_obj.related_passenger_order = ticket.related_passenger_order
                                    # when passengers are grouped ticket.passenger will be None
                                    if ticket.passenger is not None:
                                        ticket_obj.passenger = Passenger.objects.filter(name=ticket.passenger.name, surname=ticket.passenger.surname, designation=ticket.passenger.designation, passenger__pnr=temp_pnr).first()
                                    # issuing office
                                    ticket_obj.issuing_agency = ticket.issuing_agency
                                    # issuing date
                                    if ticket.issuing_date is not None:
                                        ticket_obj.update_ticket_state_status(temp_pnr, ticket.issuing_date, temp_pnr.gds_creation_date)
                                    if ticket_obj.state == 1: # if ticket is 
                                        # check subcontractor
                                        ticket_obj.process_subcontract()
                                        ticket_obj.state = 0
                                    if ticket.emitter is not None:
                                        ticket_obj.emitter = ticket.emitter
                                    if self.get_is_archived():
                                        # ticket cost on archived PNR
                                        ticket_obj.transport_cost = ticket.transport_cost - ticket_obj.tax
                                        ticket_obj.total = ticket.total
                                    # ticket type
                                    ticket_obj.ticket_type = ticket.ticket_type
                                    # ticket emitter
                                    ticket_obj.get_issuing_user_different_creator()
                                    if ticket_obj.emitter is None and current_pnr_emitter is not None:
                                        ticket_obj.emitter = current_pnr_emitter
                                    # refund case
                                    if ticket.is_refund:
                                        ticket_obj.is_refund = True
                                        if ticket_obj.transport_cost >= 0:
                                            ticket_obj.transport_cost = -1 * ticket_obj.transport_cost
                                            ticket_obj.tax = -1 * ticket_obj.tax
                                            ticket_obj.total = -1 * ticket_obj.total
                                    # re-calibrate fee
                                    ticket_obj.save() 
                                    ticket_obj.process_subcontract()
                                    print('saved: ' + ticket.number)
                                except Exception:
                                    traceback.print_exc()
                                    error_file.write('{}: \n'.format(datetime.now()))
                                    error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                                    traceback.print_exc(file=error_file)
                                    error_file.write('\n')
                        for ticket_ssr in tickets_ssrs:
                            temp_ssr_base = SpecialServiceRequestBase.objects.filter(order_line=ticket_ssr.ssr.order_line, pnr=temp_pnr).first()
                            temp_ticket = Ticket.objects.filter(number=ticket_ssr.ticket.number).first()
                            if temp_ssr_base is not None:
                                temp_ticket_ssr = TicketSSR.objects.filter(ssr=temp_ssr_base, ticket=temp_ticket).first()
                                if temp_ticket_ssr is None:
                                    ticket_ssr.ssr = temp_ssr_base
                                    ticket_ssr.ticket = temp_ticket
                                    try:
                                        ticket_ssr.save()
                                    except Exception as e:
                                        error_file.write('{}: \n'.format(datetime.now()))
                                        error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                                        traceback.print_exc(file=error_file)
                                        error_file.write('\n')
                        for ticket_segment in tickets_segments:
                            temp_segment = PnrAirSegments.objects.filter(segmentorder=ticket_segment.segment.segmentorder, pnr=temp_pnr, air_segment_status=1).first()
                            temp_ticket = Ticket.objects.filter(number=ticket_segment.ticket.number).first()
                            if temp_segment is not None:
                                temp_ticket_passenger_segment = TicketPassengerSegment.objects.filter(segment=temp_segment, ticket=temp_ticket).first()
                                if temp_ticket_passenger_segment is None:
                                    ticket_segment.segment = temp_segment
                                    ticket_segment.ticket = temp_ticket
                                    try:
                                        ticket_segment.save()
                                    except Exception as e:
                                        error_file.write('{}: \n'.format(datetime.now()))
                                        error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                                        traceback.print_exc(file=error_file)
                                        error_file.write('\n')
                            # update is_regional status
                            if temp_ticket is not None:
                                temp_ticket.get_set_regional_status()
                                temp_ticket.save()
                        
                        # recalibrating ticket fees
                        try:
                            # ticket_obj.recalibrate_fee()
                            Ticket().recalibrate_fee(temp_pnr)
                        except:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea / Fee recalibration) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                        # update ticket status
                        try:
                            Ticket().update_ticket_status_FLOWN(temp_pnr)
                        except Exception as e:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                        # update ticket status: new ticket line inserted 2 days or more later
                        try:
                            Ticket().update_ticket_status_new_line(temp_pnr)
                        except:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                        # udpate ticket status and state after checking their issuing office
                        try:
                            Ticket().update_ticket_status_from_office(temp_pnr)
                        except:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                        # update PNR state
                        try:
                            Ticket().update_pnr_state(temp_pnr)
                        except:
                            error_file.write('{}: \n'.format(datetime.now()))
                            error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                transaction.savepoint_commit(sid)
            except Exception as e:
                transaction.savepoint_rollback(sid)
                raise e