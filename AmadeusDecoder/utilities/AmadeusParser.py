'''
Created on 31 Aug 2022

@author: Famenontsoa
'''
import traceback
import datetime
import time
import pytz

import os
import django

try:
    from AmadeusDecoder.utilities.SendMail import Sending
except:
    pass

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'DjangoTravelAgency.settings'
)
django.setup()

from AmadeusDecoder.utilities.PnrOnlyParser import PnrOnlyParser
from AmadeusDecoder.utilities.TicketOnlyParser import TicketOnlyParser
from AmadeusDecoder.utilities.PnrCostParser import PnrCostParser
from AmadeusDecoder.utilities.EMDOnlyParser import EMDOnlyParser
from AmadeusDecoder.utilities.TjqOnlyParser import TjqOnlyParser
from AmadeusDecoder.utilities.ServiceFeeDecreaseResponseParser import ServiceFeeDecreaseResponseParser

class AmadeusParser(PnrOnlyParser, TicketOnlyParser, PnrCostParser, EMDOnlyParser, TjqOnlyParser, ServiceFeeDecreaseResponseParser):
    '''
    classdocs
    '''
    
    __path = ''
    __email_date = None
    __is_archived = False

    def __init__(self):
        '''
        Constructor
        '''
        
    def get_path(self): return self.__path
    def get_email_date(self): return self.__email_date
    def get_is_archived(self): return self.__is_archived
     
    def set_path(self, path):
        if path != '' and path is not None:
            self.__path = path
        else:
            raise ValueError('Path cannot be none')
        
    def set_email_date(self, email_date):
        temp_date = datetime.datetime.now()
        date_utc = datetime.datetime(temp_date.year, temp_date.month, temp_date.day, temp_date.hour, temp_date.minute, temp_date.second, temp_date.microsecond, pytz.UTC)
    
        try:
            date_utc = datetime.datetime(email_date.year, email_date.month, email_date.day, email_date.hour, email_date.minute, email_date.second, email_date.microsecond)
            REMOTE_TIME_ZONE_OFFSET = +3 * 60 * 60
            timestamp = time.mktime(date_utc.timetuple()) + REMOTE_TIME_ZONE_OFFSET
            date_utc = datetime.datetime.fromtimestamp(timestamp, pytz.UTC)
        except Exception as e:
            print(e)
        
        self.__email_date = date_utc
        
    def set_is_archived(self, is_archived_status):
        self.__is_archived = is_archived_status
    
    # read a pnr
    def read_file(self):
        file = None
        try:
            file = open(self.get_path(), "r+", encoding="utf-8")
            content = file.readlines()
            contents = []
            for line in content:
                if line != '\n':
                    contents.append(line.strip())
            return contents[3:] # Remove subject and plain text flag
        except:
            traceback.print_exc()
        finally:
            if file is not None:
                file.close()

    # get needed content
    def needed_content(self, file_content):
        neededContent = []
        for a in range(len(file_content)):
            if(file_content[a].startswith("â€¢") == False and file_content[a].startswith("•") == False):
                if((file_content[a].startswith(")>") or file_content[a].startswith(">")) and a > 0):
                    break
                neededContent.append(file_content[a])    
        return neededContent
    
    # Zenith not issued
    def parse_not_issued_zenith(self, needed_content):
        from AmadeusDecoder.utilities.ZenithParser import ZenithParser
        temp_zenith_parser = ZenithParser()
        temp_zenith_parser.set_email_date(self.get_email_date())
        temp_zenith_parser.set_path(self.get_path())
        temp_zenith_parser.get_pnr_details(needed_content, 'Non émis', self.get_email_date())
    
    '''Save data according to its type'''

    def save_data(self, file_list):
        for file in file_list:
            temp = AmadeusParser()
            temp.set_path(file['file_path'])
            temp.set_email_date(file['email_date'])
            contents = temp.read_file()
            needed_content = temp.needed_content(contents)
            # save pnr data
            if len(contents) > 0:
                # if contents[0].startswith('TKT'):
                #     try:
                #         temp.parse_ticket(needed_content, temp.get_email_date())
                #     except Exception as e:
                #         print('File (Ticket) with error: ' + str(temp.get_path()))
                #         with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                #             error_file.write('{}: \n'.format(datetime.datetime.now()))
                #             error_file.write('File (Ticket) with error: {} \n'.format(str(temp.get_path())))
                #             traceback.print_exc(file=error_file)
                #             error_file.write('\n')
                #         if (str(e) == "connection already closed"):
                #             Sending.send_email_pnr_parsing(temp.get_path())
                #         continue
                # elif contents[0].startswith('EMD'):
                #     try:
                #         temp.parse_emd(needed_content, temp.get_email_date())
                #     except Exception as e:
                #         print('File (EMD) with error: ' + str(temp.get_path()))
                #         with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                #             error_file.write('{}: \n'.format(datetime.datetime.now()))
                #             error_file.write('File (EMD) with error: {} \n'.format(str(temp.get_path())))
                #             traceback.print_exc(file=error_file)
                #             error_file.write('\n')
                #         if (str(e) == "connection already closed"):
                #             Sending.send_email_pnr_parsing(temp.get_path())
                #         continue
                # elif contents[0].startswith('TST'):
                #     try:
                #         temp.parse_tst(needed_content)
                #     except Exception as e:
                #         print('File (TST) with error: ' + str(temp.get_path()))
                #         with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                #             error_file.write('{}: \n'.format(datetime.datetime.now()))
                #             error_file.write('File (TST) with error: {} \n'.format(str(temp.get_path())))
                #             traceback.print_exc(file=error_file)
                #             error_file.write('\n')
                #         if (str(e) == "connection already closed"):
                #             Sending.send_email_pnr_parsing(temp.get_path())
                #         continue
                # elif contents[0].startswith('FEE MODIFY REQUEST'):
                #     try:
                #         temp.sf_decrease_request_update(needed_content)
                #     except:
                #         print('File (REQUEST) with error: ' + str(file))
                #         with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                #             error_file.write('{}: \n'.format(datetime.datetime.now()))
                #             error_file.write('File (REQUEST) with error: {} \n'.format(str(temp.get_path())))
                #             traceback.print_exc(file=error_file)
                #             error_file.write('\n')
                #         if (str(e) == "connection already closed"):
                #             Sending.send_email_pnr_parsing(temp.get_path())
                #         continue
                if contents[0].startswith('AGY'): # TJQ
                    try:
                        temp.parse_tjq(needed_content)
                    except Exception as e:
                        print('File (TJQ) with error: ' + str(temp.get_path()))
                        with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                            error_file.write('{}: \n'.format(datetime.datetime.now()))
                            error_file.write('File (TJQ) with error: {} \n'.format(str(temp.get_path())))
                            traceback.print_exc(file=error_file)
                            error_file.write('\n')
                        if (str(e) == "connection already closed"):
                            Sending.send_email_pnr_parsing(temp.get_path())
                        continue
                else:
                    for j in range(len(contents)):
                        if contents[j].startswith('RPP'):
                            temp.set_is_archived(True)
                            continue
                        if contents[j].startswith('RP') and not contents[j].startswith('RPP'):
                            try:
                                temp.parse_pnr(contents[j:], needed_content, temp.get_email_date(), all_content_information=contents)
                                break
                            except Exception as e:
                                print('File (PNR Altea) with error: ' + str(temp.get_path()))
                                with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                                    error_file.write('File (PNR Altea) with error: {} \n'.format(str(temp.get_path())))
                                    traceback.print_exc(file=error_file)
                                    error_file.write('\n')
                                if (str(e) == "connection already closed"):
                                    Sending.send_email_pnr_parsing(temp.get_path())
                                continue
                        if contents[j].startswith('VOTRE NUMERO DE DOSSIER'):
                            try:
                                needed_content = contents[j:]
                                temp.parse_not_issued_zenith(needed_content)
                                break
                            except Exception as e:
                                print('File (EWA) with error: ' + str(temp.get_path()))
                                with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                                    error_file.write('File (TST) with error: {} \n'.format(str(temp.get_path())))
                                    traceback.print_exc(file=error_file)
                                    error_file.write('\n')
                                if (str(e) == "connection already closed"):
                                    Sending.send_email_pnr_parsing(temp.get_path())
                                continue
                        if contents[j].startswith('EMD'):
                            try:
                                temp.parse_emd(temp.needed_content(contents[j:]), temp.get_email_date())
                                break
                            except:
                                print('File (EMD) with error: ' + str(temp.get_path()))
                                with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                                    error_file.write('File (EMD) with error: {} \n'.format(str(temp.get_path())))
                                    traceback.print_exc(file=error_file)
                                    error_file.write('\n')
                                if (str(e) == "connection already closed"):
                                    Sending.send_email_pnr_parsing(temp.get_path())
                                continue
                        if contents[j].startswith('TKT'):
                            try:
                                temp.parse_ticket(temp.needed_content(contents[j:]), temp.get_email_date())
                                break
                            except:
                                print('File (Ticket) with error: ' + str(temp.get_path()))
                                with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                                    error_file.write('File (Ticket) with error: {} \n'.format(str(temp.get_path())))
                                    traceback.print_exc(file=error_file)
                                    error_file.write('\n')
                                if (str(e) == "connection already closed"):
                                    Sending.send_email_pnr_parsing(temp.get_path())
                                continue
                        if contents[j].startswith('TST'):
                            try:
                                temp.parse_tst(temp.needed_content(contents[j:]))
                                break
                            except:
                                print('File (TST) with error: ' + str(temp.get_path()))
                                with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                                    error_file.write('File (TST) with error: {} \n'.format(str(temp.get_path())))
                                    traceback.print_exc(file=error_file)
                                    error_file.write('\n')
                                if (str(e) == "connection already closed"):
                                    Sending.send_email_pnr_parsing(temp.get_path())
                                continue
                        if contents[j].startswith('FEE MODIFY REQUEST'):
                            try:
                                temp.sf_decrease_request_update(temp.needed_content(contents[j:]))
                                break
                            except:
                                print('File (REQUEST) with error: ' + str(temp.get_path()))
                                with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                                    error_file.write('File (REQUEST) with error: {} \n'.format(str(temp.get_path())))
                                    traceback.print_exc(file=error_file)
                                    error_file.write('\n')
                                if (str(e) == "connection already closed"):
                                    Sending.send_email_pnr_parsing(temp.get_path())
                                continue
                        
    