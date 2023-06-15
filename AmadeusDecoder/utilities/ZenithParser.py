'''
Created on 3 Oct 2022

@author: Famenontsoa
'''
import email.utils
import os
import django
import time
import datetime
import traceback
import pytz
import decimal

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'DjangoTravelAgency.settings'
)
django.setup()

from django.db import transaction

from AmadeusDecoder.utilities.PdfTextExtractor import PdfTextExtractor
from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.pnr.Passenger import Passenger
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.pnr.PnrPassenger import PnrPassenger
from AmadeusDecoder.models.pnrelements.PnrAirSegments import PnrAirSegments
from AmadeusDecoder.models.pnrelements.Airline import Airline
from AmadeusDecoder.models.pnrelements.Airport import Airport
from AmadeusDecoder.models.invoice.TicketPassengerSegment import TicketPassengerSegment,\
    OtherFeeSegment
from AmadeusDecoder.models.pnrelements.ConfirmationDeadline import ConfirmationDeadline
from AmadeusDecoder.models.invoice.InvoiceDetails import InvoiceDetails
from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.models.invoice.Fee import OthersFee

_passenger_types_ = ['Adulte(s)', 'Enfant(s)', 'Bébé(s)', 'Mineur(s) non accompagné']
_passenger_designations_ = ['M.', 'Mme', 'Enfant', 'Bébé', 'Mlle', 'Ms.']
_currencies_ = ['EUR']
_e_ticket_possible_format_ = ['e-ticket', 'e‐ĕcket', 'e‐韜���cket', 'e‐⁛cket', 'e‐�cket', 'e‐଀cket', 'e‐෶���cket', 'e‐➄cket', 'e‐ᬘ���cket', 'e‐痴���cket']
_itinerary_header_possible_format_ = [['Itinéraire', 'Vol', 'Enregistrement', 'De', 'A', 'Départ', 'Arrivée CabineEscales'],
                                      ['Itinéraire', 'Vol', 'Enregistrement', 'De', 'A', 'Départ', 'Arrivée', 'CabineEscales'],
                                      ['Itinéraire', 'Vol', 'Enregistrement', 'De', 'A', 'Départ', 'Arrivée', 'Cabine Escales'],
                                      ['Itinéraire', 'Vol', 'Enregistrement', 'De', 'A', 'Départ', 'Arrivée', 'Cabine', 'Escales']]
_header_names_ = ['Itinéraire', 'Détails du tarif', 'Conditions tarifaires', 'Reçu de paiement']
_service_carrier_ = ['ZD', 'TZ']
_months_ = {'janv':'01', 'févr':'02', 'mars':'03', 'avr':'04', 'mai':'05', 'juin':'06', 'juil':'07', 'août':'08', 'sept':'09', 'oct':'10', 'nov':'11', 'déc':'12'}
_months_type_2_ = {'janvier':'01', 'février':'02', 'mars':'03', 'avril':'04', 'mai':'05', 'juin':'06', 'juillet':'07', 'août':'08', 'septembre':'09', 'octobre':'10', 'novembre':'11', 'décembre':'12'}
_week_days_ = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']
_AIRPORT_AGENCY_CODE_ = ['DZAUU000B']
_CURRENT_TRAVEL_AGENCY_IDENTIFIER_ = ['Issoufali', 'ISSOUFALI', 'Mayotte ATO']

class ZenithParser():
    '''
    classdocs
    '''
    
    __path = ''
    __main_txt_path = ''
    __email_date = None

    def __init__(self):
        '''
        Constructor
        '''
        
    def get_path(self): return self.__path
    def get_email_date(self): return self.__email_date
    def get_main_txt_path(self): return self.__main_txt_path
    
    def set_path(self, path):
        if path != '' and path is not None:
            self.__path = path
        else:
            raise ValueError('Path cannot be none')
    
    def set_main_txt_path(self, txt_path):
        if txt_path != '' and txt_path is not None:
            self.__main_txt_path = txt_path
        else:
            raise ValueError('Main txt path cannot none')
    
    """def set_email_date(self, email_date):
        temp_date = datetime.datetime.now()
        if email_date != '' and email_date is not None:
            try:
                date = email.utils.parsedate(email_date)
                REMOTE_TIME_ZONE_OFFSET = +6 * 60 * 60
                timestamp = time.mktime(date) + REMOTE_TIME_ZONE_OFFSET
                self.__email_date = datetime.datetime.fromtimestamp(timestamp, pytz.UTC)
            except Exception:
                self.__email_date = datetime.datetime(temp_date.year, temp_date.month, temp_date.day, temp_date.hour, temp_date.minute, temp_date.second, temp_date.microsecond, pytz.UTC)
        else:
            self.__email_date = datetime.datetime(temp_date.year, temp_date.month, temp_date.day, temp_date.hour, temp_date.minute, temp_date.second, temp_date.microsecond, pytz.UTC)
    """

    """def set_email_date(self, email_date):
        temp_date = datetime.datetime.now()
        date_utc = datetime.datetime(temp_date.year, temp_date.month, temp_date.day, temp_date.hour, temp_date.minute, temp_date.second, temp_date.microsecond, pytz.UTC)
    
        try:
            date_utc = datetime.datetime(email_date.year, email_date.month, email_date.day, email_date.hour, email_date.minute, email_date.second, email_date.microsecond, pytz.UTC)
        except Exception:
            pass
        
        self.__email_date = date_utc"""

    def set_email_date(self, email_date):
        temp_date = datetime.datetime.now()
        date_utc = datetime.datetime(temp_date.year, temp_date.month, temp_date.day, temp_date.hour, temp_date.minute, temp_date.second, temp_date.microsecond, pytz.UTC)
    
        try:
            date_utc = datetime.datetime(email_date.year, email_date.month, email_date.day, email_date.hour, email_date.minute, email_date.second, email_date.microsecond)
            REMOTE_TIME_ZONE_OFFSET = +3 * 60 * 60
            timestamp = time.mktime(date_utc.timetuple()) + REMOTE_TIME_ZONE_OFFSET
            date_utc = datetime.datetime.fromtimestamp(timestamp, pytz.UTC)
        except Exception:
            pass
        
        self.__email_date = date_utc



    # look for PDF parts when PNR has multiple page with multiple date
    # Get only the last part as it is the most recent update on EWA PNR
    def get_most_recent_pnr(self, content):
        itinerary_index = []
        content_parts = []
        try:
            for i in range(len(content)):
                if content[i].startswith("Itinéraire"):
                    itinerary_index.append(i)
            
            for i in range(len(itinerary_index)):
                if i < len(itinerary_index) - 1:
                    content_parts.append(content[itinerary_index[i]:itinerary_index[i+1]])
                else:
                    content_parts.append(content[itinerary_index[i]:])
            
            # return content[itinerary_index[-1]:]
            if len(content_parts) == 0:
                raise "Pass process"
            return content_parts
        except:
            content_parts.append(content)
            return content_parts
    
    # read the file
    def read_file(self):
        content = []
        if self.get_path().split('.')[len(self.get_path().split('.')) - 1] == 'pdf':
            pdf_extractor = PdfTextExtractor()
            pdf_extractor.set_path(self.get_path())
            content = pdf_extractor.get_text_from_pdf()
            content = self.get_most_recent_pnr(content)
        return content
    
    # fee subjection status
    def check_fee_subjection_status(self, pnr, other_fee):
        emitter = pnr.get_emit_agent()
        if emitter is not None:
            if emitter.office.code in _AIRPORT_AGENCY_CODE_:
                other_fee.is_subjected_to_fee = False
    
    # Get PNR number
    # Get Invoice cost
    # Get Ticket
    # Get Itinerary    
    # Get passenger    
    
    # get not emitted pnr detail
    def get_not_emitted_pnr_details(self, pnr, content):
        pnr_number = ''
        for element in content:
            if element.startswith('VOTRE NUMERO DE DOSSIER'):
                if len(element.split(':')) > 1:
                    pnr_number = element.split(':')[1].strip()
                    break
        
        if pnr_number != '':
            pnr.number = pnr_number
    
    # get not emitted pnr passengers
    def get_not_emitted_pnr_passengers(self, pnr, content):
        passenger_lines = []
        
        start_index = 0
        end_index = 0
        for j in range(len(content)):
            if content[j].startswith('Noms des passagers'):
                start_index = j
                break
        for j in range(len(content)):
            if content[j].startswith('Votre réservation :'):
                end_index = j
                break
        
        for i in range(start_index, end_index):
            passenger_lines.append(content[i])
        
        pax_order = 1
        for passenger_line in passenger_lines:
            temp_passenger_obj = Passenger()
            temp_passenger = passenger_line.strip()
            if passenger_line == passenger_lines[0]:
                temp_passenger = passenger_line.split(':')[1].strip()
            
            temp_passenger_split = temp_passenger.split(' ')
            if len(temp_passenger_split) > 1:
                if temp_passenger_split[0] in _passenger_designations_:
                    temp_passenger_obj.designation = temp_passenger_split[0]
                    temp_passenger_obj.name = temp_passenger.removeprefix(temp_passenger_split[0]).strip()
                    
                    temp_passenger_from_database = Passenger.objects.filter(name=temp_passenger_obj.name, designation=temp_passenger_obj.designation, passenger__pnr__id=pnr.id).first()
                    if temp_passenger_from_database is None:
                        temp_passenger_obj.order = 'P' + str(pax_order)
                        temp_passenger_obj.save()
                        
                        temp_pnr_passenger_obj = PnrPassenger()
                        temp_pnr_passenger_obj.passenger = temp_passenger_obj
                        temp_pnr_passenger_obj.pnr = pnr
                        temp_pnr_passenger_obj.save()
            
            pax_order += 1
            
    # date formatter
    def format_date(self, date_str): # example: ['19', 'décembre', '2022'] to 19/12/2022
        if len(date_str) == 3:
            return date_str[0] + '/' + str(_months_type_2_[date_str[1]]) + '/' + date_str[2]
        else:
            return ''
    
    # get not emitted PNR itinerary
    def get_not_emitted_pnr_itinerary(self, pnr, content):
        itinerary_lines = []
        pnr_air_segments = []
        
        start_index = 0
        end_index = 0
        for j in range(len(content)):
            if content[j].startswith('Votre réservation :'):
                start_index = j + 1
                break
        for j in range(len(content)):
            if content[j].startswith('Coût total de la réservation :'):
                end_index = j
                break
        
        for i in range(start_index, end_index):
            if content[i].startswith('*   Vol'):
                itinerary_lines.append(content[i])
        
        # normalize itinerary to get regular string separated by "-"
        for y in range(len(itinerary_lines)):
            temp_new_line_array = []
            temp_itinerary_line_split = itinerary_lines[y].split('-')
            for f in range(len(temp_itinerary_line_split)):
                if temp_itinerary_line_split[f].strip().startswith('*   Vol') or temp_itinerary_line_split[f].strip().startswith('Départ') or temp_itinerary_line_split[f].strip().startswith('Arrivée'):
                    temp_new_line_array.append(temp_itinerary_line_split[f].strip())
                else:
                    temp_new_line_array[len(temp_new_line_array) - 1] = temp_new_line_array[len(temp_new_line_array) - 1] + ' ' + temp_itinerary_line_split[f].strip()
            
            itinerary_lines[y] = temp_new_line_array
            
        itinerary_order = 1
        for itinerary_line in itinerary_lines:
            temp_segment_obj = PnrAirSegments()
            date_part = ''
            departure_time = ''
            arrival_time = ''
            
            # Flight info
            flight_info = itinerary_line[0]
            flight_info_split = flight_info.split(' ')
            index_of_flight = flight_info_split.index('Vol')
            # service carrier
            try:
                temp_airline = Airline.objects.filter(iata=flight_info_split[index_of_flight + 1]).first()
                if temp_airline is not None:
                    temp_segment_obj.servicecarrier = temp_airline
            except:
                pass
            # flight no
            if flight_info_split[index_of_flight + 2] == 'N°' or flight_info_split[index_of_flight + 2].startswith('N°'):
                temp_flight_no = ''
                if flight_info_split[index_of_flight + 2] == 'N°':
                    temp_flight_no = flight_info_split[index_of_flight + 3]
                elif flight_info_split[index_of_flight + 2].startswith('N°'):
                    temp_flight_no = flight_info_split[index_of_flight + 2].removeprefix('N°')
                temp_segment_obj.flightno = temp_flight_no
            # date part
            if flight_info_split[index_of_flight + 4] in _week_days_ or flight_info_split[index_of_flight + 3] in _week_days_:
                if flight_info_split[index_of_flight + 4] in _week_days_:
                    date_part = flight_info_split[index_of_flight + 5:]
                elif flight_info_split[index_of_flight + 3] in _week_days_:
                    date_part = flight_info_split[index_of_flight + 4:]
            # departure info
            departure_info = itinerary_line[1]
            departure_info_split = departure_info.split(' ')
            index_of_code_org_sep = departure_info_split.index('à')
            # code org
            try:
                temp_code_org = None
                if len(departure_info_split[index_of_code_org_sep - 1]) == 3:
                    temp_code_org = Airport.objects.filter(iata_code=departure_info_split[index_of_code_org_sep - 1]).first()
                elif len(departure_info_split[index_of_code_org_sep - 1]) > 3:
                    temp_code_org = Airport.objects.filter(name__contains=departure_info_split[index_of_code_org_sep - 1]).first()
                if temp_code_org is not None:
                        temp_segment_obj.codeorg = temp_code_org
                # departure time
                departure_time = departure_info_split[index_of_code_org_sep + 1]
            except:
                pass
            # arrival info
            arrival_info = itinerary_line[2]
            arrival_info_split = arrival_info.split(' ')
            index_of_cod_dest_sep = arrival_info_split.index('à')
            # code dest
            try:
                temp_code_dest = None
                if len(arrival_info_split[index_of_cod_dest_sep - 1]) == 3:
                    temp_code_dest = Airport.objects.filter(iata_code=arrival_info_split[index_of_cod_dest_sep - 1]).first()
                elif len(arrival_info_split[index_of_cod_dest_sep - 1]) > 3:
                    temp_code_dest = Airport.objects.filter(name__contains=arrival_info_split[index_of_cod_dest_sep - 1]).first()
                if temp_code_dest is not None:
                    temp_segment_obj.codedest = temp_code_dest
                # arrival time
                arrival_time = arrival_info_split[index_of_cod_dest_sep + 1]
            except:
                pass
            # departure and arrival datetime
            try:
                departure_datetime = datetime.datetime.strptime(self.format_date(date_part) + ' ' + departure_time + ':00', '%d/%m/%Y %H:%M:%S')
                arrival_datetime = datetime.datetime.strptime(self.format_date(date_part) + ' ' + arrival_time + ':00', '%d/%m/%Y %H:%M:%S')
                temp_segment_obj.departuretime = datetime.datetime(departure_datetime.year, departure_datetime.month, departure_datetime.day, departure_datetime.hour, departure_datetime.minute, departure_datetime.second, departure_datetime.microsecond, pytz.UTC)
                temp_segment_obj.arrivaltime = datetime.datetime(arrival_datetime.year, arrival_datetime.month, arrival_datetime.day, arrival_datetime.hour, arrival_datetime.minute, arrival_datetime.second, arrival_datetime.microsecond, pytz.UTC)
            except:
                pass
            
            temp_segment_obj.segmentorder = 'S' + str(itinerary_order)
            segment_checker = PnrAirSegments.objects.filter(servicecarrier=temp_segment_obj.servicecarrier, flightno=temp_segment_obj.flightno, codeorg=temp_segment_obj.codeorg, codedest=temp_segment_obj.codedest, pnr=pnr, departuretime=temp_segment_obj.departuretime, arrivaltime=temp_segment_obj.arrivaltime).first()
            if segment_checker is None:
                temp_segment_obj.pnr = pnr
                temp_segment_obj.save()
                pnr_air_segments.append(temp_segment_obj)
            itinerary_order += 1
        
        return pnr_air_segments
    
    # get opc
    def get_not_emitted_pnr_opc(self, pnr_airsegments, content):
        opc_line = ''
        for line in content:
            if line.startswith('Si vous ne payez pas votre réservation avant'):
                opc_line = line
                break
        
        for segment in pnr_airsegments:
            temp_segment_opc = ConfirmationDeadline()
            temp_segment_opc.free_flow_text = opc_line
            temp_segment_opc.segment = segment
            try:
                temp_opc_date = datetime.datetime.strptime(opc_line.removeprefix('Si vous ne payez pas votre réservation avant').removesuffix('(heure locale de DZA), celle-ci sera AUTOMATIQUEMENT ANNULÉE.').strip() + ':00', '%d/%m/%Y %H:%M:%S')
                temp_segment_opc.doc_date = datetime.datetime(temp_opc_date.year, temp_opc_date.month, temp_opc_date.day, temp_opc_date.hour, temp_opc_date.minute, temp_opc_date.second, temp_opc_date.microsecond, pytz.UTC)
            except:
                pass
            temp_segment_opc.type = 'OPC'
            temp_segment_opc.save()
    
    # get invoice (PNR) amount
    def get_not_emitted_pnr_fare(self, pnr, content):
        booking_cost = '0'
        for line in content:
            if line.startswith('Coût total de la réservation :'):
                booking_cost = line.removeprefix('Coût total de la réservation :').strip().replace(',', '.').removesuffix('\x80')
        temp_invoice_detail = InvoiceDetails.objects.filter(invoice__pnr=pnr).first()
        try:
            temp_invoice_detail.total = decimal.Decimal(booking_cost.replace(' ', ''))
        except:
            temp_invoice_detail.total = 0
        temp_invoice_detail.save()
    
    # read main text file
    def read_main_text_file(self):
        file = None
        try:
            file = open(self.get_main_txt_path(), "r+", encoding="utf-8", errors='replace')
            content = file.readlines()
            contents = []
            for line in content:
                if line != '\n':
                    contents.append(line.strip())
            return contents
        except:
            traceback.print_exc()
        finally:
            if file is not None:
                file.close()
    
    # get main text file path from pdf file path
    def get_txt_path_from_pdf(self, pdf_path):
        # file {'email_date': 'Mon, 21 Nov 2022 08:08:07 +0000', 'attachment': ['H:/Famenontsoa/Light/S5-S6/Stage/Project/TravelAgency/DjangoTravelAgency/EmailFetcher/utilities/attachments_dir/4678_issoufali.pnr@outlook.com/E-ticket 00CHUM-ANFAOUDINE RUN  .pdf']}
        needed_part = ''
        txt_folder_path = ''
        txt_path = ''
        if len(pdf_path.split("/")) > 1:
            needed_part = pdf_path.split("/")[-1]
            txt_folder_path = pdf_path.removesuffix(needed_part).removesuffix('/')
            txt_file_name = txt_folder_path.split("/")[-1]
            txt_path = txt_folder_path + "/" + txt_file_name + '.txt'
        else:
            needed_part = pdf_path.split("\\")[-1]
            txt_folder_path = pdf_path.removesuffix(needed_part).removesuffix('\\')
            txt_file_name = txt_folder_path.split("\\")[-1]
            txt_path = txt_folder_path + "\\" + txt_file_name + '.txt'
            
        return txt_path
    
    # for issued PNR: get PNR creator, emitter
    def get_creator_emitter(self):
        contents = self.read_main_text_file()
        to_list = ''
        subject = ''
        for line in contents:
            if line.startswith('To:'):
                to_list = email.utils.getaddresses(line.removeprefix('To:').strip().split(';'))
            if line.startswith('Subject:'):
                subject = line.removeprefix('Subject:').strip()
                break
        
        subject_split = subject.split('-')
        if len(subject_split) > 1:
            pnr_number_part_split = subject_split[1].split(' ')[-1]
            pnr_number = pnr_number_part_split.removesuffix('.')
            
            temp_pnr = Pnr.objects.filter(number=pnr_number).first()
            if temp_pnr is not None:
                if len(to_list) > 1:
                    temp_user = User.objects.filter(email=to_list[-1][1]).first()
                    if temp_user is not None and to_list[-1][1] != 'issoufali.pnr@outlook.com' and to_list[-1][1] != 'issoufali.pnr@outlook.com'.upper():
                        # assign creator agent
                        temp_pnr.agent = temp_user
                        temp_pnr.save()
                        # assign ticket emitter
                        pnr_tickets = Ticket.objects.filter(pnr=temp_pnr).all()
                        for ticket in pnr_tickets:
                            ticket.emitter = temp_user
                            ticket.save()
                    # else:
                    #     if to_list[-1][1] != 'issoufali.pnr@outlook.com' and to_list[-1][1] != 'issoufali.pnr@outlook.com'.upper():
                    #         temp_pnr.agent_code = to_list[-1][1]
                    #     else:
                    #         temp_pnr.agent_code = ''
                    #     temp_pnr.save()
    
    # EMD parsing
    def parse_emd(self, content, email_date):
        pnr_number = ''
        # opc = ''
        description = ''
        cost = 0
        ticket_number = ''
        is_emd = False
        for i in range(len(content)):
            line = content[i]
            if line.startswith('Référence PNR'):
                try:
                    is_emd = True
                    pnr_number = line.split(' ')[-1]
                except:
                    traceback.print_exc()
            if line.startswith('Date d\'expiration'):
                try:
                    # opc = content[i + 1]
                    ''''''
                except:
                    traceback.print_exc()
            if line.startswith('Commentaire'):
                try:
                    description = content[i + 1]
                except:
                    traceback.print_exc()
            if line.startswith('Montant'):
                try:
                    ticket_number = content[i + 2]
                    cost = decimal.Decimal(content[i + 1].split(' ')[0].replace(',', '.'))
                except:
                    traceback.print_exc()
        
        if pnr_number != '':
            temp_pnr = Pnr.objects.filter(number=pnr_number).first()
            if temp_pnr is None:
                new_pnr = Pnr()
                new_pnr.number = pnr_number
                new_pnr.status = 'Emis'
                new_pnr.type = 'EWA'
                new_pnr.status_value = 0
                new_pnr.state = 1
                new_pnr.system_creation_date = email_date
                new_pnr.save()
                temp_pnr = new_pnr
            
            temp_ticket = Ticket.objects.filter(number=ticket_number, pnr=temp_pnr).first()
            if temp_ticket is None and ticket_number != '':
                new_ticket = Ticket()
                new_ticket.number = ticket_number
                new_ticket.pnr = temp_pnr
                new_ticket.transport_cost = cost
                new_ticket.total = cost
                new_ticket.issuing_date = email_date
                new_ticket.ticket_description = description
                new_ticket.ticket_type = 'EMD'
                new_ticket.save()
        
        return is_emd
    
    # get pnr details / number
    def get_pnr_details(self, content, status, email_date):
        pnr = Pnr()
        pnr.type = 'EWA'
        # system_creation_date = datetime.datetime.now()
        # pnr.system_creation_date = datetime.datetime(system_creation_date.year, system_creation_date.month, system_creation_date.day, system_creation_date.hour, system_creation_date.minute, system_creation_date.second, system_creation_date.microsecond, pytz.UTC)
        pnr.system_creation_date = email_date
        if status == 'Non émis':
            pnr.status = 'Non émis'
            pnr.status_value = 1
            self.get_not_emitted_pnr_details(pnr, content)
            temp_pnr = Pnr.objects.filter(number=pnr.number).first()
            if temp_pnr is None:
                pnr.save()
            else:
                pnr = temp_pnr
            self.get_not_emitted_pnr_passengers(pnr, content)
            pnr_air_segments = self.get_not_emitted_pnr_itinerary(pnr, content)
            self.get_not_emitted_pnr_opc(pnr_air_segments, content)
            self.get_not_emitted_pnr_fare(pnr, content)
        else:
            pnr.status = 'Emis'
            pnr.status_value = 0
            pnr.state = 0
            for i in range(len(content)):
                if content[i].startswith('Dossier N'):
                    document_name_split = content[i].strip().split(' ')
                    if len(document_name_split) == 2:
                        if len(content[i-1]) == 6:
                            pnr.number = content[i-1]
                        else:
                            pnr.number = content[i-1]
                    elif len(document_name_split) > 2 and len(document_name_split[-1]) == 6:
                        pnr.number = document_name_split[-1]
            temp_pnr = Pnr.objects.filter(number=pnr.number).first()
            if temp_pnr is not None:
                temp_pnr.system_creation_date = email_date
                temp_pnr.status = 'Emis'
                temp_pnr.status_value = 0
                temp_pnr.state = 0
                return temp_pnr, True
                
        return pnr, False
    
    
    # normalize passenger and ticket
    def normalize_passenger(self, passenger_content):
        new_content = []
        for i in range(len(passenger_content)):
            skip = False
            # separate "passenger type" and "contact" eg: 'Adulte(s)+262639693300', 'INFT (ANDRIAMAHEFA/ASSIASHANYLA 20JUN21)Adulte(s)+33766742803'
            for psg_type in _passenger_types_:
                if passenger_content[i].startswith(psg_type) and passenger_content[i] != psg_type:
                    new_content.append(psg_type)
                    new_content.append(passenger_content[i].removeprefix(psg_type).strip())
                    skip = True
                elif len((passenger_content[i].strip()).split(psg_type)) > 1 and passenger_content[i].strip() != psg_type:
                    new_content.append((passenger_content[i].strip()).split(psg_type)[0].strip())
                    new_content.append(psg_type)
                    new_content.append((passenger_content[i].strip()).split(psg_type)[1].strip())
                    skip = True
            if not skip:
                new_content.append(passenger_content[i])
        
        # normalize passenger name
        new_content_passenger_name_assembled = []
        for i in range(len(new_content)):
            skip = False
            for psg_type in _passenger_designations_:
                # 'M. soloniaina jean francis', 'RAKOTONDRAMANANA', '7322415442815 INFT (RAKOTONDRAMANANA/YNAIA', '18DEC21)', 'Adulte(s)', '+262639215396', 'A22X460328'
                if i > 0:
                    if new_content[i-1].startswith(psg_type) and new_content[i-1] != psg_type:
                        if not new_content[i][0].isnumeric():
                            new_content_passenger_name_assembled.pop()
                            new_content_passenger_name_assembled.append(new_content[i-1].strip() + ' ' + new_content[i].strip())
                            skip = True
            if not skip:
                new_content_passenger_name_assembled.append(new_content[i])
        new_content = new_content_passenger_name_assembled
        
        # separate passenger with ticket number
        new_content_ticket_separated = []
        for i in range(len(new_content)):
            skip = False
            for psg_type in _passenger_types_:
                if new_content[i].strip() == psg_type:
                    if not new_content[i-1].strip().isnumeric() and len(new_content[i-1].strip()) > 13:
                        previous_element_space_split = new_content[i-1].split(' ')
                        
                        # 'Mme MARIE CHARLOTTE RAZAFIMANDIMBY 7322415445929', 'Adulte(s)'
                        if previous_element_space_split[0].strip() in _passenger_designations_:
                            new_content_ticket_separated.pop()
                            new_content_ticket_separated.append(new_content[i-1].removesuffix(previous_element_space_split[-1]).strip())
                            new_content_ticket_separated.append(previous_element_space_split[-1])
                            new_content_ticket_separated.append(psg_type)
                            skip = True
                        # 'Mme MARIE CHARLOTTE RAZAFIMANDIMBY 7322415445929', 'INFT (LANDRIO/KHAIRANELYA 06DEC21)', 'Adulte(s)'
                        # or 'Mme KAMARIA YOUSSOUF', '7322415447799', 'INFT (SAID/CAMELIA 24MAY22)', 'Adulte(s)',
                        else:
                            temp_head_element_space_split = new_content[i-2].split(' ')
                            if temp_head_element_space_split[0].strip() in _passenger_designations_ \
                                and temp_head_element_space_split[-1].strip().isnumeric():
                                new_content_ticket_separated.pop()
                                new_content_ticket_separated.pop()
                                new_content_ticket_separated.append(new_content[i-2].removesuffix(temp_head_element_space_split[-1]).strip())
                                new_content_ticket_separated.append(temp_head_element_space_split[-1])
                                new_content_ticket_separated.append(psg_type)
                                skip = True
                    # e.g: Mme MARIA HELENA MARCOS DO AMARAL 7322415433868INFT (DEBRITOAMARAL/AVAGABRIELLEHELENA', '03MAY21)', 'Adulte(s)'
                    elif not new_content[i-1].strip().isnumeric() and len(new_content[i-1].strip()) < 13:
                        temp_content_split_space = new_content[i-2].split(' ')
                        if temp_content_split_space[0] in _passenger_designations_:
                            temp_ticket_number = ''
                            for content_split in temp_content_split_space:
                                for word in content_split:
                                    if word.isdigit():
                                        temp_ticket_number += word
                                # stop when ticket number reached
                                if temp_ticket_number.isnumeric() and len(temp_ticket_number) > 9:
                                    break
                            temp_ticket_number_split = new_content[i-2].split(temp_ticket_number)
                            new_content_ticket_separated.pop()
                            new_content_ticket_separated.pop()
                            # passenger name
                            new_content_ticket_separated.append(temp_ticket_number_split[0].strip())
                            # ticket number
                            new_content_ticket_separated.append(temp_ticket_number)
                            # service part
                            if len(temp_ticket_number_split) > 1:
                                new_content_ticket_separated.append(" ".join(temp_ticket_number_split[1:]) + " " + new_content[i-1])
            if not skip:
                new_content_ticket_separated.append(new_content[i])
        
        new_content = new_content_ticket_separated
        
        # separate ticket number from services
        new_content_service_separated_ticket = []
        for i in range(len(new_content)):
            skip = False
            temp_part_split_space = new_content[i-1].split(' ')
            if temp_part_split_space[0] in _passenger_designations_:
                temp_ticket_number = new_content[i].split(' ')[0]
                if not new_content[i].isnumeric() and temp_ticket_number.isnumeric():
                    new_content_service_separated_ticket.append(temp_ticket_number)
                    new_content_service_separated_ticket.append(new_content[i].removeprefix(temp_ticket_number).strip())
                    skip = True
            if not skip:
                new_content_service_separated_ticket.append(new_content[i])
        
        new_content = new_content_service_separated_ticket
        
        new_content_fix_passenger = []
        to_be_skipped = None
        for i in range(len(new_content)):
            skip = False
            # append passenger name when separated
            for psg_designation in _passenger_designations_:
                if new_content[i].split(' ')[0].strip() == psg_designation:
                    if i < len(new_content) - 1:
                        if not new_content[i + 1].isnumeric() and not new_content[i + 1].startswith('N°'):
                            new_content_fix_passenger.append(new_content[i] + ' ' + new_content[i + 1])
                            skip = True
                            to_be_skipped = new_content[i + 1]
            
            if not skip and to_be_skipped != new_content[i] and not new_content[i].startswith('N°'):
                new_content_fix_passenger.append(new_content[i])
            if to_be_skipped == new_content[i]:
                to_be_skipped = None
        
        # fill service when none
        filtered_content = []
        for i in range(len(new_content_fix_passenger)):
            filtered_content.append(new_content_fix_passenger[i])
            if i < len(new_content_fix_passenger) - 1:
                if new_content_fix_passenger[i].isnumeric() and new_content_fix_passenger[i+1].strip() in _passenger_types_:
                    filtered_content.append('')
        
        # remove duplicate service
        duplicate_service_removed = []
        for i in range(len(filtered_content)):
            duplicate_service_removed.append(filtered_content[i])
            if filtered_content[i] in _passenger_types_:
                if not filtered_content[i-2].isnumeric():
                    service = filtered_content[i-2] + ' ' + filtered_content[i-1]
                    duplicate_service_removed.pop(i)
                    duplicate_service_removed.pop(i-1)
                    duplicate_service_removed.pop(i-2)
                    duplicate_service_removed.append(service)
                    duplicate_service_removed.append(filtered_content[i])
        
        # fill contact when none
        filtered_content_contact = []
        for i in range(len(duplicate_service_removed)):
            filtered_content_contact.append(duplicate_service_removed[i])
            # one passenger only and no contact
            if len(duplicate_service_removed) == 5:
                if filtered_content[i] in _passenger_types_:
                    filtered_content_contact.append('')
            elif len(duplicate_service_removed) > 6:
                if i < len(duplicate_service_removed) - 3:
                    if duplicate_service_removed[i] in _passenger_types_ and duplicate_service_removed[i+2].split(' ')[0] in _passenger_designations_:
                        filtered_content_contact.append('')
                elif i+2 == len(duplicate_service_removed) and duplicate_service_removed[i] in _passenger_types_:
                    filtered_content_contact.append('')
        
        if len(filtered_content_contact)%6 != 0:
            while len(filtered_content_contact)%6 != 0:
                filtered_content_contact.append('')
        
        
        # split passenger line by line
        passenger_lines = []
        j = 0
        for i in range(int(len(filtered_content_contact)/6)):
            passenger_lines.append(filtered_content_contact[j:j+6])
            j += 6
        
        return passenger_lines
    
    # get passengers / ticket numbers
    def get_passengers_tickets(self, content, pnr):
        passengers = []
        pnr_passengers = []
        tickets = []
        index_start = 0
        index_end = 0
        for i in range(len(content)):
            if content[i] == 'Nom du passager' and (content[i + 1] == 'Numéro de billet' or content[i + 1] == 'Numéro de billet Service(s)' or content[i + 1] == 'Numéro de billetService(s)' or (content[i + 1] == 'Numéro de' and content[i + 2] == 'billet' if i < len(content) - 3 else '')):
                if content[i] == 'Nom du passager' and content[i + 1] == 'Numéro de billet':
                    index_start = i + 6
                elif content[i] == 'Nom du passager' and (content[i + 1] == 'Numéro de billet Service(s)' or content[i + 1] == 'Numéro de billetService(s)'):
                    index_start = i + 5
                elif content[i] == 'Nom du passager' and (content[i + 1] == 'Numéro de' and content[i + 2] == 'billet' if i < len(content) - 3 else ''):
                    index_start = i + 7
                
                if index_start > 0:
                    if content[index_start].strip() == 'passeport':
                        index_start += 1
            elif content[i] in _e_ticket_possible_format_:
                index_end = i
                break
            elif content[i].startswith('Dossier N'):
                index_end = i - 2
                break
        
        def get_passenger_index(content, index_start, index_end):
            passenger_index = []
            for i in range(index_start, index_end):
                if content[i] in _passenger_types_:
                    passenger_index.append(i)
                elif content[i].split(' ')[0] in _passenger_types_ and len(content[i].split(' ')) > 1:
                    passenger_index.append(i)
                    temp_separated_value = content[i].split(' ')
                    new_content = []
                    for j in range(len(content)):
                        if j == i:
                            new_content.append(temp_separated_value[0])
                            new_content.append(temp_separated_value[1])
                        else:
                            new_content.append(content[j])
                    index_end += 1
                    return get_passenger_index(new_content, index_start, index_end)
                elif content[i].split(' ')[0] in _passenger_designations_ and content[i].split(' ')[-1].isnumeric():
                    passenger_index.append(i)
                    temp_separated_value = content[i].split(' ')
                    new_content = []
                    for j in range(len(content)):
                        if j == i:
                            new_content.append(content[i].removesuffix(temp_separated_value[-1]).strip())
                            new_content.append(temp_separated_value[-1])
                        else:
                            new_content.append(content[j])
                    index_end += 1
                    return get_passenger_index(new_content, index_start, index_end)
                else:
                    for passenger_type in _passenger_types_:
                        if content[i].startswith(passenger_type):
                            passenger_index.append(i)
                
            return content, passenger_index
        
        # content, passenger_index = get_passenger_index(content, index_start, index_end)
        print('PASSENGER_CONTENT', content[index_start: index_end])
        print('NEW_CONTENT', self.normalize_passenger(content[index_start: index_end]))
        
        new_content = self.normalize_passenger(content[index_start: index_end])
        pax_number = 1
        for content in new_content:
            try:
                temp_passenger_obj = Passenger()
                temp_pnr_passenger_obj = PnrPassenger()
                temp_ticket_obj = Ticket()
                
                # 'Nom du passager', 'Numéro de billet', 'Service(s)', 'Type', 'Contact', 'Numéro du passeport'
                if content[0].split(' ')[0] in _passenger_designations_:
                    temp_passenger_obj.name = content[0].removeprefix(content[0].split(' ')[0]).strip()
                    temp_passenger_obj.designation = content[0].split(' ')[0]
                else:
                    temp_passenger_obj.name = new_content[0]
                temp_passenger_obj.types = content[3]
                temp_passenger_obj.passeport = content[-1]
        
                temp_pnr_passenger_obj.passenger = temp_passenger_obj
                
                temp_ticket_obj.number = content[1]
                
                temp_passenger_obj.order = 'P' + str(pax_number)
                passengers.append(temp_passenger_obj)
                temp_pnr_passenger_obj.pnr = pnr
                pnr_passengers.append(temp_pnr_passenger_obj)
                temp_ticket_obj.pnr = pnr
                temp_ticket_obj.passenger = temp_passenger_obj
                temp_ticket_obj.ticket_type = 'TKT'
                tickets.append(temp_ticket_obj)
                               
                pax_number += 1
            except:
                traceback.print_exc()
            
        return passengers, pnr_passengers, tickets
    
    # get itinerary part
    def get_part(self, content, part_name): # Itinéraire or Détails du tarif or ...
        part = []
        start_index = 0
        for i in range(len(content)):
            if content[i] == part_name:
                start_index = i
                break
        i = 0
        while i < len(content):
            part.append(content[start_index + i])
            if content[start_index + i + 1] in _header_names_ and content[start_index + i + 1] != 'Reçu de paiement':
                break
            if start_index + i == len(content) - 2:
                break
            i += 1
            
        return part
    
    # get itinerary
    def get_itinerary(self, itinerary_part, pnr):
        service_carrier_indexes = []
        for airline in _service_carrier_:
            for i in range(len(itinerary_part)):
                    if itinerary_part[i].startswith(airline):
                        service_carrier_indexes.append(i)
        
        air_segments = []
        seg_order = 1
        for i in range(len(service_carrier_indexes)):
            temp_content = None
            if i < len(service_carrier_indexes) - 1:
                temp_content = itinerary_part[service_carrier_indexes[i]:service_carrier_indexes[i+1]]
            else:
                temp_content = itinerary_part[service_carrier_indexes[i]:]
            
            temp_content_1 = []
            for str_token in temp_content:
                temp_content_1 += str_token.split(' ')
            temp_content = temp_content_1
            
            temp_air_segment = PnrAirSegments()
            departuretime = None
            arrivaltime = None
            codeorg = None
            codedest = None
            segment_type = 'Flight'
            segmentorder = 'S' + str(seg_order)
            
            # get airline
            for carrier in _service_carrier_:
                if temp_content[0].startswith(carrier):
                    temp_air_segment.servicecarrier = Airline.objects.filter(iata=carrier).first()
                    temp_air_segment.flightno = temp_content[0].removeprefix(carrier)
                    break
            
            origin_destination = []
            departure_arrival = []
            
            index = 0
            for element in temp_content:
                # get origin and destination
                splitted_part_org_dest = element.split('(')
                for split in splitted_part_org_dest:
                    if split.endswith(')') and len(split.removesuffix(')')) == 3:
                        origin_destination.append(split.removesuffix(')'))
                # get departure and arrival datetime
                splitted_part_dep_arr = element.split('-')
                for split_dep_arr in splitted_part_dep_arr:
                    if split_dep_arr.removesuffix('.') in _months_:
                        day = splitted_part_dep_arr[0]
                        month = str(_months_[split_dep_arr.removesuffix('.')])
                        year = splitted_part_dep_arr[2]
                        hour = temp_content[index + 1].split(':')[0]
                        minute = temp_content[index + 1].split(':')[1]
                        date_format = datetime.datetime.strptime(year + month + day + ' ' + hour + ':' + minute + ':00', '%y%m%d %H:%M:%S')
                        temp_date = datetime.datetime(date_format.year, date_format.month, date_format.day, date_format.hour, date_format.minute, date_format.second, date_format.microsecond, pytz.UTC)
                        departure_arrival.append(temp_date)
                index += 1
            
            # origin / destination
            codeorg = origin_destination[0]
            codedest = origin_destination[1]
            try:
                temp_air_segment.codeorg = Airport.objects.get(iata_code=codeorg)
            except:
                Airport.objects.create(name='Unknown', iata_code=codeorg)
                temp_air_segment.codeorg = Airport.objects.get(iata_code=codeorg)
            try:
                temp_air_segment.codedest = Airport.objects.get(iata_code=codedest)
            except:
                Airport.objects.create(name='Unknown', iata_code=codedest)
                temp_air_segment.codedest = Airport.objects.get(iata_code=codedest)
            
            # departure / arrival
            departuretime = departure_arrival[0]
            arrivaltime = departure_arrival[1]
            temp_air_segment.departuretime = departuretime
            temp_air_segment.arrivaltime = arrivaltime
            temp_air_segment.segment_type = segment_type
            temp_air_segment.segmentorder = segmentorder
            temp_air_segment.pnr = pnr
            
            air_segments.append(temp_air_segment)
            seg_order += 1
            
        return air_segments
    
    # separate cost details per passenger type
    def separate_cost_per_passenger_type(self, segment_cost_line, passengers, air_segment, pnr):
        ticket_segments = []
        
        passenger_types_indexes = []
        passenger_type_part = []
        i = 0
        for element in segment_cost_line:
            if element in _passenger_types_:
                passenger_types_indexes.append(i)
            elif i < len(segment_cost_line) - 1:
                if (segment_cost_line[i] + ' ' + segment_cost_line[i + 1]) in _passenger_types_:
                    passenger_types_indexes.append(i + 1)
            i += 1
        
        # Get each part by passenger(s) type
        for index in range(len(passenger_types_indexes)):
            if index < len(passenger_types_indexes) - 1:
                passenger_type_part.append(segment_cost_line[passenger_types_indexes[index]:passenger_types_indexes[index+1]])
            else:
                passenger_type_part.append(segment_cost_line[passenger_types_indexes[index]:])
        
        # Get all related ticket segment
        for part in passenger_type_part:
            current_index = 0
            passenger_count = 0
            passengers_on_segment = []
            
            # check multiple passengers of the same type on the same segment
            for content_element in part:
                for passenger in passengers:
                    temp_passenger = Passenger.objects.filter(name=passenger.name, designation=passenger.designation, passenger__pnr=pnr).first()
                    if temp_passenger is not None:
                        passenger = temp_passenger
                    if content_element == passenger.name:
                        passengers_on_segment.append(passenger)
                        passenger_count += 1
                    if current_index < len(part) - 1:
                        if content_element + ' ' + part[current_index + 1] == passenger.name or content_element + part[current_index + 1] == passenger.name:
                            passengers_on_segment.append(passenger)
                            passenger_count += 1
                current_index += 1
            
            # get ticket segment and cost
            for content_element in part:
                # more than one passengers are on the same segment part with the same type
                if passenger_count > 1:
                    if content_element in _currencies_:
                        first_passenger_fare_index = part.index('EUR') + 1
                        fare_index = first_passenger_fare_index
                        tax_index = fare_index + passenger_count
                        total_index = tax_index + passenger_count
                        for passenger in passengers_on_segment:
                            temp_ticket_segment = TicketPassengerSegment()
                            temp_ticket_segment.ticket = passenger.ticket.last()
                            temp_ticket_segment.segment = air_segment
                            try:
                                temp_ticket_segment.fare = float(part[fare_index].replace(',','.'))
                                temp_ticket_segment.tax = float(part[tax_index].replace(',','.'))
                                temp_ticket_segment.total = float(part[total_index].replace(',','.'))
                            except:
                                temp_ticket_segment.fare = 0
                                temp_ticket_segment.tax = 0
                                temp_ticket_segment.total = 0
                            
                            fare_index += 1
                            tax_index += 1
                            total_index += 1
                            ticket_segments.append(temp_ticket_segment)
                        break
                # one passenger is on the segment part under one type
                elif passenger_count == 1:
                    first_passenger_fare_index = part.index('EUR') + 1
                    fare_index = first_passenger_fare_index
                    tax_index = fare_index + passenger_count
                    total_index = tax_index + passenger_count
                    
                    temp_ticket_segment = TicketPassengerSegment()
                    temp_ticket_segment.ticket = passengers_on_segment[0].ticket.last()
                    temp_ticket_segment.segment = air_segment
                    try:
                        temp_ticket_segment.fare = float(part[fare_index].replace(',','.'))
                        temp_ticket_segment.tax = float(part[tax_index].replace(',','.'))
                        temp_ticket_segment.total = float(part[total_index].replace(',','.'))
                    except:
                        temp_ticket_segment.fare = 0
                        temp_ticket_segment.tax = 0
                        temp_ticket_segment.total = 0
                    
                    ticket_segments.append(temp_ticket_segment)
                    break
        
        return ticket_segments
    
    # get ticket/segment cost details
    def get_ticket_segment_costs(self, cost_details_part, passengers, air_segments, pnr):
        segment_indexes = []
        ticket_segments = []
        for segment in air_segments:
            for i in range(len(cost_details_part)):
                # Itinerary can be: ['MJN ->', 'DZA'] or ['MJN -> DZA']
                temp_origin_destination_split = cost_details_part[i].split('➜')
                # if itinerary is like "['MJN -> DZA']"
                if len(temp_origin_destination_split) > 1:
                    if temp_origin_destination_split[0].strip() == segment.codeorg.iata_code and temp_origin_destination_split[1].strip() == segment.codedest.iata_code:
                        segment_indexes.append(i)
                # if itinerary is like "['MJN ->', 'DZA']"
                if cost_details_part[i].strip() == segment.codedest.iata_code:
                    if cost_details_part[i - 1].endswith('➜') and cost_details_part[i - 1].split('➜')[0].strip() == segment.codeorg.iata_code:     
                        segment_indexes.append(i + 1)
        
        for i in range(len(segment_indexes)):
            temp_content = None
            if i < len(segment_indexes) - 1:
                temp_content = cost_details_part[segment_indexes[i]:segment_indexes[i+1]]
            else:
                temp_content = cost_details_part[segment_indexes[i]:]
            
            air_segments[i].flightclass = temp_content[1]
            
            ticket_segments += self.separate_cost_per_passenger_type(temp_content, passengers, air_segments[i], pnr)
        
        return ticket_segments
    
    # get ancillaries
    def get_ancillaries_zenith(self, ancillaries_part, pnr, passengers, air_segments):
        # get indexes of all "Total" keywords
        total_keyword_indexes = []
        for i in range(len(ancillaries_part)):
            if ancillaries_part[i] == 'Total' or ancillaries_part[i].startswith('Total'):
                total_keyword_indexes.append(i)
        
        if len(total_keyword_indexes) > 1:
            ancillaries_part = ancillaries_part[1:total_keyword_indexes[1]+2]
        
        destination_airports = []
        for segment in air_segments:
            destination_airports.append(segment.codeorg.iata_code)
        
        # get ancillary line by line
        ancillary_lines = []
        segment_binding_index = []
        ancillary_same_type_part = []
        
        temp_ancillary_lines = [] # used to store modified ancillary lines
        interval = 0
        for i in range(len(ancillaries_part)):
            current_value = ancillaries_part[i]
            current_value_split = current_value.split('-')
            skip = False
            if current_value_split[0].strip() in destination_airports:
                if ancillaries_part[i - 1].endswith('EUR'):
                    segment_binding_index.append(i - interval)
                else:
                    if not ancillaries_part[i - 2].endswith('EUR') and 'passager' not in ancillaries_part[i - 2].split(' '):
                        temp_ancillary_name = ancillaries_part[i - 2] + ' ' + ancillaries_part[i - 1]
                        temp_ancillary_lines.pop()
                        temp_ancillary_lines.pop()
                        temp_ancillary_lines.append(temp_ancillary_name)
                        temp_ancillary_lines.append(ancillaries_part[i])
                        segment_binding_index.append(i - 2 - interval)
                        interval += 1
                        skip = True
                    else:
                        segment_binding_index.append(i - 1 - interval)
            
            if not skip:
                temp_ancillary_lines.append(ancillaries_part[i])
            
        ancillaries_part = temp_ancillary_lines
        for len_segment_binding_index in range(len(segment_binding_index)):
            if len_segment_binding_index == len(segment_binding_index) - 1:
                ancillary_same_type_part.append(ancillaries_part[segment_binding_index[len_segment_binding_index]:])
            else:
                ancillary_same_type_part.append(ancillaries_part[segment_binding_index[len_segment_binding_index]:segment_binding_index[len_segment_binding_index + 1]])
        
        previsous_ancillary_name = ''
        for one_type_part in ancillary_same_type_part:
            if one_type_part[0].split('-')[0].strip() not in destination_airports:
                ancillary_name = one_type_part[0]
                previsous_ancillary_name = ancillary_name
                flight_and_date = one_type_part[1]
                index_start = 2
                if len(flight_and_date.split('(')) == 1:
                    flight_and_date = one_type_part[1] + ' ' + one_type_part[2]
                    index_start = 3
            else:
                ancillary_name = previsous_ancillary_name
                flight_and_date = one_type_part[0]
                index_start = 1
                if len(flight_and_date.split('(')) == 1:
                    flight_and_date = one_type_part[0] + ' ' + one_type_part[1]
                    index_start = 2
            
            for one_type_part_element in range(index_start, len(one_type_part)):
                if one_type_part[one_type_part_element].strip() == 'EUR':
                    checker = False
                    if one_type_part_element == len(one_type_part) - 1:
                        checker = True
                    elif one_type_part_element < len(one_type_part) - 1:
                        if one_type_part[one_type_part_element+1].strip() == 'Total':
                            checker = True
                        elif one_type_part[one_type_part_element+1].split(' ')[0] in _passenger_designations_:
                            checker = True
                    
                    if checker:
                        passenger_name = ''
                        quantity = ''
                        total = ''
                        header_element = one_type_part[one_type_part_element-3]
                        
                        if header_element.split(' ')[0] in _passenger_designations_:
                            passenger_name = one_type_part[one_type_part_element-3]
                            quantity = one_type_part[one_type_part_element-2]
                            total = one_type_part[one_type_part_element-1]
                        else:
                            passenger_name = one_type_part[one_type_part_element-4] + ' ' + one_type_part[one_type_part_element-3]
                            quantity = one_type_part[one_type_part_element-2]
                            total = one_type_part[one_type_part_element-1]
                        
                        temp_line = {'ancillary_name': ancillary_name, 'flight_and_date': flight_and_date, 'passenger_name': passenger_name, 'quantity': quantity, 'total': total}
                        ancillary_lines.append(temp_line)
                elif one_type_part[one_type_part_element].endswith('EUR') and one_type_part[one_type_part_element-1].strip() != 'Total':
                    passenger_name = ''
                    quantity = ''
                    total = ''
                    header_element = one_type_part[one_type_part_element-3]
                    if (len(header_element.split('-')) > 1 and header_element.split('-')[0].strip() in destination_airports) or one_type_part[one_type_part_element-3].endswith('EUR'):
                        passenger_name = one_type_part[one_type_part_element-2]
                        quantity = one_type_part[one_type_part_element-1]
                        total = one_type_part[one_type_part_element]
                    else:
                        passenger_name = one_type_part[one_type_part_element-3] + ' ' + one_type_part[one_type_part_element-2]
                        quantity = one_type_part[one_type_part_element-1]
                        total = one_type_part[one_type_part_element]
                
                    temp_line = {'ancillary_name': ancillary_name, 'flight_and_date': flight_and_date, 'passenger_name': passenger_name, 'quantity': quantity, 'total': total}
                    ancillary_lines.append(temp_line)
        
        # assign ancillaries to objects
        ancillaries = []
        ancillary_segments = []
        for line in ancillary_lines:
            temp_ancillary = OthersFee()
            temp_ancillary.pnr = pnr
            temp_ancillary.fee_type = 'EMD'
            temp_ancillary.designation = line['ancillary_name']
            try:
                temp_ancillary.cost = decimal.Decimal(line['total'].split(' ')[0].replace(',', '.'))
                temp_ancillary.total = temp_ancillary.cost
                temp_ancillary.quantity = int(line['quantity'])
            except:
                with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                    error_file.write('{}: \n'.format(datetime.datetime.now()))
                    traceback.print_exc(file=error_file)
                    error_file.write('\n')
            
            temp_ancillary_segment = OtherFeeSegment()
            temp_ancillary_segment.other_fee = temp_ancillary
            # passenger
            for passenger in passengers:
                if (line['passenger_name']).find(passenger.designation + ' ' + passenger.name) > -1:
                    temp_ancillary_segment.passenger = passenger
                    temp_ancillary.passenger = passenger
                    break
            # segment
            for segment in air_segments:
                if segment.codeorg.iata_code == line['flight_and_date'].split('-')[0].strip():
                    temp_ancillary_segment.segment = segment
            # issuing date
            flight_and_date_part = line['flight_and_date']
            flight_and_date_part_split = flight_and_date_part.split('(')
            if len(flight_and_date_part_split) > 0:
                flight_date = flight_and_date_part_split[1][:-1]
                # _months_ = {'janv':'01', 'févr':'02', 'mars':'03', 'avr':'04', 'mai':'05', 'juin':'06', 'juil':'07', 'août':'08', 'sept':'09', 'oct':'10', 'nov':'11', 'déc':'12'}
                if flight_date.find('mars') > -1 or  flight_date.find('mai') > -1 or  flight_date.find('juin') > -1 or  flight_date.find('août') > -1:
                    year = flight_date[-2:]
                    flight_date = flight_date[:-2] + '.' + year
                year_part = flight_date.split('.')[1]
                day_part = ''
                month_part = ''
                day_month_part = flight_date.split('.')[0]
                if day_month_part[2:] in _months_:
                    day_part = day_month_part[0:2]
                    month_part = str(_months_[day_month_part[2:]])
                elif day_month_part[1:] in _months_:
                    day_part = day_month_part[0:1]
                    month_part = str(_months_[day_month_part[1:]])
                try:
                    ancillary_issuing_date = datetime.datetime.strptime(year_part + month_part + day_part + ' ' + '00:00:00', '%y%m%d %H:%M:%S')
                    ancillary_issuing_date = datetime.datetime(ancillary_issuing_date.year, ancillary_issuing_date.month, ancillary_issuing_date.day, ancillary_issuing_date.hour, ancillary_issuing_date.minute, ancillary_issuing_date.second, ancillary_issuing_date.microsecond, pytz.UTC)
                    temp_ancillary.creation_date = ancillary_issuing_date.date()
                    # status
                    if ancillary_issuing_date.date() < pnr.system_creation_date.date():
                        # temp_ancillary.other_fee_status = 3
                        1
                    # fee subjection
                    ancillary_segment = temp_ancillary_segment.segment
                    flight_departure_time = ancillary_segment.departuretime.date()
                    if ancillary_issuing_date.date() == flight_departure_time and flight_departure_time == pnr.system_creation_date.date():
                        self.check_fee_subjection_status(pnr, temp_ancillary)
                        # temp_ancillary.is_subjected_to_fee = False
                except:
                    traceback.print_exc()
                
            ancillaries.append(temp_ancillary)
            ancillary_segments.append(temp_ancillary_segment)
        
        return ancillaries, ancillary_segments
    
    # process taxes
    def process_taxes(self, taxes_part_string):
        # pattern: MG : 637,50; YQ : 1 020,00; YT: 359,21; O4 : 51,00; FR :414,80; F9 : 76,50; IZ : 77,35;A5 : 289,00; G9 : 707,20; O3 :117,30;
        taxes = 0
        # get each tax part
        tax_parts = taxes_part_string.split(";")
        for part in tax_parts:
            # one part pattern: 'MG : 637,50'
            part_split = part.split(":")
            if len(part_split) > 1:
                temp_normalizer = part_split[-1].strip().replace(",", ".").replace(" ", "")
                try:
                    taxes += decimal.Decimal(temp_normalizer)
                except Exception as e:
                    print(e)
        
        return taxes
    
    # get other PNR's details: payment option, emit date, emit office, ...
    def get_other_info(self, other_info_part):
        payment_option = ''
        taxes_part = ''
        issuing_date = None
        issuing_office = ''
        ancillaries = []
        
        for i in range(len(other_info_part)):
            temp_info = other_info_part[i]
            if i < len(other_info_part) - 1:
                temp_info_next = other_info_part[i + 1]
            
            # form of payment
            if temp_info.startswith('Forme de'):
                if temp_info_next.startswith('paiement'):
                    payment_option = other_info_part[i + 2]
                else:
                    payment_option = temp_info_next
            # issuing date
            if temp_info.startswith("Date d'émission"):
                temp_issuing_date = ''
                if temp_info_next != ':':
                    temp_issuing_date = temp_info_next
                else:
                    temp_issuing_date = other_info_part[i + 2]
                try:
                    splitted_issuing_date = temp_issuing_date.split('-')
                    for split_iss_date in splitted_issuing_date:
                        if split_iss_date.removesuffix('.') in _months_:
                            day = splitted_issuing_date[0]
                            month = str(_months_[split_iss_date.removesuffix('.')])
                            year = splitted_issuing_date[2]
                            date_format = datetime.datetime.strptime(year + month + day, '%y%m%d')
                            issuing_date = datetime.datetime(date_format.year, date_format.month, date_format.day)
                except:
                    pass
            # issuing agency
            if temp_info.startswith("Lieu d'émission"):
                j = i + 1
                while True:
                    if other_info_part[j].startswith('Tarif') or j == len(other_info_part):
                        break
                    issuing_office += other_info_part[j] + ' '
                    j += 1
            # modification state
            if temp_info.startswith("Différence tarifaire") or temp_info.startswith("Pénalité d'échange"):
                temp_ancillary = OthersFee()
                temp_ancillary.fee_type = 'TKT'
                temp_ancillary.designation = temp_info
                try:
                    temp_ancillary.cost = decimal.Decimal(other_info_part[i+1].split(' ')[0].replace(',', '.'))
                    temp_ancillary.total = temp_ancillary.cost
                    temp_ancillary.quantity = 1
                    if temp_info.startswith("Différence tarifaire"):
                        ancillaries.append(temp_ancillary)
                    if temp_info.startswith("Pénalité d'échange"):
                        temp_ancillary.cost = ancillaries[0].cost + decimal.Decimal(other_info_part[i+1].split(' ')[0].replace(',', '.'))
                        temp_ancillary.total = temp_ancillary.cost
                        temp_ancillary.designation = "Différence tarifaire + Pénalité d'échange"
                        ancillaries[0] = temp_ancillary
                except:
                    with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                        error_file.write('{}: \n'.format(datetime.datetime.now()))
                        traceback.print_exc(file=error_file)
                        error_file.write('\n')
                j += 1
            # taxes
            if temp_info.startswith("Taxes"):
                try:
                    index_of_taxes = other_info_part.index("Taxes") + 1
                    for a in range(index_of_taxes, len(other_info_part)):
                        if other_info_part[a] == "Total":
                            break
                        taxes_part += other_info_part[a]
                except:
                    with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                        error_file.write('{}: \n'.format(datetime.datetime.now()))
                        traceback.print_exc(file=error_file)
                        error_file.write('\n')
        
        # get taxes
        taxes = self.process_taxes(taxes_part)
        return payment_option, issuing_date, issuing_office, ancillaries, taxes
            
    # save data
    def parse_pnr(self, email_date):
        sid = transaction.savepoint()
        try:
            content_parts = self.read_file()
            for content in content_parts:
                if len(content) == 0:
                    raise Exception('File is empty or not in PDF format.')
                
                if 'Transaction/Synthèse des éléments financiers' in content:
                    from AmadeusDecoder.utilities.ZenithParserReceipt import ZenithParserReceipt
                    ZenithParserReceipt(content).parseReceipt()
                    raise Exception('Receipt received')
                
                if 'Itinéraire' not in content and 'Nom du passager' not in content and 'Nom du client' not in content:
                    raise Exception('File not EWA PNR.')
                    
                pnr, is_saved = self.get_pnr_details(content, 'Emis', email_date)
                pnr.save()
                
                if not is_saved:
                    passengers, pnr_passengers, tickets = self.get_passengers_tickets(content, pnr)
                    for passenger in passengers:
                        passenger.save()
                    for pnr_passenger in pnr_passengers:
                        pnr_passenger.save()
                        
                    other_info_part = self.get_part(content, 'Reçu de paiement')
                    payment_option, issuing_date, issuing_office, other_ancillaries, taxes = self.get_other_info(other_info_part)
                    if issuing_office != '':
                        pnr.agency_name = issuing_office
                        pnr.save()
                    
                    ticket_status = 1
                    # check issuing date and 
                    if issuing_date is not None:
                        try:
                            issuing_date_day = issuing_date.strftime('%A')
                            pnr_creation_date_day = pnr.system_creation_date.strftime('%A')
                            date_difference = pnr.system_creation_date.date() - issuing_date.date()
                            if date_difference.days > 4:
                                ticket_status = 1
                            # if (issuing_date.date() < pnr.system_creation_date.date() and issuing_date_day != 'Saturday' \
                            #     and issuing_date_day != 'Sunday' and pnr_creation_date_day != 'Monday') or date_difference.days > 2 or len(other_ancillaries) > 0:
                            #         ticket_status = 3
                            
                            # accept all from JAN 01
                            first_accepted_date = datetime.datetime(2023, 1, 1).date()
                            if issuing_date.date() < first_accepted_date:
                                ticket_status = 3
                        except:
                            traceback.print_exc()
                    
                    # other ancillaries check
                    modification_fee = 0.0
                    if len(other_ancillaries) > 0:
                        modification_fee = other_ancillaries[0].total / len(passengers);
                    
                    for ticket in tickets:
                        if payment_option != '':
                            ticket.payment_option = payment_option
                        if issuing_date is not None:
                            ticket.issuing_date = issuing_date
                        ticket.ticket_status = ticket_status
                        # set is_subjected_to_fees to False to prevent fee value error
                        ticket.is_subjected_to_fees = False
                        ticket.save()
                        
                    itinerary_part = self.get_part(content, 'Itinéraire')
                    air_segments = self.get_itinerary(itinerary_part, pnr)
                    for segment in air_segments:
                        segment.save()
                        
                    cost_details_part = self.get_part(content, 'Détails du tarif')
                    ticket_segments = self.get_ticket_segment_costs(cost_details_part, passengers, air_segments, pnr)
                    for ticket_segment in ticket_segments:
                        if len(other_ancillaries) > 0:
                            ticket_segment.fare = 0
                            ticket_segment.tax = 0
                            ticket_segment.total = 0
                        ticket_segment.save()
                        
                    # re-adjust is_subjected_to_fees to True to restore true fee
                    for ticket in tickets:
                        pre_saved_ticket = Ticket.objects.filter(number=ticket.number, pnr=pnr).first()
                        if pre_saved_ticket is not None:
                            pre_saved_ticket.is_subjected_to_fees = True
                            pre_saved_ticket.save()
                                            
                    # update ticket fare on PNR update/modification
                    if len(other_ancillaries) > 0:
                        for ticket in tickets:
                            temp_ticket_obj = Ticket.objects.filter(number=ticket.number).first()
                            if pnr.agency_name is not None:
                                for identifier in _CURRENT_TRAVEL_AGENCY_IDENTIFIER_:
                                    if pnr.agency_name.find(identifier) > -1:
                                        temp_ticket_obj.ticket_status = 1
                                        break
                                    else:
                                        temp_ticket_obj.ticket_status = 3
                            temp_ticket_obj.transport_cost = modification_fee
                            temp_ticket_obj.tax = 0.0
                            temp_ticket_obj.total = modification_fee
                            temp_ticket_obj.ticket_description = 'modif'
                            temp_ticket_obj.ticket_status = ticket_status
                            temp_ticket_obj.is_subjected_to_fees = True
                            temp_ticket_obj.save()
                    
                    ancillaries_part = self.get_part(content, 'Ancillaries')
                    ancillaries, ancillaries_segment = self.get_ancillaries_zenith(ancillaries_part, pnr, passengers, air_segments)
                    # if len(other_ancillaries) == 0:
                    for ancillary in ancillaries:
                        # if self.check_fee_subjection_status(date_time, pnr, ticket, other_fee)
                        ancillary.save()
                    for ancillary_segment in ancillaries_segment:
                        ancillary_segment.save()
                        
                    # check if PNR has grouped passenger
                    temp_pnr_invoice_detail = InvoiceDetails.objects.filter(invoice__pnr=pnr).first()
                    if temp_pnr_invoice_detail is not None:
                        if temp_pnr_invoice_detail.total == 0:
                            shared_tax = taxes/(len(tickets))
                            for ticket in tickets:
                                temp_ticket = Ticket.objects.filter(number=ticket.number, pnr=pnr).first()
                                temp_ticket.tax = shared_tax
                                temp_ticket.save()
                        
                    # other ancillaries
                    # for ancillary in other_ancillaries:
                    #     ancillary.pnr = pnr
                    #     ancillary.save()
                # if PNR has already been saved and the previous status was 'Non émis'
                # elif is_saved and pnr.status_value == 1:
                elif is_saved:
                    is_invoiced_status = pnr.is_invoiced
                    psg_invoice_ticket_fee_other = []
                    if is_invoiced_status:
                        passenger_invoices = pnr.passenger_invoice.all()
                        for invoice in passenger_invoices:
                            temp_data = {}
                            if invoice.ticket is not None:
                                temp_data['psg_invoice'] = invoice
                                temp_data['psg_invoice_ticket'] = invoice.ticket
                                temp_data['psg_invoice_fee'] = None
                                temp_data['psg_invoice_other'] = None
                                temp_data['ticket_number'] = invoice.ticket.number
                            if invoice.fee is not None:
                                temp_data['psg_invoice'] = invoice
                                temp_data['psg_invoice_ticket'] = None
                                temp_data['psg_invoice_fee'] = invoice.fee
                                temp_data['psg_invoice_other'] = None
                                try:
                                    temp_data['ticket_number'] = invoice.fee.ticket.number
                                except:
                                    temp_data['ticket_number'] = invoice.fee.other_fee.designation
                            if invoice.other_fee is not None:
                                temp_data['psg_invoice'] = invoice
                                temp_data['psg_invoice_ticket'] = None
                                temp_data['psg_invoice_fee'] = None
                                temp_data['psg_invoice_other'] = invoice.other_fee
                                temp_data['ticket_number'] = None
                            psg_invoice_ticket_fee_other.append(temp_data)
                        is_invoiced_status = True
                    
                    pnr.is_invoiced = is_invoiced_status
                    
                    '''
                    # if not pnr.is_invoiced:
                    # delete old data -- History needed --
                    # passengers
                    current_passengers = Passenger.objects.filter(passenger__pnr=pnr).all()
                    current_passengers.delete()
                    # air segments
                    current_airsegments = PnrAirSegments.objects.filter(pnr=pnr).all()
                    current_airsegments.delete()
                    # ancillaries
                    current_ancillaries = OthersFee.objects.filter(pnr=pnr).all()
                    current_ancillaries.delete()'''
                    
                    # add new data
                    passengers, pnr_passengers, tickets = self.get_passengers_tickets(content, pnr)
                    # passengers
                    # compare and delete
                    try:
                        Passenger().compare_and_delete(pnr, passengers)
                    except:
                        traceback.print_exc()
                        # error_file.write('{}: \n'.format(datetime.now()))
                        # error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                        # traceback.print_exc(file=error_file)
                        # error_file.write('\n')
                    for passenger in passengers:
                        temp_passenger = passenger.get_passenger_by_pnr_passenger(pnr)
                        if temp_passenger is None:
                            passenger.save()
                            try:
                                passenger.update_ticket_passenger(pnr)
                            except:
                                traceback.print_exc()
                                # error_file.write('{}: \n'.format(datetime.now()))
                                # error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                                # traceback.print_exc(file=error_file)
                                # error_file.write('\n')
                            pnr_passenger = PnrPassenger(pnr=pnr, passenger=passenger)
                            pnr_passenger.save()
                        else:
                            passenger = temp_passenger
                    
                    # for passenger in passengers:
                    #     passenger.save()
                    # for pnr_passenger in pnr_passengers:
                    #     pnr_passenger.save()
                        
                    other_info_part = self.get_part(content, 'Reçu de paiement')
                    payment_option, issuing_date, issuing_office, other_ancillaries, taxes= self.get_other_info(other_info_part)
                    if issuing_office != '':
                        pnr.agency_name = issuing_office
                        pnr.save()
                    
                    ticket_status = 1
                    # check issuing date and 
                    if issuing_date is not None:
                        try:
                            issuing_date_day = issuing_date.strftime('%A')
                            pnr_creation_date_day = pnr.system_creation_date.strftime('%A')
                            date_difference = pnr.system_creation_date.date() - issuing_date.date()
                            if date_difference.days > 4:
                                ticket_status = 1
                                
                            # if (issuing_date.date() < pnr.system_creation_date.date() and issuing_date_day != 'Saturday' \
                            #     and issuing_date_day != 'Sunday' and pnr_creation_date_day != 'Monday') or date_difference.days > 2 or len(other_ancillaries) > 0:
                            #         ticket_status = 3
                            
                            # accept all from JAN 01
                            first_accepted_date = datetime.datetime(2023, 1, 1).date()
                            if issuing_date.date() < first_accepted_date:
                                ticket_status = 3
                        except:
                            traceback.print_exc()
                    
                    # other ancillaries check
                    modification_fee = 0
                    if len(other_ancillaries) > 0:
                        modification_fee = other_ancillaries[0].total / len(passengers);
                    
                    # update ticket status if the PNR has been reissued with different ticket(s)
                    try:
                        is_multiple_file = False
                        if len(content_parts) > 1:
                            is_multiple_file = True
                        Ticket().update_ticket_status_PNR_reissued_EWA(pnr, tickets, is_multiple_file)
                    except Exception:
                        # error_file.write('{}: \n'.format(datetime.now()))
                        # error_file.write('File (PNR Altea) with error: {} \n'.format(str(self.get_path())))
                        # traceback.print_exc(file=error_file)
                        # error_file.write('\n')
                        traceback.print_exc()
                    
                    for ticket in tickets:
                        temp_ticket = Ticket.objects.filter(number=ticket.number).first()
                        temp_passenger = Passenger.objects.filter(name=ticket.passenger.name, designation=ticket.passenger.designation, passenger__pnr=pnr).first()
                    
                        if temp_ticket is not None:
                            ticket = temp_ticket
                            
                        if temp_passenger is not None:
                            ticket.passenger = temp_passenger
                        
                        if payment_option != '':
                            ticket.payment_option = payment_option
                        if issuing_date is not None:
                            ticket.issuing_date = issuing_date
                        ticket.ticket_status = ticket_status
                        ticket.save()
                    
                    itinerary_part = self.get_part(content, 'Itinéraire')
                    air_segments = self.get_itinerary(itinerary_part, pnr)
                    for segment in air_segments:
                        try:
                            temp_segment = segment.get_air_segment_by_air_segment(pnr)
                            if temp_segment is None:
                                segment.save()
                            else:
                                try:
                                    temp_segment.departuretime = segment.departuretime if segment.departuretime is not None else None
                                    temp_segment.arrivaltime = segment.arrivaltime if segment.arrivaltime is not None else None
                                    temp_segment.air_segment_status = 1
                                    temp_segment.segment_state = segment.segment_state
                                    temp_segment.save()
                                except:
                                    traceback.print_exc()
                                
                        except Exception:
                            traceback.print_exc()
                        # segment.save()
                        
                    cost_details_part = self.get_part(content, 'Détails du tarif')
                    ticket_segments = self.get_ticket_segment_costs(cost_details_part, passengers, air_segments, pnr)
                    for ticket_segment in ticket_segments:
                        temp_segment = PnrAirSegments.objects.filter(segmentorder=ticket_segment.segment.segmentorder, pnr=pnr, air_segment_status=1).first()
                        temp_ticket = Ticket.objects.filter(number=ticket_segment.ticket.number).first()
                        if temp_segment is not None:
                            temp_ticket_passenger_segment = TicketPassengerSegment.objects.filter(segment=temp_segment, ticket=temp_ticket).first()
                            if temp_ticket_passenger_segment is None:
                                ticket_segment.segment = temp_segment
                                ticket_segment.ticket = temp_ticket
                                try:
                                    if len(other_ancillaries) > 0:
                                        ticket_segment.fare = 0
                                        ticket_segment.tax = 0
                                        ticket_segment.total = 0
                                    ticket_segment.save()
                                except Exception as e:
                                    print(e)
                                    traceback.print_exc()
                        
                    # update ticket fare on PNR update/modification
                    if len(other_ancillaries) > 0:
                        for ticket in tickets:
                            temp_ticket_obj = Ticket.objects.filter(number=ticket.number).first()
                            if pnr.agency_name is not None:
                                for identifier in _CURRENT_TRAVEL_AGENCY_IDENTIFIER_:
                                    if pnr.agency_name.find(identifier) > -1:
                                        temp_ticket_obj.ticket_status = 1
                                        break
                                    else:
                                        temp_ticket_obj.ticket_status = 3
                            temp_ticket_obj.transport_cost = modification_fee;
                            temp_ticket_obj.tax = 0.0;
                            temp_ticket_obj.total = modification_fee;
                            temp_ticket_obj.ticket_description = 'modif'
                            temp_ticket_obj.ticket_status = ticket_status
                            temp_ticket_obj.save()
                    
                    ancillaries_part = self.get_part(content, 'Ancillaries')
                    ancillaries, ancillaries_segment = self.get_ancillaries_zenith(ancillaries_part, pnr, passengers, air_segments)
                    # if len(other_ancillaries) == 0:
                    for ancillary in ancillaries:
                        temp_ancillary = None
                        is_ancillary_saved = False
                        for passenger in passengers:
                            temp_passenger = passenger.get_passenger_by_pnr_passenger(pnr)
                            temp_ancillary = OthersFee.objects.filter(designation=ancillary.designation, pnr=pnr, related_segments__passenger=temp_passenger).first()
                            if temp_ancillary is not None:
                                ancillary = temp_ancillary
                                is_ancillary_saved = True
                                break
                        if not is_ancillary_saved:
                            ancillary.passenger = ancillary.passenger.get_passenger_by_pnr_passenger(pnr)
                        ancillary.save()
                    for ancillary_segment in ancillaries_segment:
                        temp_segment = PnrAirSegments.objects.filter(segmentorder=ancillary_segment.segment.segmentorder, pnr=pnr, air_segment_status=1).last()
                        temp_passenger = ancillary_segment.passenger.get_passenger_by_pnr_passenger(pnr)
                        temp_ancillary = OthersFee.objects.filter(designation=ancillary_segment.other_fee.designation, pnr=pnr, passenger=temp_passenger).first()
                        temp_ancillary_seg = OtherFeeSegment.objects.filter(other_fee=temp_ancillary, segment=temp_segment, passenger=temp_passenger).first()
                        if temp_ancillary_seg is None and temp_passenger is not None and temp_segment is not None and temp_ancillary is not None:
                            ancillary_segment.other_fee = temp_ancillary
                            ancillary_segment.passenger = temp_passenger
                            ancillary_segment.segment = temp_segment
                            ancillary_segment.save()
                    
                    # check if PNR has grouped passenger
                    temp_pnr_invoice_detail = InvoiceDetails.objects.filter(invoice__pnr=pnr).first()
                    if temp_pnr_invoice_detail is not None:
                        if temp_pnr_invoice_detail.total == 0:
                            shared_tax = taxes/(len(tickets))
                            for ticket in tickets:
                                temp_ticket = Ticket.objects.filter(number=ticket.number, pnr=pnr).first()
                                temp_ticket.tax = shared_tax
                                temp_ticket.save()
                        
                    
                    # other ancillaries
                    # for ancillary in other_ancillaries:
                    #     ancillary.pnr = pnr
                    #     ancillary.save()
                    
                    '''
                    # re-save passenger invoice
                    if initial_is_invoiced_status:
                        for temp_data in psg_invoice_ticket_fee_other:
                            passenger_invoice = temp_data['psg_invoice']
                            ticket = temp_data['psg_invoice_ticket']
                            fee = temp_data['psg_invoice_fee']
                            other_fee = temp_data['psg_invoice_other']
                            ticket_number = temp_data['ticket_number']
                            
                            if ticket is not None:
                                temp_ticket_obj = Ticket.objects.filter(number=ticket_number).first()
                                if temp_ticket_obj is None:
                                    ticket_to_be_created = Ticket()
                                    ticket_to_be_created.number = ticket.number
                                    ticket_to_be_created.pnr = pnr
                                    ticket_to_be_created.state = 0
                                    ticket_to_be_created.ticket_status = 0
                                    ticket_to_be_created.transport_cost = ticket.transport_cost
                                    ticket_to_be_created.tax = ticket.tax
                                    ticket_to_be_created.total = ticket.total
                                    ticket_to_be_created.emitter = ticket.emitter
                                    ticket_to_be_created.passenger = ticket.passenger
                                    ticket_to_be_created.ticket_type = ticket.ticket_type
                                    # ticket_to_be_created.save()
                                    temp_ticket_obj = ticket_to_be_created
                                ticket = temp_ticket_obj
                            elif fee is not None:
                                temp_fee_obj = None
                                if Fee.objects.filter(ticket__number=ticket_number, pnr=pnr).first() is not None:
                                    temp_fee_obj = Fee.objects.filter(ticket__number=ticket_number, pnr=pnr).first()
                                elif Fee.objects.filter(other_fee__designation=ticket_number, pnr=pnr).first() is not None:
                                    temp_fee_obj = Fee.objects.filter(other_fee__designation=ticket_number, pnr=pnr).first()
                                    
                                if temp_fee_obj is not None:
                                    temp_fee_obj.cost = fee.cost
                                    temp_fee_obj.total = fee.total
                                    # temp_fee_obj.save()
                                fee = temp_fee_obj
                            elif other_fee is not None:
                                temp_other_fee = OthersFee.objects.filter(designation=other_fee.designation, pnr=pnr).first()
                                if temp_other_fee is None:
                                    other_fee_to_be_created = OthersFee()
                                    other_fee_to_be_created.designation = other_fee.designation
                                    other_fee_to_be_created.cost = other_fee.cost
                                    other_fee_to_be_created.tax = other_fee.tax
                                    other_fee_to_be_created.total = other_fee.total
                                    other_fee_to_be_created.pnr = pnr
                                    other_fee_to_be_created.creation_date = other_fee.creation_date
                                    other_fee_to_be_created.is_subjected_too_fee = other_fee.is_subjected_too_fee
                                    # other_fee_to_be_created.save()
                                    temp_other_fee = other_fee_to_be_created
                                other_fee = temp_other_fee
                                
                            temp_passenger_invoice_obj = PassengerInvoice()
                            temp_passenger_invoice_obj.reference = passenger_invoice.reference
                            temp_passenger_invoice_obj.is_invoiced = passenger_invoice.is_invoiced
                            temp_passenger_invoice_obj.is_checked = passenger_invoice.is_checked
                            temp_passenger_invoice_obj.type = passenger_invoice.type
                            temp_passenger_invoice_obj.client_id = passenger_invoice.client_id
                            temp_passenger_invoice_obj.fee = fee
                            temp_passenger_invoice_obj.pnr = pnr
                            temp_passenger_invoice_obj.ticket = ticket
                            temp_passenger_invoice_obj.user_follower = passenger_invoice.user_follower
                            temp_passenger_invoice_obj.is_quotation = passenger_invoice.is_quotation
                            temp_passenger_invoice_obj.invoice_id = passenger_invoice.invoice_id
                            temp_passenger_invoice_obj.status = passenger_invoice.status
                            temp_passenger_invoice_obj.other_fee = other_fee
                            temp_passenger_invoice_obj.date_creation = passenger_invoice.date_creation
                            temp_passenger_invoice_obj.control = passenger_invoice.control
                            # temp_passenger_invoice_obj.save()
                    '''
            transaction.savepoint_commit(sid)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            raise e
    
    # file_list 
    # [{'email_date': 'Tue, 25 Oct 2022 13:15:16 +0000', 'attachment': ['h:/Famenontsoa/Light/S5-S6/Stage/Project/TravelAgency/DjangoTravelAgency/EmailFetcher/utilities/attachments_dir/2046_issoufali.pnr@outlook.com/E-ticket 00CDLF-ASSANE DZA  .pdf']}]
    
    # save multiple file
    def save_data(self, file_list):
        for file in file_list:
            for temp_file in file['attachment']:
                temp = ZenithParser()
                temp.set_path(temp_file)
                temp.set_email_date(file['email_date'])
                try:
                    try:
                        if self.parse_emd(temp.read_file(), temp.get_email_date()):
                            return
                    except:
                        traceback.print_exc()
                    temp.parse_pnr(temp.get_email_date())
                    temp.set_main_txt_path(self.get_txt_path_from_pdf(temp_file))
                    temp.get_creator_emitter()
                except Exception as e:
                    if str(e) == 'File is empty or not in PDF format.':
                        print('File (PNR EWA) not PDF or empty: ' + str(file))
                    elif str(e) == 'Receipt received':
                        print(str(e))
                    else:
                        print('File (PNR EWA) with error: ' + str(file))
                    with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                        error_file.write('{}: \n'.format(datetime.datetime.now()))
                        error_file.write('File (PNR EWA) with error: {} \n'.format(str(file)))
                        traceback.print_exc(file=error_file)
                        error_file.write('\n')
                    if (str(e) == "connection already closed"):
                        from AmadeusDecoder.utilities.SendMail import Sending
                        Sending.send_email_pnr_parsing(str(file))
                    continue
                
                