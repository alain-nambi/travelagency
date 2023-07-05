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
                error_file.write('Getting company name failed. \n')
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
                error_file.write('Getting company name failed. \n')
                traceback.print_exc(file=error_file)
                error_file.write('\n')