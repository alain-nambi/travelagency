'''
Created on 10 Sep 2022

@author: Famenontsoa
'''
import os
import datetime
import traceback
import decimal

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.TicketPassengerTST import TicketPassengerTST
from AmadeusDecoder.models.data.RawData import RawData

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
            if temp.startswith('TKT'):
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
            elif temp.startswith('LOC'):
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
                if element.startswith('DOI') and len(element.split('-')) > 1:
                    try:
                        issuing_date = datetime.datetime.strptime(element.split('-')[1], '%d%b%y')
                    except:
                        pass
        
        return issuing_date
            
    # get gp status
    def get_ticket_gp_status(self, file_contents):
        all_possible_status = ['OK', 'SA', 'NS']
        gp_status = ''
        for temp in file_contents:
            if temp.split(' ')[0].isnumeric():
                for element in temp.split(' '):
                    if element in all_possible_status:
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
        
        # temp currency manager for issoufali only
        issoufali_currency = 'EUR'
        
        try:
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                fare_text = ''
                try:
                    temp_fare_line_split = fare_line.split(' ')                        
                    if temp_fare_line_split[-1] == 'IT':
                        fare_text = '0'
                        fare_type = 'IT'
                    if len(temp_fare_line_split) > 2 and temp_fare_line_split[-1] != 'IT':
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
                    if total_line.split(' ')[-1].endswith('A') or total_line.split(' ')[-1].endswith('ADC'):
                        is_ticket_modification = True
                        if total_line.split(' ')[-1].endswith('ADC'):
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
            if issoufali_currency not in temp_fare_line_split:
                fare = total - tax
            
            if is_ticket_modification:
                fare = total
                tax = 0
                
            if fare_type == 'IT':
                fare = 0
                tax = 0
                total = 0
        except:
            pass
        
        return fare, fare_type, tax, total, is_no_adc
    
    # check prime status
    def check_ticket_prime_status(self, file_contents, ticket):
        for line in file_contents:
            if line.startswith('FE'):
                temp_line_split = line.split(' ')
                # for issoufali only
                if ('BP' in temp_line_split or 'PRIME' in temp_line_split) and ticket.transport_cost == 0 and ticket.fare_type != 'IT':
                    ticket.is_prime = True
                    
    # check invol remote status
    def check_is_subjected_to_fees(self, file_contents, ticket):
        for line in file_contents:
            if line.startswith('FE'):
                temp_line_split = line.split(' ')
                if 'INVOL REMOTE' in temp_line_split:
                    ticket.is_subjected_to_fees = False
    
    # check if current ticket is a credit note
    def check_credit_note(self, ticket):
        # for UU ticket only and with Issoufali
        if ticket.number.startswith('760901') or ticket.number.startswith('760-901'):
            ticket.ticket_type = 'Credit_Note'
            ticket.is_subjected_to_fees = False
                    
    # parse ticket data
    def parse_ticket(self, file_contents, email_date):
        print('TICKET FILE DETECTED')
        ticket = Ticket()
        
        ticket_info_line = ''
        fare_line = ''
        tax_line = ''
        total_line = ''
        
        for line in file_contents:
            if line.startswith('TKT'):
                ticket_info_line = line
            elif line.startswith('FARE'):
                fare_line = line
            elif line.startswith('TOTALTAX'):
                tax_line = line
            elif line.startswith('TOTAL'):
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
        ticket.doccurrency = 'EUR'
        ticket.farecurrency = 'EUR'
        ticket.state = ticket_state
        ticket.ticket_type = 'TKT'
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
                if not ticket.is_no_adc and ticket.transport_cost == 0 and fare_type != 'IT':
                    ticket.is_prime = True
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
            if fare_type == 'IT':
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
            if (temp_ticket.transport_cost == 0 or pnr.is_archived) and (temp_ticket.transport_cost != transport_cost or temp_ticket.is_prime):
                temp_ticket.transport_cost = transport_cost
                temp_ticket.tax = ticket_tax
                temp_ticket.total = decimal.Decimal(temp_ticket.transport_cost) + decimal.Decimal(temp_ticket.tax)
            if temp_ticket.fare_type == 'IT':
                temp_ticket.fare_type = fare_type
            # if tax > 0:
            temp_ticket.state = ticket_state
            temp_ticket.ticket_type = 'TKT'
            temp_ticket.ticket_gp_status = gp_status
            temp_ticket.issuing_date = issuing_date
            temp_ticket.is_no_adc = is_no_adc
            if passenger_type is not None:
                temp_ticket.passenger_type = passenger_type
            try:
                # check prime status
                self.check_ticket_prime_status(file_contents, temp_ticket)
                # check is_subjected_to_fees status
                self.check_is_subjected_to_fees(file_contents, temp_ticket)
                # update is regional status
                temp_ticket.get_set_regional_status()
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