'''
Created on 21 Oct 2022

@author: Famenontsoa
'''
import os
import traceback
import datetime

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.data.RawData import RawData

_AIRPORT_AGENCY_CODE_ = ['DZAUU000B']
_SPECIAL_EMD_DESCRIPTION_ = ['DEPOSIT']
_NOT_FEED_ = ['RESIDUAL VALUE']

class EMDOnlyParser():
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
    def check_emd_pnr(self, ticket_info_line, email_date):
        pnr_number = ''
        ticket_number = ''
        ticket_state = 0
        for temp in ticket_info_line.split(' '):
            if temp.startswith('EMD'):
                ticket_number = temp.split('-')[1]
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
    
    # check if EMD will be subjected to fees
    def check_emd_fee_subjection(self, pnr, emd):
        try:
            is_emitted_in_airport = False
            emd_issuing_date = emd.issuing_date.date()
            emitter = pnr.get_emit_agent()
            if emitter is not None:
                if emitter.office.code in _AIRPORT_AGENCY_CODE_:
                    is_emitted_in_airport = True
            
            if emd.ticket_ssrs.first() is not None:
                emd_related_segment = emd.ticket_ssrs.first().ssr.segments.first().segment
                emd_segment_flight_date = emd_related_segment.departuretime.date()
                if emd_issuing_date == emd_segment_flight_date and is_emitted_in_airport:
                    emd.is_subjected_to_fees = False
            
            # check fee subjection based on description
            for element in _NOT_FEED_:
                if emd.ticket_description.find(element) > -1:
                    emd.is_subjected_to_fees = False
                    break
        except:
            traceback.print_exc()
    
    # check if EMD is SPECIAL
    def check_if_emd_is_special(self, emd):
        for element in _SPECIAL_EMD_DESCRIPTION_:
            if emd.ticket_description.find(element) > -1:
                emd.is_subjected_to_fees = False
                emd.is_deposit = True
                break
    
    # update ticket status for ticket issued outside current travel agency
    def update_status_outside(self, emd):
        if emd.is_issued_outside:
            emd.ticket_status = 1
    
    # get emd description, issuing_date, payment info, status
    def get_emd_info(self, file_contents):
        emd_description = ''
        emd_issuing_date = None
        emd_payment_info = ''
        emd_status = 1
        
        for content in file_contents:
            content_split = content.split(' ')
            len_content_split = len(content_split)
            for temp in content_split:
                temp_split = temp.split('-')
                len_temp_split = len(temp_split)
                if temp.startswith('S') and len_temp_split > 1:
                    statuses = {'O': 1, 'A': 2, 'F': 3, 'V': 0, 'R': 4, 'E': 5, 'P':6}
                    if temp_split[1] in statuses:
                        emd_status = statuses[temp_split[1]]
                if temp.startswith('RFIC'):
                    if len_content_split > 1:
                        emd_description += '('
                        for i in range(1, len_content_split):
                            emd_description += content_split[i] if content_split[i] != '' else ''
                        emd_description += ')'
                if temp.startswith('DESCRIPTION'):
                    if len_temp_split > 1:
                        if len_content_split == 1:
                            emd_description += ' ' + temp_split[1]
                        elif len_content_split > 1:
                            emd_description += temp_split[1]
                            for i in range(content_split.index(temp) + 1, len_content_split):
                                emd_description += ' ' + content_split[i]
                if temp.startswith('DOI') and len_temp_split > 1:
                    emd_issuing_date = datetime.datetime.strptime(temp_split[1], '%d%b%y')
                if temp.startswith('FP') and len_content_split > 1:
                    emd_payment_info = content_split[1]
        
        return emd_status, emd_description, emd_issuing_date, emd_payment_info
    
    # get fare, tax and total in number format
    def get_emd_fares(self, fare_line, exch_val_line, rfnd_val_line ,total_line):
        fare = 0.0
        exch_val = 0.0
        rfnd_val = 0.0
        total = 0.0
        is_ticket_modification = False
        is_no_adc = False
        
        try:
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                fare_text = ''
                try:
                    float(fare_line.split(' ')[-1])
                    fare_text = fare_line.split(' ')[-1]
                except Exception:
                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                    traceback.print_exc(file=error_file)
                    error_file.write('\n')
                    for value in total_line.split(' ')[-1]:
                        if value.isnumeric() or value == '.':
                            fare_text += value
                if fare_text != '':
                    fare = float(fare_text)
                    if fare == 0:
                        is_no_adc = True
                    
                exch_val_text = ''
                try:
                    float(exch_val_line.split(' ')[-1])
                    exch_val_text = exch_val_line.split(' ')[-1]
                except:
                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                    traceback.print_exc(file=error_file)
                    error_file.write('\n')
                    for value in exch_val_line.split(' ')[-1]:
                        if value.isnumeric() or value == '.':
                            exch_val_text += value
                if exch_val_text != '':
                    exch_val = float(exch_val_text)
                
                rfnd_val_text = ''
                try:
                    float(rfnd_val_line.split(' ')[-1])
                    rfnd_val_text = rfnd_val_line.split(' ')[-1]
                except:
                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                    traceback.print_exc(file=error_file)
                    error_file.write('\n')
                    for value in rfnd_val_line.split(' ')[-1]:
                        if value.isnumeric() or value == '.':
                            rfnd_val_text += value
                if rfnd_val_text != '':
                    rfnd_val = float(rfnd_val_text)
                    
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
            if is_ticket_modification:
                fare = total
        except:
            pass
        
        return fare, exch_val, rfnd_val, total, is_no_adc
    
    # get each info and fare lines
    def info_fare_lines(self, file_contents):
        info_line = ''
        fare_line = ''
        exch_val_line = ''
        rfnd_val_line = ''
        total_line = ''
        
        for line in file_contents:
            if line.startswith('EMD'):
                info_line = line
            elif line.startswith('FARE'):
                fare_line = line
            elif line.startswith('EXCH VAL'):
                if line.find('RFND VAL') != -1:
                    temp_line_split = line.split(' ')
                    for i in range(len(temp_line_split)):
                        if temp_line_split[i] == 'RFND':
                            break
                        if temp_line_split[i] != '':
                            exch_val_line += temp_line_split[i] + ' '
                    for j in range(i, len(temp_line_split)):
                        rfnd_val_line += temp_line_split[j] + ' '
            elif line.startswith('TOTAL'):
                total_line = line
        
        return info_line, fare_line, exch_val_line[:-1], rfnd_val_line[:-1], total_line
    
    # parse ticket data
    def parse_emd(self, file_contents, email_date):
        print('EMD FILE DETECTED')
        emd = Ticket()
        
        # save or update EMD
        info_line, fare_line, exch_val_line, rfnd_val_line, total_line = self.info_fare_lines(file_contents)
        emd_status, emd_description, emd_issuing_date, emd_payment_info = self.get_emd_info(file_contents)
        pnr, emd_number, ticket_state = self.check_emd_pnr(info_line, email_date)
        fare, exch_val, rfnd_val, total, is_no_adc = self.get_emd_fares(fare_line, exch_val_line, rfnd_val_line, total_line)
        
        if pnr.gds_creation_date == emd_issuing_date.date() or pnr.system_creation_date.date() == emd_issuing_date.date():
            emd_status = 1
        
        emd.number = emd_number
        emd.pnr = pnr
        emd.transport_cost = fare
        emd.exch_val = exch_val
        emd.rfnd_val = rfnd_val
        emd.tax = total - fare
        emd.total = total
        emd.doccurrency = 'EUR'
        emd.farecurrency = 'EUR'
        emd.state = ticket_state
        emd.ticket_type = 'EMD'
        emd.ticket_status = emd_status
        emd.ticket_description = emd_description
        emd.issuing_date = emd_issuing_date
        emd.payment_option = emd_payment_info
        emd.is_no_adc = is_no_adc
        
        temp_emd = Ticket.objects.filter(number=emd_number).first()
        trasaction_emd = None
        if temp_emd is None:
            trasaction_emd = emd
        else:
            if temp_emd.transport_cost >= 0 and temp_emd.transport_cost != fare:
                temp_emd.transport_cost = fare
                temp_emd.exch_val = exch_val
                temp_emd.rfnd_val = rfnd_val
                temp_emd.tax = total - fare
                temp_emd.total = total
            temp_emd.state = ticket_state
            temp_emd.ticket_type = 'EMD'
            temp_emd.ticket_status = emd_status
            temp_emd.ticket_description = emd_description
            temp_emd.issuing_date = emd_issuing_date
            temp_emd.payment_option = emd_payment_info
            temp_emd.is_no_adc = is_no_adc
            trasaction_emd = temp_emd
                
        # check emd fee subjection
        self.check_emd_fee_subjection(pnr, trasaction_emd)
        
        # check if emd is special
        try:
            self.check_if_emd_is_special(trasaction_emd)
        except:
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('File (PNR Altea (EMD)) with error: {} \n'.format(str(self.get_path())))
                traceback.print_exc(file=error_file)
                error_file.write('\n')
        
        # update ticket status based on is_issued_outside status
        self.update_status_outside(trasaction_emd)
        
        # save emd
        trasaction_emd.save()
        
        # save raw data
        try:
            RawData().save_raw_data(file_contents, pnr, trasaction_emd)
        except:
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('File (PNR Altea (EMD)) with error: {} \n'.format(str(self.get_path())))
                traceback.print_exc(file=error_file)
                error_file.write('\n')
        
        # update pnr state
        self.update_pnr_state(pnr)
        pnr.save()
        
        # re-check fee
        if trasaction_emd.fees is not None:
            temp_fee = trasaction_emd.fees.first()
            if not trasaction_emd.is_subjected_to_fees and temp_fee is not None:
                temp_fee.cost = 0
                temp_fee.total = 0
                temp_fee.save()