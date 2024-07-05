'''
Created on 8 Sep 2022

'''
import json
import os
import shlex
import subprocess
import time
import traceback

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests

from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
from AmadeusDecoder.models.pnr.Pnr import Pnr

from AmadeusDecoder.utilities.AmadeusParser import AmadeusParser
from AmadeusDecoder.utilities.ProductImportParser import ProductParser, CustomerParser
from AmadeusDecoder.models.configuration.Configuration import Configuration
from django.db.models import Q

from AmadeusDecoder.utilities.ZenithParser import ZenithParser, ReceiptException


@login_required(login_url='index')
def tools(request):  
    return render(request,'tools/tools.html')


def call_product_import(request):
    
    status = ''
    try:
        directory = '/opt/odoo/issoufali-addons/sync_products/data/exported/'
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                ProductParser.import_product(os.path.join(directory, file), directory)
        status = 'Product successfuly imported'
    except Exception as e:
        print(e)
        status = str(e)

    return JsonResponse({'return':status})


def call_customer_import(request):
    
    status = ''
    try:
        directory = '/opt/odoo/issoufali-addons/export_contacts/data/exported/'
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                CustomerParser.import_customer(os.path.join(directory, file), directory)
        status = 'Customer successfuly imported'
    except Exception as e:
        print(e)
        status = str(e)


    return JsonResponse({'return':status})

    #get the invoice number for unordering a pnr
def get_invoice_number(request,numeroPnr):
    
    pnr = Pnr.objects.get(number=numeroPnr)
    invoices = PassengerInvoice.objects.filter(pnr_id=pnr.id, is_invoiced=True).distinct()

    invoices_data = [{'invoice_number': invoice.invoice_number} for invoice in invoices]
    
    unique_invoice_numbers_set = {entry['invoice_number'] for entry in invoices_data}

    unique_invoice_numbers_list = list(unique_invoice_numbers_set)

    print(unique_invoice_numbers_list)
    return JsonResponse({'invoices': unique_invoice_numbers_list})

# def server(request):
#     chemin_api_js = r"..\travelagency\AmadeusDecoder\static\js\pnr_unordering\pnr_unordering.js"
#     commande = ["node", chemin_api_js]
#     processus_api = subprocess.Popen(commande, shell=True)
#     print(processus_api.returncode)
#     return JsonResponse({'message': 'Le serveur NodeJS a été démarré'}, safe=False)


# ------------------------ TEST PARSING ---------------------------
def test_parsing(request):
    return render(request,'tools/test_parsing.html')  

def test_parsing_txt(request):
    if request.method == 'POST':
        context={}

    return JsonResponse(context, safe=False)

def test_parsing_upload_file(request):
    import fitz
    import base64
    if 'file' in request.FILES:
        try:
            context={'status':200}
            uploaded_file = request.FILES['file']
            uploaded_file_name = (uploaded_file.name).replace(' ','')
            with open('EmailFetcher/utilities/attachments_dir/test@test.com/' + uploaded_file_name, 'wb') as destination_file:
                for chunk in uploaded_file.chunks():
                    destination_file.write(chunk)

            pdf_image = fitz.open('EmailFetcher/utilities/attachments_dir/test@test.com/' + uploaded_file_name)
            # Récupérer le nombre de pages du PDF
            num_pages = pdf_image.page_count
            # Créer une liste pour stocker les images
            images = []
            for page_number in range(num_pages):
                # Charger la page
                page = pdf_image.load_page(page_number)
                # Obtenir une représentation en bytes de l'image (vous pouvez choisir un format d'image approprié)
                image_bytes = page.get_pixmap().tobytes()
                
                # Convertir les bytes en base64
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')

                images.append(image_base64)
            pdf_image.close()
            context['pdf_image'] = json.dumps(images)
            
        except:
            context['status':1]
            trace_str = traceback.format_exc()
            print(trace_str)

    return JsonResponse(context, safe=False)


def test_parsing_zenith(request):
    import fitz
    import base64
    if request.method == 'POST':
        context = {'status':200,'error':''}
        uploaded_file_name = request.POST.get('uploaded_file_name')
        uploaded_file_name = uploaded_file_name.replace(' ','')
        try:
            
            temp = ZenithParser()
            attachement_folder = 'test@test.com'
            temp.set_path('EmailFetcher//utilities//attachments_dir//' + attachement_folder + '//' + uploaded_file_name)
            temp.set_email_date(None)
            temp.set_main_txt_path('EmailFetcher//utilities//attachments_dir//' + attachement_folder + '//' + attachement_folder + '.txt')
            
            content = temp.read_file()
            for line in content:
                print(line)

            data = temp.test_parse_pnr(temp.get_email_date())
            pnr_data = data['pnr']

            # get details pnr
            pnr = {'id': pnr_data.id, 'number':pnr_data.number,'status':pnr_data.status}
            context['pnr'] = pnr

            # get data segments
            air_segments = pnr_data.segments.filter(segment_type='Flight', air_segment_status=1).all().order_by('segmentorder')
            segments_data = []
            for segment in air_segments:
                values = {}
                values['segmentorder'] = segment.segmentorder
                values['segment'] = segment.__str__()
                values['flightclass'] = segment.flightclass
                values['codeorg'] = segment.codeorg.iata_code
                values['codedest'] = segment.codedest.iata_code
                values['departuretime'] = segment.departuretime.strftime("%d/%m/%Y, %H:%M:%S") if segment.departuretime is not None else ''
                values['arrivaltime'] = segment.arrivaltime.strftime("%d/%m/%Y, %H:%M:%S") if segment.arrivaltime is not None else ''
                values['segment_state'] = segment.segment_state
                segments_data.append(values)

            context['segments'] = segments_data
            print('££££££££££££££££££££££££££££££££££')
            print(context['segments'])

            # get data ticket
            tickets = pnr_data.tickets.filter(Q(ticket_status=1) | Q(is_invoiced=True)).filter(Q(total__gt=0) | Q(is_no_adc=True) | (Q(is_refund=True) & Q(total__lt=0))).all().order_by('number')
            tickets_data = []
            for ticket in tickets:
                values = {}
                if ticket.ticket_type == 'EMD' or ticket.ticket_type == 'TKT':
                    values['type'] = ticket.ticket_type
                if ticket.ticket_type == 'CREDIT_NOTE':
                    values['type'] = 'Avoir'
            
                values['billet'] = ticket.__str__()
                if ticket.ticket_type == 'EMD' and pnr_data.type == 'EWA':
                    if ticket.ticket_description is not None:
                        values['passager'] = ticket.ticket_description

                values['passager'] = ticket.passenger.__str__() if ticket.passenger is not None else ''
                values['montant'] = round(ticket.transport_cost,2)
                values['taxe'] = round(ticket.tax,2)
                values['total'] = round(ticket.total,2)

                values['passenger_order'] = ticket.passenger.order if ticket.passenger is not None else ''
                values['issuing_date'] = (ticket.issuing_date).strftime("%d/%m/%Y") if ticket.issuing_date is not None else ''
                
                fee = ticket.fees.all()[0]
                values['fee_type'] = fee.type
                values['fee_cost'] = round(fee.cost,2)
                values['fee_taxe'] = round(fee.tax,2)
                values['fee_total'] = round(fee.total,2)
                values['fee_issuing_date'] = (fee.ticket.issuing_date).strftime("%d/%m/%Y") if fee.ticket.issuing_date is not None else ''

                tickets_data.append(values)

            context['tickets'] = tickets_data

            # get data other fee
            other_fees = pnr_data.others_fees.filter((Q(other_fee_status=1) & Q(ticket=None)) | Q(is_invoiced=True)).all()
            other_fee_data =[]

            if other_fees is not None:

                for other_fee in other_fees:
                    values = {}
                    values['type'] = other_fee.fee_type
                    values['billet'] = other_fee.designation
                    values['passager'] = other_fee.passenger.__str__()
                    values['montant'] = round(other_fee.cost,2)
                    values['taxe'] = round(other_fee.tax,2)
                    values['total'] = round(other_fee.total,2)
                    values['passenger_segment'] = other_fee.passenger_segment if other_fee.passenger_segment is not None else ''
                    values['issuing_date'] = (other_fee.creation_date).strftime("%d/%m/%Y") if other_fee.creation_date is not None else ''

                    fee = ticket.fees.all()[0]
                    values['fee_type'] = fee.type
                    values['fee_cost'] = round(fee.cost,2)
                    values['fee_taxe'] = round(fee.tax,2)
                    values['fee_total'] = round(fee.total,2)
                    values['fee_issuing_date'] = (fee.ticket.issuing_date).strftime("%d/%m/%Y") if fee.ticket.issuing_date is not None else ''
                    
                    other_fee_data.append(values)

                context['other_fee'] = other_fee_data
            
            temp.get_creator_emitter()
            
        except ReceiptException as e:
            context['status'] = 122
            pnr_number = e.identifier
            pnr_data = Pnr.objects.get(number=pnr_number)

            # get details pnr
            pnr = {'id': pnr_data.id, 'number':pnr_data.number,'status':pnr_data.status}
            context['pnr'] = pnr

            # get data segments
            air_segments = pnr_data.segments.filter(segment_type='Flight', air_segment_status=1).all().order_by('segmentorder')
            segments_data = []
            for segment in air_segments:
                values = {}
                values['segmentorder'] = segment.segmentorder
                values['segment'] = segment.__str__()
                values['flightclass'] = segment.flightclass
                values['codeorg'] = segment.codeorg.iata_code
                values['codedest'] = segment.codedest.iata_code
                values['departuretime'] = segment.departuretime.strftime("%d/%m/%Y, %H:%M:%S") if segment.departuretime is not None else ''
                values['arrivaltime'] = segment.arrivaltime.strftime("%d/%m/%Y, %H:%M:%S") if segment.arrivaltime is not None else ''
                values['segment_state'] = segment.segment_state
                segments_data.append(values)

            context['segments'] = segments_data

            # get data ticket
            tickets = pnr_data.tickets.filter(Q(ticket_status=1) | Q(is_invoiced=True)).filter(Q(total__gt=0) | Q(is_no_adc=True) | (Q(is_refund=True) & Q(total__lt=0))).all().order_by('number')
            tickets_data = []
            for ticket in tickets:
                values = {}
                if ticket.ticket_type == 'EMD' or ticket.ticket_type == 'TKT':
                    values['type'] = ticket.ticket_type
                if ticket.ticket_type == 'CREDIT_NOTE':
                    values['type'] = 'Avoir'
            
                values['billet'] = ticket.__str__()
                if ticket.ticket_type == 'EMD' and pnr_data.type == 'EWA':
                    if ticket.ticket_description is not None:
                        values['passager'] = ticket.ticket_description

                values['passager'] = ticket.passenger.__str__() if ticket.passenger is not None else ''
                values['montant'] = round(ticket.transport_cost,2)
                values['taxe'] = round(ticket.tax,2)
                values['total'] = round(ticket.total,2)

                values['passenger_order'] = ticket.passenger.order if ticket.passenger is not None else ''
                values['issuing_date'] = (ticket.issuing_date).strftime("%d/%m/%Y") if ticket.issuing_date is not None else ''
                
                fee = ticket.fees.all()[0]
                values['fee_type'] = fee.type
                values['fee_cost'] = round(fee.cost,2)
                values['fee_taxe'] = round(fee.tax,2)
                values['fee_total'] = round(fee.total,2)
                values['fee_issuing_date'] = (fee.ticket.issuing_date).strftime("%d/%m/%Y") if fee.ticket.issuing_date is not None else ''

                tickets_data.append(values)

            context['tickets'] = tickets_data

            # get data other fee
            other_fees = pnr_data.others_fees.filter((Q(other_fee_status=1) & Q(ticket=None)) | Q(is_invoiced=True)).all()
            other_fee_data =[]

            if other_fees is not None:

                for other_fee in other_fees:
                    values = {}
                    values['type'] = other_fee.fee_type
                    values['billet'] = other_fee.designation
                    values['passager'] = other_fee.passenger.__str__()
                    values['montant'] = round(other_fee.cost,2)
                    values['taxe'] = round(other_fee.tax,2)
                    values['total'] = round(other_fee.total,2)
                    values['passenger_segment'] = other_fee.passenger_segment if other_fee.passenger_segment is not None else ''
                    values['issuing_date'] = (other_fee.creation_date).strftime("%d/%m/%Y") if other_fee.creation_date is not None else ''

                    fee = other_fee.fees.all()[0]
                    values['fee_type'] = fee.type
                    values['fee_cost'] = round(fee.cost,2)
                    values['fee_taxe'] = round(fee.tax,2)
                    values['fee_total'] = round(fee.total,2)
                    values['fee_issuing_date'] = (other_fee.creation_date).strftime("%d/%m/%Y") if other_fee.creation_date is not None else ''
                    
                    other_fee_data.append(values)

                context['other_fee'] = other_fee_data

        except Exception as e:
            trace_str = traceback.format_exc()
            context['status'] = 10
            context['error'] = trace_str
        
        return JsonResponse(context, safe=False)

def test_parsing_text(request):
    import os
    data = request.POST.get('data')
    context={'status':200, 'message':"Pas d'Erreur",'error':''}

    try: 

        temp = AmadeusParser() 
        file = '0_fnd@amadeus.com'
        chemin = os.getcwd() + '/EmailFetcher/utilities/attachments_dir/' + file 
        text_to_write = "Subject\nYour travel information\n\nPlain_Text\n"

        # Vérifiez si le fichier existe, sinon créer le fichier
        if not os.path.exists(chemin):
            open(chemin, 'a').close()
            with open(chemin,'w') as fichier:
                fichier.write(text_to_write)
 
        # Lecture du contenu existant du fichier
        with open(chemin,'r') as fichier:
            lines = fichier.readlines()
        
        # Écriture des premières lignes et ajout des nouvelles données
        with open(chemin,'w') as fichier:
            fichier.writelines(lines[:8 -1])
            fichier.writelines(data)

        temp.set_path(os.getcwd() + '/EmailFetcher/utilities/attachments_dir/' + file )

        contents = temp.read_file()
        needed_content = temp.needed_content(contents)
        normalize_file = temp.normalize_file(needed_content)

        temp.set_email_date(None)
        if len(contents) > 0:
        
            
            if contents[0].startswith('AGY'): # TJQ
                try:
                    temp.parse_tjq(needed_content)
                except:
                    print('File (TJQ) with error: ' + str(file))
                    traceback.print_exc()
                    context['error'] = traceback.format_exc()
                    context['status'] = 1
                    context['message'] = 'File (TJQ) with error: ' + str(file)
            else:
                for j in range(len(contents)):
                    if contents[j].startswith('RPP'):
                        temp.set_is_archived(True)
                        continue
                    if contents[j].startswith('RP') and not contents[j].startswith('RPP'):
                        try:
                            # temp.parse_pnr(contents[j:], needed_content, temp.get_email_date())
                            data = temp.test_parse_pnr(contents[j:], needed_content, temp.get_email_date())
                            pnr_data = data['pnr']
                            pnr = {'id': pnr_data.id, 'number':pnr_data.number,'status':pnr_data.status}
                            context['pnr'] = pnr

                            # get data segments
                            air_segments = pnr_data.segments.filter(segment_type='Flight', air_segment_status=1).all().order_by('segmentorder')
                            segments_data = []
                            for segment in air_segments:
                                values = {}
                                values['segmentorder'] = segment.segmentorder
                                values['segment'] = segment.__str__()
                                values['flightclass'] = segment.flightclass
                                values['codeorg'] = segment.codeorg.iata_code
                                values['codedest'] = segment.codedest.iata_code
                                values['departuretime'] = segment.departuretime.strftime("%d/%m/%Y, %H:%M:%S") if segment.departuretime is not None else ''
                                values['arrivaltime'] = segment.arrivaltime.strftime("%d/%m/%Y, %H:%M:%S") if segment.arrivaltime is not None else ''
                                values['segment_state'] = segment.segment_state
                                segments_data.append(values)

                            context['segments'] = segments_data
                            print('£££££££££££££££££££££££££££££££££')
                            print(context['segments'])

                            # get data ticket
                            tickets = pnr_data.tickets.filter(Q(ticket_status=1) | Q(is_invoiced=True)).filter(Q(total__gt=0) | Q(is_no_adc=True) | (Q(is_refund=True) & Q(total__lt=0))).all().order_by('number')
                            tickets_data = []
                            for ticket in tickets:
                                values = {}
                                if ticket.ticket_type == 'EMD' or ticket.ticket_type == 'TKT':
                                    values['type'] = ticket.ticket_type
                                if ticket.ticket_type == 'CREDIT_NOTE':
                                    values['type'] = 'Avoir'
                            
                                values['billet'] = ticket.__str__()
                                if ticket.ticket_type == 'EMD' and pnr_data.type == 'EWA':
                                    if ticket.ticket_description is not None:
                                        values['passager'] = ticket.ticket_description

                                values['passager'] = ticket.passenger.__str__() if ticket.passenger is not None else ''
                                values['montant'] = round(ticket.transport_cost,2)
                                values['taxe'] = round(ticket.tax,2)
                                values['total'] = round(ticket.total,2)

                                values['passenger_order'] = ticket.passenger.order if ticket.passenger is not None else ''
                                values['issuing_date'] = (ticket.issuing_date).strftime("%d/%m/%Y") if ticket.issuing_date is not None else ''
                                
                                fee = ticket.fees.all()[0]
                                values['fee_type'] = fee.type
                                values['fee_cost'] = round(fee.cost,2)
                                values['fee_taxe'] = round(fee.tax,2)
                                values['fee_total'] = round(fee.total,2)
                                values['fee_issuing_date'] = (fee.ticket.issuing_date).strftime("%d/%m/%Y") if fee.ticket.issuing_date is not None else ''

                                tickets_data.append(values)

                            context['tickets'] = tickets_data

                            # get data other fee
                            other_fees = pnr_data.others_fees.filter((Q(other_fee_status=1) & Q(ticket=None)) | Q(is_invoiced=True)).all()
                            other_fee_data =[]

                            if other_fees is not None:

                                for other_fee in other_fees:
                                    values = {}
                                    values['type'] = other_fee.fee_type
                                    values['billet'] = other_fee.designation
                                    values['passager'] = other_fee.passenger.__str__()
                                    values['montant'] = round(other_fee.cost,2)
                                    values['taxe'] = round(other_fee.tax,2)
                                    values['total'] = round(other_fee.total,2)
                                    values['passenger_segment'] = other_fee.passenger_segment if other_fee.passenger_segment is not None else ''
                                    values['issuing_date'] = (other_fee.creation_date).strftime("%d/%m/%Y") if other_fee.creation_date is not None else ''

                                    fee = ticket.fees.all()[0]
                                    values['fee_type'] = fee.type
                                    values['fee_cost'] = round(fee.cost,2)
                                    values['fee_taxe'] = round(fee.tax,2)
                                    values['fee_total'] = round(fee.total,2)
                                    values['fee_issuing_date'] = (fee.ticket.issuing_date).strftime("%d/%m/%Y") if fee.ticket.issuing_date is not None else ''
                                    
                                    other_fee_data.append(values)

                                context['other_fee'] = other_fee_data
          
                            break
                        except:
                            print('File (PNR) with error: ' + file)
                            traceback.print_exc()
                            context['error'] = traceback.format_exc()
                            context['status'] = 1
                            context['message'] = 'File (PNR) with error: ' + file
                    if contents[j].startswith('EMD'):
                        try:
                            print('Needed content ', needed_content)
                            print('Needed content 2 ', temp.needed_content(contents[j:]))
                            # temp.parse_emd(temp.needed_content(contents[j:]), temp.get_email_date())
                            ticket_data = temp.test_parse_emd(temp.needed_content(contents[j:]), temp.get_email_date())

                            pnr_data = ticket_data['pnr']
                            pnr = {'id': pnr_data.id, 'number':pnr_data.number,'status':pnr_data.status}
                            context['pnr'] = pnr

                            # get data segments
                            air_segments = pnr_data.segments.filter(segment_type='Flight', air_segment_status=1).all().order_by('segmentorder')
                            segments_data = []
                            for segment in air_segments:
                                values = {}
                                values['segmentorder'] = segment.segmentorder
                                values['segment'] = segment.__str__()
                                values['flightclass'] = segment.flightclass
                                values['codeorg'] = segment.codeorg.iata_code
                                values['codedest'] = segment.codedest.iata_code
                                values['departuretime'] = segment.departuretime.strftime("%d/%m/%Y, %H:%M:%S") if segment.departuretime is not None else ''
                                values['arrivaltime'] = segment.arrivaltime.strftime("%d/%m/%Y, %H:%M:%S") if segment.arrivaltime is not None else ''
                                values['segment_state'] = segment.segment_state
                                segments_data.append(values)

                            context['segments'] = segments_data

                            # get data ticket
                            tickets = pnr_data.tickets.filter(Q(ticket_status=1) | Q(is_invoiced=True)).filter(Q(total__gt=0) | Q(is_no_adc=True) | (Q(is_refund=True) & Q(total__lt=0))).all().order_by('number')
                            tickets_data = []
                            for ticket in tickets:
                                values = {}
                                if ticket.ticket_type == 'EMD' or ticket.ticket_type == 'TKT':
                                    values['type'] = ticket.ticket_type
                                if ticket.ticket_type == 'CREDIT_NOTE':
                                    values['type'] = 'Avoir'
                            
                                values['billet'] = ticket.__str__()
                                if ticket.ticket_type == 'EMD' and pnr_data.type == 'EWA':
                                    if ticket.ticket_description is not None:
                                        values['passager'] = ticket.ticket_description

                                values['passager'] = ticket.passenger.__str__() if ticket.passenger is not None else ''
                                values['montant'] = round(ticket.transport_cost,2)
                                values['taxe'] = round(ticket.tax,2)
                                values['total'] = round(ticket.total,2)

                                values['passenger_order'] = ticket.passenger.order if ticket.passenger is not None else ''
                                values['issuing_date'] = (ticket.issuing_date).strftime("%d/%m/%Y") if ticket.issuing_date is not None else ''
                                
                                fee = ticket.fees.all()[0]
                                values['fee_type'] = fee.type
                                values['fee_cost'] = round(fee.cost,2)
                                values['fee_taxe'] = round(fee.tax,2)
                                values['fee_total'] = round(fee.total,2)
                                values['fee_issuing_date'] = (fee.ticket.issuing_date).strftime("%d/%m/%Y") if fee.ticket.issuing_date is not None else ''

                                tickets_data.append(values)

                            context['tickets'] = tickets_data

                            # get data other fee
                            other_fees = pnr_data.others_fees.filter((Q(other_fee_status=1) & Q(ticket=None)) | Q(is_invoiced=True)).all()
                            other_fee_data =[]

                            if other_fees is not None:

                                for other_fee in other_fees:
                                    values = {}
                                    values['type'] = other_fee.fee_type
                                    values['billet'] = other_fee.designation
                                    values['passager'] = other_fee.passenger.__str__()
                                    values['montant'] = round(other_fee.cost,2)
                                    values['taxe'] = round(other_fee.tax,2)
                                    values['total'] = round(other_fee.total,2)
                                    values['passenger_segment'] = other_fee.passenger_segment if other_fee.passenger_segment is not None else ''
                                    values['issuing_date'] = (other_fee.creation_date).strftime("%d/%m/%Y") if other_fee.creation_date is not None else ''

                                    fee = ticket.fees.all()[0]
                                    values['fee_type'] = fee.type
                                    values['fee_cost'] = round(fee.cost,2)
                                    values['fee_taxe'] = round(fee.tax,2)
                                    values['fee_total'] = round(fee.total,2)
                                    values['fee_issuing_date'] = (fee.ticket.issuing_date).strftime("%d/%m/%Y") if fee.ticket.issuing_date is not None else ''
                                    
                                    other_fee_data.append(values)

                                context['other_fee'] = other_fee_data
          
                            break
                        except:
                            print('File (EMD) with error: ' + file)
                            traceback.print_exc()
                            context['error'] = traceback.format_exc()
                            context['status'] = 1
                            context['message'] = 'File (EMD) with error: ' + file
                    if contents[j].startswith('TKT'):
                        try:
                            # temp.parse_ticket(temp.needed_content(contents[j:]), temp.get_email_date())

                            ticket_data = temp.test_parse_ticket(temp.needed_content(contents[j:]), temp.get_email_date())

                            pnr_data = ticket_data['pnr']
                            pnr = {'id': pnr_data.id, 'number':pnr_data.number,'status':pnr_data.status}
                            context['pnr'] = pnr

                            # get data segments
                            air_segments = pnr_data.segments.filter(segment_type='Flight', air_segment_status=1).all().order_by('segmentorder')
                            segments_data = []
                            for segment in air_segments:
                                values = {}
                                values['segmentorder'] = segment.segmentorder
                                values['segment'] = segment.__str__()
                                values['flightclass'] = segment.flightclass
                                values['codeorg'] = segment.codeorg.iata_code
                                values['codedest'] = segment.codedest.iata_code
                                values['departuretime'] = segment.departuretime.strftime("%d/%m/%Y, %H:%M:%S") if segment.departuretime is not None else ''
                                values['arrivaltime'] = segment.arrivaltime.strftime("%d/%m/%Y, %H:%M:%S") if segment.arrivaltime is not None else ''
                                values['segment_state'] = segment.segment_state
                                segments_data.append(values)

                            context['segments'] = segments_data

                            # get data ticket
                            tickets = pnr_data.tickets.filter(Q(ticket_status=1) | Q(is_invoiced=True)).filter(Q(total__gt=0) | Q(is_no_adc=True) | (Q(is_refund=True) & Q(total__lt=0))).all().order_by('number')
                            tickets_data = []
                            for ticket in tickets:
                                values = {}
                                if ticket.ticket_type == 'EMD' or ticket.ticket_type == 'TKT':
                                    values['type'] = ticket.ticket_type
                                if ticket.ticket_type == 'CREDIT_NOTE':
                                    values['type'] = 'Avoir'
                            
                                values['billet'] = ticket.__str__()
                                if ticket.ticket_type == 'EMD' and pnr_data.type == 'EWA':
                                    if ticket.ticket_description is not None:
                                        values['passager'] = ticket.ticket_description

                                values['passager'] = ticket.passenger.__str__() if ticket.passenger is not None else ''
                                values['montant'] = round(ticket.transport_cost,2)
                                values['taxe'] = round(ticket.tax,2)
                                values['total'] = round(ticket.total,2)

                                values['passenger_order'] = ticket.passenger.order if ticket.passenger is not None else ''
                                values['issuing_date'] = (ticket.issuing_date).strftime("%d/%m/%Y") if ticket.issuing_date is not None else ''
                                
                                fee = ticket.fees.all()[0]
                                values['fee_type'] = fee.type
                                values['fee_cost'] = round(fee.cost,2)
                                values['fee_taxe'] = round(fee.tax,2)
                                values['fee_total'] = round(fee.total,2)
                                values['fee_issuing_date'] = (fee.ticket.issuing_date).strftime("%d/%m/%Y") if fee.ticket.issuing_date is not None else ''

                                tickets_data.append(values)

                            context['tickets'] = tickets_data

                            # get data other fee
                            other_fees = pnr_data.others_fees.filter((Q(other_fee_status=1) & Q(ticket=None)) | Q(is_invoiced=True)).all()
                            other_fee_data =[]

                            if other_fees is not None:

                                for other_fee in other_fees:
                                    values = {}
                                    values['type'] = other_fee.fee_type
                                    values['billet'] = other_fee.designation
                                    values['passager'] = other_fee.passenger.__str__()
                                    values['montant'] = round(other_fee.cost,2)
                                    values['taxe'] = round(other_fee.tax,2)
                                    values['total'] = round(other_fee.total,2)
                                    values['passenger_segment'] = other_fee.passenger_segment if other_fee.passenger_segment is not None else ''
                                    values['issuing_date'] = (other_fee.creation_date).strftime("%d/%m/%Y") if other_fee.creation_date is not None else ''

                                    fee = ticket.fees.all()[0]
                                    values['fee_type'] = fee.type
                                    values['fee_cost'] = round(fee.cost,2)
                                    values['fee_taxe'] = round(fee.tax,2)
                                    values['fee_total'] = round(fee.total,2)
                                    values['fee_issuing_date'] = (fee.ticket.issuing_date).strftime("%d/%m/%Y") if fee.ticket.issuing_date is not None else ''
                                    
                                    other_fee_data.append(values)

                                context['other_fee'] = other_fee_data
          
                            break
                        except:
                            print('File (Ticket) with error: ' + file)
                            traceback.print_exc()
                            context['error'] = traceback.format_exc()
                            context['status'] = 1
                            context['message'] = 'File (Ticket) with error: ' + file
                    if contents[j].startswith('TST'):
                        try:
                            temp.parse_tst(temp.needed_content(contents[j:]))
                            break
                        except:
                            print('File (TST) with error: ' + file)
                            traceback.print_exc()
                            context['error'] = traceback.format_exc()
                            context['status'] = 1
                            context['message'] = 'File (TST) with error: ' + file
                    if contents[j].startswith('FEE MODIFY REQUEST'):
                        try:
                            temp.sf_decrease_request_update(temp.needed_content(contents[j:]))
                            break
                        except:
                            print('File (REQUEST) with error: ' + file)
                            traceback.print_exc()
                            context['error'] = traceback.format_exc()
                            context['status'] = 1
                            context['message'] = 'File (REQUEST) with error: ' + file
                    if contents[j].startswith('VOTRE NUMERO DE DOSSIER'):
                        try:
                            needed_content = contents[j:]
                            temp.parse_not_issued_zenith(needed_content)
                            break
                        except:
                            print('File (EWA) with error: ' + file)
                            traceback.print_exc()
                            context['error'] = traceback.format_exc()
                            context['status'] = 1
                            context['message'] = 'File (EWA) with error: ' + file
        # context['content'] = data
        return JsonResponse(context, safe=False)
            
    except:
        context['error'] = traceback.format_exc()
        return JsonResponse(context, safe=False)

