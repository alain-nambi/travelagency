'''
Created on 16 Nov 2022

@author: Famenontsoa
'''
import os
import datetime
# import django
import traceback

# os.environ.setdefault(
#     'DJANGO_SETTINGS_MODULE', 'DjangoTravelAgency.settings'
# )
# django.setup()

from django.conf import settings
from django.shortcuts import redirect

import AmadeusDecoder.utilities.configuration_data as configs

from AmadeusDecoder.models.configuration.Configuration import Configuration
from AmadeusDecoder.models.company_info.CompanyInfo import CompanyInfo
from AmadeusDecoder.models.pnrelements.Country import Country
from AmadeusDecoder.models.api.FrenchCountry import Department, Municipality

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
            configs.REGIONAL_COUNTRIES = Configuration.objects.filter(name=config_name, value_name='Regional country').first().array_value
        except:
            print('There was some error when loading company information configuration data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting company name failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')


    # load saving protocol file odoo
    @staticmethod
    def load_file_protocol():
        config_name = 'Saving File Tools'
        environment = settings.ENVIRONMENT
        try:
            configs.FILE_PROTOCOL = Configuration.objects.filter(name=config_name, environment=environment).first()
            
        except:
            print('There was some error when loading saving file tools configuration data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting saving file failed. \n')
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
            
            email_error_notification_temp = Configuration.objects.filter(name=config_name, value_name='Email sending error notification recipients', environment=environment).first()
            if email_error_notification_temp is None:
                email_error_notification_temp = Configuration.objects.filter(name=config_name, value_name='Email sending error notification recipients').first()
            configs.EMAIL_SENDING_ERROR_NOTIFICATION_RECIPIENTS = email_error_notification_temp.array_value
            
            email_sending_error_notification_temp = Configuration.objects.filter(name=config_name, value_name='Email sending error notification', environment=environment).first()
            if email_sending_error_notification_temp is None:
                email_sending_error_notification_temp = Configuration.objects.filter(name=config_name, value_name='Email sending error notification').first()
            configs.EMAIL_SENDING_ERROR_NOTIFICATION = email_sending_error_notification_temp.dict_value
            
            anomaly_email_sender_temp = Configuration.objects.filter(name=config_name, value_name='Anomaly email sender', environment=environment).first()
            if anomaly_email_sender_temp is None:
                anomaly_email_sender_temp = Configuration.objects.filter(name=config_name, value_name='Anomaly email sender').first()
            configs.ANOMALY_EMAIL_SENDER = anomaly_email_sender_temp.dict_value
            
            pnr_not_fetched_notification_sender_temp = Configuration.objects.filter(name=config_name, value_name='PNR not fetched notification sender', environment=environment).first()
            if pnr_not_fetched_notification_sender_temp is None:
                pnr_not_fetched_notification_sender_temp = Configuration.objects.filter(name=config_name, value_name='PNR not fetched notification sender').first()
            configs.PNR_NOT_FETCHED_NOTIFICATION_SENDER = pnr_not_fetched_notification_sender_temp.dict_value
            
            fee_request_sender_temp = Configuration.objects.filter(name=config_name, value_name='Fee request sender', environment=environment).first()
            if fee_request_sender_temp is None:
                fee_request_sender_temp = Configuration.objects.filter(name=config_name, value_name='Fee request sender').first()
            configs.FEE_REQUEST_SENDER = fee_request_sender_temp.dict_value
            
            fee_request_recipient_temp = Configuration.objects.filter(name=config_name, value_name='Fee request recipient', environment=environment).first()
            if fee_request_recipient_temp is None:
                fee_request_recipient_temp = Configuration.objects.filter(name=config_name, value_name='Fee request recipient').first()
            configs.FEE_REQUEST_RECIPIENT = fee_request_recipient_temp.array_value
            
            pnr_parsing_error_notification_sender_temp = Configuration.objects.filter(name=config_name, value_name='PNR parsing error notification sender', environment=environment).first()
            if pnr_parsing_error_notification_sender_temp is None:
                pnr_parsing_error_notification_sender_temp = Configuration.objects.filter(name=config_name, value_name='PNR parsing error notification sender').first()
            configs.PNR_PARSING_ERROR_NOTIFICATION_SENDER = pnr_parsing_error_notification_sender_temp.dict_value
            
            pnr_parsing_error_notification_recipients_temp = Configuration.objects.filter(name=config_name, value_name='PNR parsing error notification recipients', environment=environment).first()
            if pnr_parsing_error_notification_recipients_temp is None:
                pnr_parsing_error_notification_recipients_temp = Configuration.objects.filter(name=config_name, value_name='PNR parsing error notification recipients').first()
            configs.PNR_PARSING_ERROR_NOTIFICATION_RECIPIENTS = pnr_parsing_error_notification_recipients_temp.array_value
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
            configs.TST_FARE_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Fare identifier').first().array_value
            configs.TST_FARE_EQUIV_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Fare equiv identifier').first().array_value
            configs.TST_TOTAL_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Total identifier').first().array_value
            configs.TST_GRAND_TOTAL_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Grand Total identifier').first().array_value
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
            
            temp_issuing_agent_identifier = None
            temp_issuing_agent_identifier = Configuration.objects.filter(name=config_name, value_name='Issuing agent identifier').first()
            if temp_issuing_agent_identifier is not None:
                configs.ISSUING_AGENT_IDENTIFIER = temp_issuing_agent_identifier.array_value
            
            configs.COST_WORD_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Cost word identifier').first().array_value
            configs.MODIFICATION_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Modification identifier').first().array_value
            configs.TAX_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Tax identifier').first().array_value
            configs.RECEIPT_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Receipt identifier').first().array_value
            configs.CUSTOMER_NAME_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Customer name identifier').first().array_value
            configs.ITINERARY_AIRPORT_IATA_CODE_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Itinerary airport iata code identifier').first().array_value
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
            configs.FEE_DECREASE_REQUEST_RESPONSE_RECIPIENTS = Configuration.objects.filter(name=config_name, value_name='Fee decrease request response recipient').first().array_value
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
        environment = settings.ENVIRONMENT
        try:
            fee_history_report_local_recipients_temp = Configuration.objects.filter(name=config_name, value_name='Fee history report local recipients', environment=environment).first()
            if fee_history_report_local_recipients_temp is None:
                fee_history_report_local_recipients_temp = Configuration.objects.filter(name=config_name, value_name='Fee history report local recipients').first()
            configs.FEE_HISTORY_REPORT_LOCAL_RECIPIENTS = fee_history_report_local_recipients_temp.array_value
            
            fee_history_report_customer_recipients_temp = Configuration.objects.filter(name=config_name, value_name='Fee history report customer recipients', environment=environment).first()
            if fee_history_report_customer_recipients_temp is None:
                fee_history_report_customer_recipients_temp = Configuration.objects.filter(name=config_name, value_name='Fee history report customer recipients').first()
            configs.FEE_HISTORY_REPORT_CUSTOMER_RECIPIENTS = fee_history_report_customer_recipients_temp.array_value
        except:
            print('There was some error when loading Report email data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting Report email data failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
                
    # load PNR parser tools data
    @staticmethod
    def load_pnr_parser_tool_data():
        config_name = 'PNR Parser Tools'
        try:
            configs.PNR_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='PNR identifier').first().array_value
            configs.MAIN_PNR_TYPE = Configuration.objects.filter(name=config_name, value_name='PNR type').first().array_value
            configs.DUPLICATE_PNR_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Duplicate PNR identifier').first().array_value
            configs.SPLIT_PNR_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Split PNR identifier').first().array_value
            configs.TO_BE_EXCLUDED_LINE = Configuration.objects.filter(name=config_name, value_name='To be excluded line').first().array_value
            configs.CONTACT_TYPES = Configuration.objects.filter(name=config_name, value_name='Contact types').first().array_value
            configs.CONTACT_TYPE_NAMES = Configuration.objects.filter(name=config_name, value_name='Contact type names').first().dict_value
            configs.TICKET_LINE_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Ticket line identifier').first().array_value
            configs.SECOND_DEGREE_TICKET_LINE_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Second degree ticket line identifier').first().array_value
            configs.REMARK_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='Remark identifier').first().array_value
            configs.PNR_PASSENGER_DESIGNATIONS = Configuration.objects.filter(name=config_name, value_name='Passenger designations').first().array_value
            configs.POSSIBLE_COST_CURRENCY = Configuration.objects.filter(name=config_name, value_name='Possible cost currency').first().array_value
            configs.AM_H_LINE_IDENTIFIER = Configuration.objects.filter(name=config_name, value_name='AM H line identifier').first().array_value
        except:
            print('There was some error when loading PNR parser tool data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting PNR parser tool data failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
                
    @staticmethod
    def load_absolute_path_for_service_runner():
        PATH_DIR = {
            'test': '',
            # 'test':'/',
            'prod': ''
        } 
        
        configs.ABSOLUTE_PATH_SERVICE_RUNNER = PATH_DIR
        
    @staticmethod
    def load_all_coutries():
        try:
            countries = Country.objects.values("name").order_by("name")
            configs.COUTRIES_DATA = countries
        except:
            print('There was some error when loading countries data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting all coutries data failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
                
    @staticmethod
    def load_all_departments():
        try:
            departments = Department.objects.values("nom", "code").order_by("nom")
            configs.DEPARTMENTS_FRANCE = departments
        except:
            print('There was some error when loading departments data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting all departments data failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
                
    @staticmethod
    def load_all_municipalities():
        try:
            municipalities  =   Municipality.objects.values(
                                    "nom", "code_departement", "codes_postaux"
                                ).order_by("nom")
            configs.MUNICIPALITIES_FRANCE = municipalities
        except:
            print('There was some error when loading municipalities data. See error.txt for details.')
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Getting all municipalities data failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
                
                
    # load a chain of configs
    def load_config(self):
        print('Loading configuration ...')
        self.load_company_info()
        self.load_file_protocol()
        self.load_email_source()
        self.load_emd_parser_tool_data()
        self.load_tst_parser_tool_data()
        self.load_zenith_parser_tool_data()
        self.load_zenith_parser_receipt_tool_data()
        self.load_ticket_parser_tool_data()
        self.load_fee_request_tool_data()
        self.load_report_email_data()
        self.load_pnr_parser_tool_data()
        self.load_absolute_path_for_service_runner()
        self.load_all_coutries()
        self.load_all_departments()
        self.load_all_municipalities()
        print('Configuration loaded.')