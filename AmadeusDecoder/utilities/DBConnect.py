'''
Created on 27 Feb 2023

@author: Famenontsoa
'''
import psycopg2
import os
import datetime
import traceback

from django.conf import settings

class DBConnect():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    @staticmethod
    def db_connect():
        conn = None
        try:
            database_settings = settings.DATABASES['default']
            database_user = database_settings['USER']
            database_password = database_settings['PASSWORD']
            database_name = database_settings['NAME']
            database_host = database_settings['HOST']
            database_port = database_settings['PORT']
            
            conn = psycopg2.connect(
                database=database_name, user=database_user, password=database_password, host=database_host, port=database_port
            )
        except:
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Database connection error.')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
        finally:
            return conn