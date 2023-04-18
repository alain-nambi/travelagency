from asyncio.windows_events import NULL
import os
import pytz
import traceback
from datetime import datetime
from datetime import timedelta


from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.utilities.PnrOnlyParser import *
from AmadeusDecoder.models.utilities.Notifications import Notification
from AmadeusDecoder.utilities.AmadeusParser import *
from AmadeusDecoder.utilities.ZenithParser import *

_e_ticket_possible_format_ = ['e-ticket', 'e‐ĕcket', 'e‐韜���cket', 'e‐⁛cket', 'e‐�cket', 'e‐଀cket']
_passenger_types_ = ['Adulte(s)', 'Enfant(s)', 'Bébé(s)']

class AmadeusNotification():

    def get_notification_pnr_status(self, normalized_file):
        pnr_status = 'Non émis'
        pnr_status_value = 1
        
        for line in normalized_file:
            temp = line.split(" ")
            if len(temp) > 2 and temp[0].isnumeric() == True:
                # all phone contacts and email
                if temp[1].startswith('FA'):
                    pnr_status = 'Emis'
                    pnr_status_value = 0
                    break

        return pnr_status, pnr_status_value

    def get_pnr_number(self, file_content):
        pnrDetailRow = ''
        for i in range(len(file_content)):
            if(file_content[i].startswith("RP")):
                pnrDetailRow = file_content[i]
                 
        # new method
        header_with_no_space = []
        for detail_row in pnrDetailRow.split(' '):
            if detail_row != '':
                header_with_no_space.append(detail_row)
        
        pnr_number = header_with_no_space[len(header_with_no_space) - 1]
        user_gds_id = header_with_no_space[len(header_with_no_space) - 3].split('/')[0]

        return pnr_number, user_gds_id



    def get_pnr_ticket_number(self, normalized_file):
        ticket_lines = []
        ticket_number = []
        for line in normalized_file:
            temp = line.split(" ")
            if len(temp) > 2 and temp[0].isnumeric():
                if temp[1] == 'FA' and (temp[2] == 'PAX' or temp[2] == 'INF'):
                    ticket_lines.append(line)
        
        for ticket in ticket_lines:
            info_part = ticket.split(' ')[3:]
            ticket_number.append(info_part[0].split('/')[0].replace('-', ''))

        return ticket_number


    def get_pnr_ticket_only(self, ticket_info_line):
        pnr_number = ''
        ticket_number = []
        for temp in ticket_info_line.split(' '):
            if temp.startswith('TKT'):
                ticket_number.append(temp.split('-')[1])
            elif temp.startswith('LOC'):
                pnr_number = temp.split('-')[1]

        return ticket_number, pnr_number



    def check_emd_pnr(self, ticket_info_line):
        pnr_number = ''
        ticket_number = []
        for temp in ticket_info_line.split(' '):
            if temp.startswith('EMD'):
                ticket_number.append(temp.split('-')[1])
            elif temp.startswith('LOC'):
                pnr_number = temp.split('-')[1]

        return pnr_number, ticket_number
    


    def save_notification_data(self, file_list):
        amadeus_parser = AmadeusParser()
        pnr_only_parser = PnrOnlyParser()
        message = ''

        for file in file_list:
            amadeus_parser.set_path(file)
            contents = amadeus_parser.read_file()
            needeed_contents = amadeus_parser.needed_content(contents)
            try:
                normalized_file = pnr_only_parser.normalize_file(needeed_contents)
                pnr_number, user_gds_id = self.get_pnr_number(contents)
                user_id = User.objects.get(gds_id=user_gds_id)
                pnr_status = self.get_notification_pnr_status(normalized_file)
                notif_already_exit = Notification.objects.filter(document_number=pnr_number)
                if pnr_status == 'Emis':
                    if len(contents) > 2:
                        if contents[1].startswith('RP'):
                            tickets_number = self.get_pnr_ticket_number(normalized_file)
                            if not notif_already_exit.exists():
                                message = "Un nouveau PNR a été créé : {}".format(pnr_number)
                                notification = Notification(document_number=pnr_number, is_read=False, user_id=user_id.id, message=message, document_parent=False)
                            else:
                                pass
                            notification.save()
                    elif contents[0].startswith('TKT'):
                        tickets_number, pnr_number = self.get_pnr_ticket_only(needeed_contents)
                        message = "Un nouveau billet a été créé"
                        for ticket in tickets_number:
                            notif_tickets = Notification.objects.filter(document_number=ticket)
                            if notif_tickets.exists():
                                notif_tickets.update(document_number=ticket, document_parent=pnr_number)
                                

            except Exception as e:
                print("Erreur détectée: {}".format(e))

            

class ZenithNotification():

    def get_pnr_number(self, file_content):
        pnr_number = ''
        if len(file_content) == 0:
            # pnr is not issued
            1
        else:
            for i in range(len(file_content)):
                if file_content[i].startswith('Dossier N'):
                    if len(file_content[i-1]) == 6:
                        pnr_number = file_content[i-1]
                    else:
                        pnr_number = file_content[i-1]
        
        return pnr_number

    def get_ticket_number(self, content):
        index_start = 0
        index_end = 0
        passenger_index = []
        tickets = []
        ticket_number = ''
        for i in range(len(content)):
            if content[i] == 'Nom du passager' and content[i + 1] == 'Numéro de billet':
                index_start = i + 6
            elif content[i] in _e_ticket_possible_format_:
                index_end = i
        
        for i in range(index_start, index_end):
            if content[i] in _passenger_types_:
                passenger_index.append(i)

        pax_number = 1
        for index in passenger_index:
            if content[index - 1].isnumeric():
                if content[index + 3] in _e_ticket_possible_format_ or content[index + 4].isnumeric():
                    ticket_number = content[index - 1]
                if content[index + 2] in _e_ticket_possible_format_ or content[index + 3].isnumeric():
                    ticket_number = content[index - 1]
            if content[index - 2].isnumeric():
                if content[index + 3] in _e_ticket_possible_format_ or content[index + 4].isnumeric():
                    ticket_number = content[index - 2]
                if content[index + 2] in _e_ticket_possible_format_ or content[index + 3].isnumeric():
                    ticket_number = content[index - 2]
            tickets.append(ticket_number)

        return tickets

    
    def save_notification_data(self, file_list):
        notification = Notification()
        for file in file_list:
            zenith_parser = ZenithParser()
            for temp_file in file:
                zenith_parser.set_path(temp_file)
                try:
                    content = zenith_parser.read_file()
                    pnr_number = self.get_pnr_number(content)
                    tickets = self.get_ticket_number(content)
                    if tickets == [] or tickets == '':
                        notification.is_pnr = False
                        notification.is_read = False
                        notification.document_number = pnr_number
                except Exception as e:
                    print("Une érreur a été detectée: {}".format(e))

