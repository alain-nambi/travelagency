'''
Created on 16 Nov 2022

@author: Famenontsoa
'''
import os
import datetime
import django
import traceback
from AmadeusDecoder.models.configuration.Configuration import Configuration

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'DjangoTravelAgency.settings'
)
django.setup()

from django.conf import settings

import AmadeusDecoder.utilities.configuration_data as configs

from AmadeusDecoder.models.company_info.CompanyInfo import CompanyInfo

class ConfigReader():
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
    
    # ready config file (config.txt) and return company name
    def read_config(self):
        company_name = None
        config_file = None
        try:
            config_file = open(os.path.join(os.getcwd(),'config.txt'), 'r')
            lines = []
            for line in config_file.readlines():
                lines.append(line)
            company_name = lines[0].split('=')[1]
        except:
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting company name failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
        finally:
            if config_file is not None:
                config_file.close()
        
        return company_name
            
    @staticmethod
    def get_company():
        company_name = ConfigReader().read_config()
        if company_name is not None:
            try:
                temp_company_info_obj = CompanyInfo.objects.filter(company_name=company_name).first()
                if temp_company_info_obj is not None:
                    return temp_company_info_obj
                else:
                    raise Exception('No company found')
            except:
                with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                    error_file.write('Getting company name failed. \n')
                    traceback.print_exc(file=error_file)
                    error_file.write('\n')
                return None
        else:
            return None
        
    # load company info
    @staticmethod
    def load_company_info():
        config_name = 'Company Information'
        try:
            configs.COMPANY_NAME = Configuration.objects.filter(name=config_name, value_name='Name').first().single_value
            configs.COMPANY_CURRENCY_NAME = Configuration.objects.filter(name=config_name, value_name='Currency name').first().single_value
            configs.COMPANY_CURRENCY_CODE = Configuration.objects.filter(name=config_name, value_name='Currency code').first().single_value
            configs.COMPANY_LANGUAGE_CODE = Configuration.objects.filter(name=config_name, value_name='Language code').first().single_value
        except:
            print('There was some error when loading company information configuration data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting company name failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
                
    # load email source data
    @staticmethod
    def load_email_source():
        config_name = 'Email Source'
        environment = settings.ENVIRONMENT
        try:
            email_pnr_temp = Configuration.objects.filter(name=config_name, value_name='Email PNR', environment=environment).first()
            if email_pnr_temp is None:
                email_pnr_temp = Configuration.objects.filter(name=config_name, value_name='Email PNR').first()
            configs.EMAIL_PNR = email_pnr_temp.dict_value
            configs.EMAIL_SENDING_ERROR_NOTIFICATION_RECIPIENTS = Configuration.objects.filter(name=config_name, value_name='Email sending error notification recipients').first().array_value
            configs.EMAIL_SENDING_ERROR_NOTIFICATION = Configuration.objects.filter(name=config_name, value_name='Email sending error notification').first().dict_value
            configs.ANOMALY_EMAIL_SENDER = Configuration.objects.filter(name=config_name, value_name='Anomaly email sender').first().dict_value
            configs.PNR_NOT_FETCHED_NOTIFICATION_SENDER = Configuration.objects.filter(name=config_name, value_name='PNR not fetched notification sender').first().dict_value
            configs.FEE_REQUEST_SENDER = Configuration.objects.filter(name=config_name, value_name='Fee request sender').first().dict_value
            configs.PNR_PARSING_ERROR_NOTIFICATION_SENDER = Configuration.objects.filter(name=config_name, value_name='PNR parsing error notification sender').first().dict_value
            configs.PNR_PARSING_ERROR_NOTIFICATION_RECIPIENTS = Configuration.objects.filter(name=config_name, value_name='PNR parsing error notification recipients').first().array_value
        except:
            print('There was some error when loading email source configuration data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting company information failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
                
    # load emd parser tool data
    @staticmethod
    def load_emd_parser_tool_data():
        config_name = 'EMD Parser Tools'
        try:
            configs.AIRPORT_AGENCY_CODE = Configuration.objects.filter(name=config_name, value_name='Airport agency code').first().array_value
            configs.SPECIAL_EMD_DESCRIPTION = Configuration.objects.filter(name=config_name, value_name='Special EMD description').first().array_value
            configs.NOT_FEED = Configuration.objects.filter(name=config_name, value_name='Not feed').first().array_value
            configs.EMD_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='EMD identifier').first().array_value
            configs.PNR_NUMBER_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='PNR number identifier').first().array_value
            configs.PNR_TYPE = Configuration.objects.filter(name=config_name, value_name='PNR type').first().array_value
            configs.EMD_STATUSES = Configuration.objects.filter(name=config_name, value_name='EMD statuses').first().dict_value
            configs.EMD_DESCRIPTION_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='EMD description identifier').first().array_value
            configs.EMD_ISSUING_DATE_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='EMD issuing date identifier').first().array_value
            configs.EMD_PAYMENT_METHOD_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='EMD payment method identifier').first().array_value
            configs.NO_ADC_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='NO ADC identifier').first().array_value
            configs.COST_MODIFICATION_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Cost modification identifier').first().array_value
            configs.COST_DETAIL_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Cost detail identifier').first().array_value
        except:
            print('There was some error when loading EMD parser tool data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting EMD parser tool data failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
                
    # load TST parser tool data
    @staticmethod
    def load_tst_parser_tool_data():
        config_name = 'TST Parser Tools'
        try:
            configs.SPECIAL_AGENCY_CODE = Configuration.objects.filter(name=config_name, value_name='Special agency code').first().array_value
            configs.PASSENGER_DESIGNATIONS = Configuration.objects.filter(name=config_name, value_name='Passenger designations').first().array_value
            configs.TST_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='TST identifier').first().array_value
            configs.TICKET_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Ticket identifier').first().array_value
            configs.COST_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Cost identifier').first().array_value
        except:
            print('There was some error when loading TST parser tool data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting TST parser tool data failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
                
    # load Zenith parser tool data
    @staticmethod
    def load_zenith_parser_tool_data():
        config_name = "Zenith Parser Tools"
        try:
            configs.PASSENGER_TYPES = Configuration.objects.filter(name=config_name, value_name='Passenger type').first().array_value
            configs.ZENITH_PASSENGER_DESIGNATIONS = Configuration.objects.filter(name=config_name, value_name='Passenger designations').first().array_value
            configs.E_TICKET_POSSIBLE_FORMAT = Configuration.objects.filter(name=config_name, value_name='E-ticket possible format').first().array_value
            configs.ITINERARY_HEADER_POSSIBLE_FORMAT = Configuration.objects.filter(name=config_name, value_name='Itinerary header possible format').first().array_value
            configs.HEADER_NAMES = Configuration.objects.filter(name=config_name, value_name='Header names').first().array_value
            configs.SERVICE_CARRIER = Configuration.objects.filter(name=config_name, value_name='Service carrier').first().array_value
            configs.AIRPORT_AGENCY_CODE = Configuration.objects.filter(name=config_name, value_name='Airport agency code').first().array_value
            configs.CURRENT_TRAVEL_AGENCY_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Current travel agency identifier').first().array_value
            configs.NON_RELEVANT_IDENTIFIER_FOR_PASSENGER = Configuration.objects.filter(name=config_name, value_name='Non relevant identifier for passenger').first().array_value
            configs.ITINERARY_NAME = Configuration.objects.filter(name=config_name, value_name='Itinerary name').first().array_value
            configs.ZENITH_COST_DETAIL_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Cost detail identifier').first().array_value
            configs.ANCILLARIES_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Ancillaries identifier').first().array_value
            configs.NOT_EMITTED_PNR_START_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Not emitted PNR start identifier').first().array_value
            configs.NOT_EMITTED_PNR_START_PASSENGER = Configuration.objects.filter(name=config_name, value_name='Not emitted PNR start passenger').first().array_value
            configs.NOT_EMITTED_PNR_START_BOOKING = Configuration.objects.filter(name=config_name, value_name='Not emitted PNR start booking').first().array_value
            configs.NOT_EMITTED_PNR_START_BOOKING_COST = Configuration.objects.filter(name=config_name, value_name='Not emitted PNR start booking cost').first().array_value
            configs.NOT_EMITTED_PNR_START_OPC = Configuration.objects.filter(name=config_name, value_name='Not emitted pnr start opc').first().array_value
            configs.NOT_EMITTED_PNR_END_OPC = Configuration.objects.filter(name=config_name, value_name='Not emitted pnr end opc').first().array_value
            configs.TO_BE_EXCLUDED_PNR_RECIPIENT_EMAIL = Configuration.objects.filter(name=config_name, value_name='To be excluded recipient email').first().array_value
            configs.EMD_REFERENCE_START = Configuration.objects.filter(name=config_name, value_name='EMD reference start').first().array_value
            configs.EMD_EXPIRY_DATE_START = Configuration.objects.filter(name=config_name, value_name='EMD expiry date start').first().array_value
            configs.EMD_COMMENT_START = Configuration.objects.filter(name=config_name, value_name='EMD comment start').first().array_value
            configs.EMD_COST_START = Configuration.objects.filter(name=config_name, value_name='EMD cost start').first().array_value
            configs.MAIN_PNR_NUMBER_START_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Main pnr start identifier').first().array_value
            configs.PASSPORT_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Passport identifier').first().array_value
            configs.PASSENGER_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Passenger identifier').first().array_value
            configs.PAYMENT_RECEIPT_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Payment receipt identifier').first().array_value
            configs.TOTAL_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Total identifier').first().array_value
            configs.PASSENGER_WORD_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Passenger word identifier').first().array_value
            configs.PAYMENT_METHOD_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Payment method identifier').first().array_value
            configs.ISSUING_DATE_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Issuing date identifier').first().array_value
            configs.ISSUING_OFFICE_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Issuing office identifier').first().array_value
            configs.COST_WORD_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Cost word identifier').first().array_value
            configs.MODIFICATION_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Modification identifier').first().array_value
            configs.TAX_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Tax identifier').first().array_value
            configs.RECEIPT_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Receipt identifier').first().array_value
            configs.CUSTOMER_NAME_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Customer name identifier').first().array_value
        except:
            print('There was some error when loading Zenith parser tool data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting Zenith parser tool data failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
                
    # load Zenith parser receipt
    @staticmethod
    def load_zenith_parser_receipt_tool_data():
        config_name = 'Zenith Receipt Parser Tools'
        try:
            configs.PAYMENT_OPTIONS = Configuration.objects.filter(name=config_name, value_name='Payment option').first().array_value
            configs.TICKET_NUMBER_PREFIX = Configuration.objects.filter(name=config_name, value_name='Ticket number prefix').first().array_value
            configs.TO_BE_EXCLUDED_KEY_KEYWORDS = Configuration.objects.filter(name=config_name, value_name='To be excluded keywords').first().array_value
            configs.STARTED_PROCESS_DATE = Configuration.objects.filter(name=config_name, value_name='Started process date').first().date_value
            configs.TICKET_PAYMENT_PART = Configuration.objects.filter(name=config_name, value_name='Ticket payment part').first().array_value
            configs.ADJUSTMENT_PART = Configuration.objects.filter(name=config_name, value_name='Adjustment part').first().array_value
            configs.EMD_CANCELLATION_PART = Configuration.objects.filter(name=config_name, value_name='EMD cancellation part').first().array_value
            configs.TICKET_CANCELLATION_PART = Configuration.objects.filter(name=config_name, value_name='Ticket cancellation part').first().array_value
            configs.PENALTY_PART = Configuration.objects.filter(name=config_name, value_name='Penalty part').first().array_value
            configs.AGENCY_FEE_PART = Configuration.objects.filter(name=config_name, value_name='Agency fee part').first().array_value
            configs.EMD_NO_NUMBER_POSSIBLE_DESIGNATION = Configuration.objects.filter(name=config_name, value_name='EMD no number possible designation').first().array_value
            configs.DEFAULT_ASSIGNED_PASSENGER_ON_OBJECT = Configuration.objects.filter(name=config_name, value_name='Default passenger on object').first().array_value
            configs.EMD_BALANCING_STATEMENT_PART = Configuration.objects.filter(name=config_name, value_name='EMD balancing statement part').first().array_value
        except:
            print('There was some error when loading Zenith parser receipt tool data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting Zenith parser receipt tool data failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
                
    # load ticket parser tool data
    @staticmethod
    def load_ticket_parser_tool_data():
        config_name = 'Ticket Parser Tools'
        try:
            configs.TICKET_MAIN_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Ticket identifier').first().array_value
            configs.RELATED_PNR_NUMBER_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Related PNR number identifier').first().array_value
            configs.TICKET_ISSUING_DATE_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Ticket issuing date identifier').first().array_value
            configs.ALL_POSSIBLE_TICKET_STATUSES = Configuration.objects.filter(name=config_name, value_name='All possible ticket statuses').first().array_value
            configs.TICKET_IT_FARE_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='IT fare identifier').first().array_value
            configs.TICKET_NO_ADC_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='NO ADC identifier').first().array_value
            configs.TICKET_COST_MODIFICATION_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Cost modification identifier').first().array_value
            configs.PRIME_TICKET_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Prime ticket identifier').first().array_value
            configs.INVOL_REMOTE_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Invol remote identifier').first().array_value
            configs.CREDIT_NOTE_TICKET_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Credit note ticket identifier').first().array_value
            configs.GP_TICKET_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='GP ticket identifier').first().array_value
            configs.TICKET_COST_DETAIL_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Cost detail identifier').first().array_value
        except:
            print('There was some error when loading Ticket parser tool data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting Ticket parser tool data failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
                
    # load fee request tool data
    @staticmethod
    def load_fee_request_tool_data():
        config_name = 'Fee Request Tools'
        try:
            configs.FEE_REQUEST_RESPONSE_RECIPIENT = Configuration.objects.filter(name=config_name, value_name='Fee request response recipient').first().array_value
            configs.FEE_DECREASE_REQUEST_RESPONSE_SENDER = Configuration.objects.filter(name=config_name, value_name='Fee decrease request response sender').first().array_value
            configs.FEE_DECREASE_REQUEST_RESPONSE_RECIPIENTS = Configuration.objects.filter(name=config_name, value_name='Fee request request response recipient').first().array_value
        except:
            print('There was some error when loading Fee request tool data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting Fee request tool data failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
                
    # load report email data
    @staticmethod
    def load_report_email_data():
        config_name = 'Report Email'
        try:
            1
        except:
            print('There was some error when loading Report data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting Report email data failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')