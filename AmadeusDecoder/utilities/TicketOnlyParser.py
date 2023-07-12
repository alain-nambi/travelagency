'''
Created on 10 Sep 2022

@author: Famenontsoa
'''
import os
import datetime
import traceback
import decimal

import AmadeusDecoder.utilities.configuration_data as configs

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.TicketPassengerTST import TicketPassengerTST
from AmadeusDecoder.models.data.RawData import RawData

COMPANY_CURRENCY = configs.COMPANY_CURRENCY_CODE

# TICKET_IDENTIFIER = ["TKT"]
# RELATED_PNR_NUMBER_IDENTIFIER = ["LOC"]
# TICKET_ISSUING_DATE_IDENTIFIER = ["DOI"]
# ALL_POSSIBLE_TICKET_STATUSES = ['OK', 'SA', 'NS']
# IT_FARE_IDENTIFIER = ["IT"]
# NO_ADC_IDENTIFIER = ["NO", "ADC", "NO ADC"]
# COST_MODIFICATION_IDENTIFIER = ["A"]
# PRIME_TICKET_IDENTIFIER = ["FE", "BP", "PRIME"]
# INVOL_REMOTE_IDENTIFIER = ["INVOL REMOTE"]
# CREDIT_NOTE_TICKET_IDENTIFIER = ["760901", "760-901"]
# GP_TICKET_IDENTIFIER = ["FP OE"]
# COST_DETAIL_IDENTIFIER = ["FARE", "TOTALTAX", "TOTAL"]

TICKET_IDENTIFIER = configs.TICKET_MAIN_IDENTIFIER
RELATED_PNR_NUMBER_IDENTIFIER = configs.RELATED_PNR_NUMBER_IDENTIFIER
TICKET_ISSUING_DATE_IDENTIFIER = configs.TICKET_ISSUING_DATE_IDENTIFIER
ALL_POSSIBLE_TICKET_STATUSES = configs.ALL_POSSIBLE_TICKET_STATUSES
IT_FARE_IDENTIFIER = configs.TICKET_IT_FARE_IDENTIFIER
NO_ADC_IDENTIFIER = configs.TICKET_NO_ADC_IDENTIFIER
COST_MODIFICATION_IDENTIFIER = configs.TICKET_COST_MODIFICATION_IDENTIFIER
PRIME_TICKET_IDENTIFIER = configs.PRIME_TICKET_IDENTIFIER
INVOL_REMOTE_IDENTIFIER = configs.INVOL_REMOTE_IDENTIFIER
CREDIT_NOTE_TICKET_IDENTIFIER = configs.CREDIT_NOTE_TICKET_IDENTIFIER
GP_TICKET_IDENTIFIER = configs.GP_TICKET_IDENTIFIER
COST_DETAIL_IDENTIFIER = configs.TICKET_COST_DETAIL_IDENTIFIER

class TicketOnlyParser():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    # update pnr state
    def update_pnr_state(self, pnr):
        pnr_state = 2 # Ticket(s) missing
        unfilled_ticket = Ticket.objects.filter(pnr=pnr).filter(state=2).first()
        if unfilled_ticket is None:
            pnr_state = 0
        if pnr.state != 1:
            pnr.state = pnr_state
        
        # if a non-emitted PNR is being emitted but instead of receiving emitted PNR the system receives Ticket first
        if pnr.status_value == 1 and pnr.state == 0:
            pnr.state = 1
            pnr.status = 'Emis'
            pnr.status_value = 0
    
    # check if pnr has been saved in database
    def check_pnr(self, ticket_info_line, email_date):
        pnr_number = ''
        ticket_number = ''
        ticket_state = 0
        for temp in ticket_info_line.split(' '):
            if temp.startswith(TICKET_IDENTIFIER[0]):
                # ticket number can be: TKT-7609010406291 or TKT-7602404573845-846
                # if like TKT-7609010406291
                temp_ticket_number_split = temp.split('-')
                if len(temp_ticket_number_split) < 3:
                    ticket_number = temp_ticket_number_split[1]
                # if like TKT-7602404573845-846
                else:
                    if len(temp_ticket_number_split[2]) > 2:
                        ticket_number = temp_ticket_number_split[1] + '-' + temp_ticket_number_split[2][-2:]
                    else:
                        ticket_number = temp_ticket_number_split[1] + '-' + temp_ticket_number_split[2]
            elif temp.startswith(RELATED_PNR_NUMBER_IDENTIFIER[0]):
                pnr_number = temp.split('-')[1]
        
        # system_creation_date = datetime.datetime.now()
        pnr = Pnr.objects.filter(number=pnr_number).first()
        if pnr is None:
            temp_pnr = Pnr()
            temp_pnr.number = pnr_number
            temp_pnr.state = 1 # PNR manquant
            ticket_state = 1 # PNR manquant
            temp_pnr.type = 'Altea'
            temp_pnr.status = 'Emis'
            temp_pnr.status_value = 0
            # temp_pnr.system_creation_date = datetime.datetime(system_creation_date.year, system_creation_date.month, system_creation_date.day, system_creation_date.hour, system_creation_date.minute, system_creation_date.second, system_creation_date.microsecond, pytz.UTC)
            temp_pnr.system_creation_date = email_date
            temp_pnr.save()
            pnr = temp_pnr
        # if PNR is about to be emitted but this ticket comes first
        else:
            if pnr.status_value == 1:
                ticket_state = 1
        ################################### Billet manquant
        pnr.is_read = False
        return pnr, ticket_number, ticket_state
    
    # get ticket issuing date
    def get_ticket_issuing_date(self, file_contents):
        issuing_date = None
        for temp in file_contents:
            temp_space_split = temp.split(' ')
            for element in temp_space_split:
                if element.startswith(TICKET_ISSUING_DATE_IDENTIFIER[0]) and len(element.split('-')) > 1:
                    try:
                        issuing_date = datetime.datetime.strptime(element.split('-')[1], '%d%b%y')
                    except:
                        pass
        
        return issuing_date
            
    # get gp status
    def get_ticket_gp_status(self, file_contents):
        gp_status = ''
        for temp in file_contents:
            if temp.split(' ')[0].isnumeric():
                for element in temp.split(' '):
                    if element in ALL_POSSIBLE_TICKET_STATUSES:
                        gp_status = element
                        break
                break
        return gp_status
    
    # get passenger type
    def get_passenger_type(self, file_content):
        for temp in file_content:
            if temp.split('.')[0].isnumeric():
                for element in temp.split('.'):
                    for space_splitted in element.split(' '):
                        if space_splitted == 'INF':
                            return 'INF'
        return None
    
    # update ticket status for ticket issued outside current travel agency
    def update_status_outside(self, ticket):
        if ticket.is_issued_outside or ticket.is_not_fa_line:
            ticket.ticket_status = 1
    
    # get fare, tax and total in number format
    def get_fares(self, fare_line, tax_line, total_line):
        fare = 0.0
        fare_type = 'F'
        tax = 0.0
        total = 0.0
        is_ticket_modification = False
        is_no_adc = False
        
        try:
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                fare_text = ''
                try:
                    temp_fare_line_split = fare_line.split(' ')                        
                    if temp_fare_line_split[-1] == IT_FARE_IDENTIFIER[0]:
                        fare_text = '0'
                        fare_type = IT_FARE_IDENTIFIER[0]
                    if len(temp_fare_line_split) > 2 and temp_fare_line_split[-1] != IT_FARE_IDENTIFIER[0]:
                        fare_type = temp_fare_line_split[1]
                        float(temp_fare_line_split[-1])
                        fare_text = fare_line.split(' ')[-1]
                except:
                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                    traceback.print_exc(file=error_file)
                    error_file.write('\n')
                    for value in temp_fare_line_split[-1]:
                        if value.isnumeric() or value == '.':
                            fare_text += value
                if fare_text != '':
                    fare = float(fare_text)
                    
                tax_text = ''
                try:
                    float(tax_line.split(' ')[-1])
                    tax_text = tax_line.split(' ')[-1]
                except:
                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                    traceback.print_exc(file=error_file)
                    error_file.write('\n')
                    for value in tax_line.split(' ')[-1]:
                        if value.isnumeric() or value == '.':
                            tax_text += value
                if tax_text != '':
                    tax = float(tax_text)
                    
                total_text = ''
                try:
                    float(total_line.split(' ')[-1])
                    total_text = total_line.split(' ')[-1]
                except:
                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                    traceback.print_exc(file=error_file)
                    error_file.write('\n')
                    if total_line.split(' ')[-1].endswith(COST_MODIFICATION_IDENTIFIER[0]) or total_line.split(' ')[-1].endswith(NO_ADC_IDENTIFIER[1]):
                        is_ticket_modification = True
                        if total_line.split(' ')[-1].endswith(NO_ADC_IDENTIFIER[1]):
                            total_line.split(' ')[-1] = 0
                            is_no_adc = True
                    for value in total_line.split(' ')[-1]:
                        if value.isnumeric() or value == '.':
                            total_text += value
                if total_text != '':
                    total = float(total_text)
        except:
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                traceback.print_exc(file=error_file)
                error_file.write('\n')
        
        try:
            if COMPANY_CURRENCY not in temp_fare_line_split:
                fare = total - tax
            
            if is_ticket_modification:
                fare = total
                tax = 0
                
            if fare_type == IT_FARE_IDENTIFIER[0]:
                fare = 0
                tax = 0
                total = 0
        except:
            pass
        
        return fare, fare_type, tax, total, is_no_adc
    
    # check prime status
    def check_ticket_prime_status(self, file_contents, ticket):
        for line in file_contents:
            if line.startswith(PRIME_TICKET_IDENTIFIER[0]):
                temp_line_split = line.split(' ')
                # for issoufali only
                if (PRIME_TICKET_IDENTIFIER[1] in temp_line_split or PRIME_TICKET_IDENTIFIER[2] in temp_line_split) and ticket.transport_cost == 0 and ticket.fare_type != IT_FARE_IDENTIFIER[0]:
                    ticket.is_prime = True
                    
    # check invol remote status
    def check_is_subjected_to_fees(self, file_contents, ticket):
        for line in file_contents:
            if line.startswith(PRIME_TICKET_IDENTIFIER[0]):
                temp_line_split = line.split(' ')
                if INVOL_REMOTE_IDENTIFIER[0] in temp_line_split:
                    ticket.is_subjected_to_fees = False
    
    # check if current ticket is a credit note
    def check_credit_note(self, ticket):
        # for UU ticket only and with Issoufali
        for identifier in CREDIT_NOTE_TICKET_IDENTIFIER:
            if ticket.number.startswith(identifier) or ticket.number.startswith(identifier):
                ticket.ticket_type = 'Credit_Note'
                ticket.is_subjected_to_fees = False
                break
    
    # check GP status
    def check_gp_status(self, file_contents, ticket):
        for line in file_contents:
            if line.startswith(GP_TICKET_IDENTIFIER[0]):
                ticket.is_gp = True
                break
    
    # parse ticket data
    def parse_ticket(self, file_contents, email_date):
        print('TICKET FILE DETECTED')
        ticket = Ticket()
        
        ticket_info_line = ''
        fare_line = ''
        tax_line = ''
        total_line = ''
        
        for line in file_contents:
            if line.startswith(TICKET_IDENTIFIER[0]):
                ticket_info_line = line
            elif line.startswith(COST_DETAIL_IDENTIFIER[0]):
                fare_line = line
            elif line.startswith(COST_DETAIL_IDENTIFIER[1]):
                tax_line = line
            elif line.startswith(COST_DETAIL_IDENTIFIER[2]):
                total_line = line
        
        # save or update ticket
        pnr, ticket_number, ticket_state = self.check_pnr(ticket_info_line, email_date)
        fare, fare_type, tax, total, is_no_adc = self.get_fares(fare_line, tax_line, total_line)
        # set total to the sum of fare and tax
        total = fare + tax
        gp_status = self.get_ticket_gp_status(file_contents)
        issuing_date = self.get_ticket_issuing_date(file_contents)
        passenger_type = self.get_passenger_type(file_contents)
        
        ticket.number = ticket_number
        ticket.pnr = pnr
        ticket.transport_cost = fare
        ticket.fare_type = fare_type
        ticket.tax = tax
        ticket.total = total
        ticket.doccurrency = COMPANY_CURRENCY
        ticket.farecurrency = COMPANY_CURRENCY
        ticket.state = ticket_state
        ticket.ticket_type = TICKET_IDENTIFIER[0]
        ticket.ticket_gp_status = gp_status
        ticket.issuing_date = issuing_date
        ticket.is_no_adc = is_no_adc
        if passenger_type is not None:
            ticket.passenger_type = passenger_type
        
        temp_ticket = Ticket.objects.filter(number=ticket_number).first()
        if temp_ticket is None:
            try:
                # check prime status
                self.check_ticket_prime_status(file_contents, ticket)
                # check is_subjected_to_fees status
                self.check_is_subjected_to_fees(file_contents, ticket)
                # prime
                if not ticket.is_no_adc and ticket.transport_cost == 0 and fare_type != IT_FARE_IDENTIFIER[0]:
                    ticket.is_prime = True
                # gp
                self.check_gp_status(file_contents, ticket)
            except:
                pass
            ticket.save()
            # update is regional status
            ticket.get_set_regional_status()
        else:
            # get TST if exists on IT fare
            transport_cost = fare
            ticket_tax = tax
            # ticket_total = total
            if fare_type == IT_FARE_IDENTIFIER[0]:
                try:
                    temp_tst_passenger = TicketPassengerTST.objects.filter(passenger__id=temp_ticket.passenger.id).all()
                    if len(temp_tst_passenger) == 1:
                        temp_tst_ticket = Ticket.objects.filter(ticket__id=temp_tst_passenger[0].ticket.id).first()
                        if temp_tst_ticket is not None:
                            transport_cost = temp_tst_ticket.transport_cost
                            ticket_tax = temp_tst_ticket.tax
                            # ticket_total = temp_tst_ticket.total
                except:
                    print('IT not found')
            
            # prime
            # if not temp_ticket.is_no_adc and temp_ticket.transport_cost == 0 and fare_type != 'IT':
            #    temp_ticket.is_prime = True
            if (temp_ticket.transport_cost == 0 or pnr.is_archived) and (decimal.Decimal(temp_ticket.total) != decimal.Decimal(total) or temp_ticket.is_prime):
                temp_ticket.transport_cost = transport_cost
                temp_ticket.tax = ticket_tax
                temp_ticket.total = decimal.Decimal(temp_ticket.transport_cost) + decimal.Decimal(temp_ticket.tax)
            if temp_ticket.fare_type == IT_FARE_IDENTIFIER[0]:
                temp_ticket.fare_type = fare_type
            # if tax > 0:
            temp_ticket.state = ticket_state
            temp_ticket.ticket_type = TICKET_IDENTIFIER[0]
            temp_ticket.ticket_gp_status = gp_status
            temp_ticket.issuing_date = issuing_date
            temp_ticket.is_no_adc = is_no_adc
            if passenger_type is not None:
                temp_ticket.passenger_type = passenger_type
            try:
                # check prime status
                self.check_ticket_prime_status(file_contents, temp_ticket)
                # prime
                if not temp_ticket.is_no_adc and temp_ticket.transport_cost == 0 and fare_type != IT_FARE_IDENTIFIER[0]:
                    temp_ticket.is_prime = True
                # check is_subjected_to_fees status
                self.check_is_subjected_to_fees(file_contents, temp_ticket)
                # update is regional status
                temp_ticket.get_set_regional_status()
                # GP
                self.check_gp_status(file_contents, temp_ticket)
            except:
                pass
            temp_ticket.save()
            ticket = temp_ticket
        
        # update ticket status based on is_issued_outside status
        self.update_status_outside(ticket)
        ticket.save()
        
        self.update_pnr_state(pnr)
        pnr.save()
        
        # save raw data
        try:
            RawData().save_raw_data(file_contents, pnr, ticket)
        except:
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                traceback.print_exc(file=error_file)
                error_file.write('\n')