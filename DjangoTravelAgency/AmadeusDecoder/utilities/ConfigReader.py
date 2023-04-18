'''
Created on 16 Nov 2022

@author: Famenontsoa
'''
import os
import datetime
import django
import traceback

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'DjangoTravelAgency.settings'
)
django.setup()

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