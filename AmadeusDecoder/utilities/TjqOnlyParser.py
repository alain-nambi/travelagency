'''
Created on 29 Dec 2022

@author: Mihaja
'''
import os
from datetime import datetime
import traceback

from AmadeusDecoder.models.pnrelements.Tjq import Tjq
from AmadeusDecoder.models.user.Users import User, Office
from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.Fee import Fee

class TjqOnlyParser():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    
    # get each info and fare lines
    def get_doc_info(self, file_contents):
        tjq_agent_type = ''
        office = ''
        tjq_lines = []
        currency =''
        doc_date = ''
        

        for i,line in enumerate(file_contents):
            if line.startswith('AGENT'):
                try :
                    tjq_agent_type = line.split('AGENT  - ')[0]
                    doc_date = line[-12:]
                except :
                    traceback.print_exc()
                    with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                        error_file.write('{}: \n'.format(datetime.now()))
                        # error_file.write('Line (TJQ) with error: {} \n'.format(str(error_file)))
                        traceback.print_exc(file=error_file)
                        error_file.write('\n')

            elif line.startswith('OFFICE'):
                try :
                    office = line.split('OFFICE -')[1].split('SELECTION')[0]
                except :
                    traceback.print_exc()
                    with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                        error_file.write('{}: \n'.format(datetime.now()))
                        # error_file.write('Line (TJQ) with error: {} \n'.format(str(error_file)))
                        traceback.print_exc(file=error_file)
                        error_file.write('\n')
            elif line.startswith('CURRENCY'):
                try :
                    currency = line.split('CURRENCY')[1]
                except :
                    traceback.print_exc()
                    with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                        error_file.write('{}: \n'.format(datetime.now()))
                        # error_file.write('Line (TJQ) with error: {} \n'.format(str(error_file)))
                        traceback.print_exc(file=error_file)
                        error_file.write('\n')
            elif line.startswith('SEQ'):
                tjq_lines = file_contents[i+2:]

               
        
        return tjq_agent_type, office,currency,doc_date, tjq_lines
    # update ticket on missing fare/total or tst
    def update_ticket(self, tjq):
        pnr = Pnr.objects.filter(number=tjq.pnr_number).first()
        if pnr is not None:
            ticket = Ticket.objects.filter(number=tjq.ticket_number, pnr=pnr).first()
            if ticket is not None:
                fee = Fee.objects.filter(ticket=ticket).first()
                if fee is None and ticket.total == 0 and ticket.transport_cost == 0:
                    ticket.total = tjq.total
                    ticket.tax = tjq.tax
                    ticket.transport_cost = tjq.total - tjq.tax
                    ticket.state = 0
                    if tjq.total == 0:
                        ticket.is_no_adc = True
                    ticket.save()
                    # update pnr state
                    ticket.update_pnr_state(pnr)
    
    # save tjq
    def save_tjq(self, tjq_agent_type, office,currency,doc_date, tjq_lines) :
        tjq = Tjq()
        tjq_lines = tjq_lines.replace('*', ' ')
        lines = tjq_lines.split(" ")
        lines = [ t for t in lines if t != '']
        
        # Check if exists
        tjq_objects = Tjq.objects.all()
        tjqs_seq_no = [ t.seq_no for t in tjq_objects]
        try :
            user_gds_id = lines[-3]
            user_agent = User.objects.filter(gds_id=user_gds_id).first()
            user_agency = Office.objects.filter(code=office).first()

            tjq.agency = user_agency if user_agency is not None else None
            tjq.agency_name = office
            tjq.tjq_agent_type = tjq_agent_type
            tjq.doc_date = doc_date
            tjq.currency = currency
            tjq.seq_no = lines[0]
            tjq.ticket_number = "".join([lines[1], lines[2]])
            tjq.pnr_number = lines[-2]
            tjq.tax = float(lines[4])
            tjq.total = float(lines[3])
            tjq.fee = float(lines[5])
            tjq.comm = float(lines[6])
            tjq.fp_pax = lines[7]
            tjq.passenger = lines[8]
            tjq.agent_code = user_gds_id
            tjq.agent = user_agent if user_agent is not None else None
            tjq.type = lines[-1]
            tjq.system_creation_date = datetime.now()
            
            if tjq.seq_no not in tjqs_seq_no :

                tjq.save()
                print('TJQ SAVED')

            else :
                print('TJQ ALREADY CREATED')
            
            # update ticket on missing fare/total or tst
            self.update_ticket(tjq)
        except :
            traceback.print_exc()
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.now()))
                # error_file.write('Line (TJQ) with error: {} \n'.format(str(error_file)))
                traceback.print_exc(file=error_file)
                error_file.write('\n')
    
    # parse ticket data
    def parse_tjq(self, file_contents):
        print('TJQ FILE DETECTED')
        
        # save or update EMD
        tjq_agent_type, office, currency,doc_date, tjq_lines = self.get_doc_info(file_contents)

        for tjq in tjq_lines :
            self.save_tjq(tjq_agent_type, office, currency,doc_date, tjq)
