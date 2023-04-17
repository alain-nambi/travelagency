'''
Created on 3 Jan 2023

@author: Famenontsoa
'''
import decimal
import traceback

from AmadeusDecoder.models.invoice.Fee import ReducePnrFeeRequest, Fee
from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.utilities.ServiceFeesDecreaseRequest import ServiceFeesDecreaseRequest
from AmadeusDecoder.models.invoice.InvoiceDetails import InvoiceDetails
from AmadeusDecoder.models.history.History import History

class ServiceFeeDecreaseResponseParser():
    '''
    classdocs
    '''
    
    __record_locator = ''
    __ticket_concerned = ''
    __token = ''
    __status = ''
    __to_be_applied = 0

    def __init__(self):
        '''
        Constructor
        '''

    def get_record_locator(self):
        return self.__record_locator

    def get_ticket_concerned(self):
        return self.__ticket_concerned

    def get_token(self):
        return self.__token

    def get_status(self):
        return self.__status

    def get_to_be_applied(self):
        return self.__to_be_applied

    def set_record_locator(self, value):
        self.__record_locator = value

    def set_ticket_concerned(self, value):
        self.__ticket_concerned = value

    def set_token(self, value):
        self.__token = value

    def set_status(self, value):
        self.__status = value

    def set_to_be_applied(self, value):
        self.__to_be_applied = value
    
    # get action performer
    def get_reduce_request_submitter(self, request_obj):
        file_path = self.get_path()
        try:
            submitter_email = file_path.split('/')[-1]
            if len(file_path.split('/')) == 1:
                submitter_email = file_path.split("\\")[-1]
            submitter_email = submitter_email.removeprefix(submitter_email.split('_')[0] + '_').removesuffix('.txt')
            user_submit = User.objects.filter(email=submitter_email).first()
            if user_submit is not None:
                request_obj.user_responder = user_submit
        except:
            print('Error when finding reduce fee request action performer')
    
    # get all returned data
    def sf_decrease_request_data(self, file_contents):
        one_line_content = ''
        for line in file_contents:
            one_line_content += line.strip() + ' '
        
        file_contents = one_line_content.split(';')
        print(file_contents)
        for line in file_contents:
            line_dot_split = line.split('.')
            line_space_split = line.split(' ')
            if line_dot_split[0].endswith('1'):
                b = -1
                while True:
                    if line_space_split[b] != '' and len(line_space_split[b]) == 6:
                        self.set_record_locator(line_space_split[b])
                        break
                    b -= 1
            elif line_dot_split[0].endswith('2'):
                if line_dot_split[1] == 'ONLY ONE TICKET CONCERNED':
                    self.set_ticket_concerned('one')
                elif line_dot_split[1] == 'ALL TICKET CONCERNED':
                    self.set_ticket_concerned('all')
            elif line_dot_split[0].endswith('3'):
                
                self.set_token(line_space_split[-1])
            elif line_dot_split[0].endswith('9'):
                self.set_status(line_space_split[-1])
            elif line_dot_split[0].endswith('10'):
                if line.split(':')[-1].isnumeric():
                    self.set_to_be_applied(decimal.Decimal(line.split(':')[-1].replace(',', '.')))
                if line_space_split[-1].isnumeric():
                    self.set_to_be_applied(decimal.Decimal(line_space_split[-1].replace(',', '.')))
        print(self.get_token())

    # update fee
    def sf_decrease_request_update(self, file_contents):
        self.sf_decrease_request_data(file_contents)
        
        pnr_obj = Pnr.objects.filter(number=self.get_record_locator().strip()).first()
        print(self.get_record_locator())
        request_obj = ReducePnrFeeRequest.objects.filter(pnr=pnr_obj, token=self.get_token().strip()).first()
        fee_obj = request_obj.fee
        fee_amount = request_obj.amount
        request_status = 1
        
        # get current total and initial fee
        initial_total = 0
        current_fee_cost = fee_obj.cost
        try:
            invoice_detail_obj = InvoiceDetails().get_invoice_detail_by_pnr(pnr_obj)
            initial_total = invoice_detail_obj.total
        except:
            traceback.print_exc()
        
        if request_obj and request_obj.status == 0:
            # when the requested fee has been accepted but modified by administrations
            if self.get_status() == 'ACCEPTED/MODIFIED':
                fee_amount = self.get_to_be_applied()
                decrease_status = 2
                request_status = 3
            elif self.get_status() == 'ACCEPTED':
                decrease_status = 1
                request_status = 1
            elif self.get_status() == 'REJECTED':
                fee_amount = fee_obj.cost
                decrease_status = 0
                request_status = 2
                
            if decrease_status in (1, 2):
                # if only one fee is concerned
                if self.get_ticket_concerned() == 'one':
                    fee_obj.cost = fee_amount
                    fee_obj.total = fee_amount
                    fee_obj.save()
                # if all fees are concerned
                elif self.get_ticket_concerned() == 'all':
                    all_ticket_related_fees = Fee.objects.filter(pnr=pnr_obj).all()
                    for temp_related_ticket in all_ticket_related_fees:
                        temp_related_ticket.cost = fee_amount
                        temp_related_ticket.total = fee_amount
                        temp_related_ticket.save()
            
            request_obj.status = request_status
            self.get_reduce_request_submitter(request_obj)
            request_obj.save()
            # send response
            user_responder = ''
            if request_obj.user_responder is not None:
                user_responder = str(request_obj.user_responder)
            service_fees_decrease_request_obj = ServiceFeesDecreaseRequest()
            service_fees_decrease_request_obj.send_decrease_request_response(request_obj, fee_amount, decrease_status, self.get_ticket_concerned().strip(), user_responder)
            
            # fee history
            # save fee update history
            History().fee_history(fee_obj, request_obj.user_responder, current_fee_cost, fee_amount, initial_total)