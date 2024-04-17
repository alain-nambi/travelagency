'''
Created on 8 Sep 2022

'''
import base64
import datetime
import io
from itertools import count
import os
import shlex
import subprocess
import time

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
from AmadeusDecoder.models.pnr.Passenger import Passenger
from AmadeusDecoder.models.pnr.Pnr import Pnr

from AmadeusDecoder.models.pnrelements.Airline import Airline
from AmadeusDecoder.models.pnrelements.Airport import Airport
from AmadeusDecoder.models.pnrelements.PnrAirSegments import PnrAirSegments
from AmadeusDecoder.utilities.ProductImportParser import ProductParser, CustomerParser
from AmadeusDecoder.models.configuration.Configuration import Configuration

from django.db.models import Count
from django.db.models.functions import Lower, ExtractYear

@login_required(login_url='index')
def tools(request):  
    return render(request,'tools.html')


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

# ------------------------ STATISTIQUES -----------------------------------------------------------------

def graph_view(request):

    context = {}
    
    context['passenger_by_age'] = get_passenger_by_age(request)
    context['all_data'] = get_destination_by_month(request)
    context['all_data_origin'] = get_origin_by_month(request)
    context['all_data_airline'] = get_stat_airlines(request)
    
    return render(request, 'stat.html', context)  

def get_stat_airlines(request):
    # month = datetime.datetime.now().month
    month = 3
    all_year = PnrAirSegments.objects.annotate(year=ExtractYear('departuretime')).values('year').distinct()
    all_data = []
    for element in all_year:
        if element['year'] is not None:
            data = []
            
            queryset = PnrAirSegments.objects.annotate(total= Count('servicecarrier_id')).filter( departuretime__month=month,departuretime__year = element['year']).values('servicecarrier_id','total').annotate(total_count=Count('servicecarrier_id')).filter(total_count__gt=10)
            if queryset.exists():
                data.append(str(element['year']))
                for item in queryset:
                    airline = Airline.objects.get(pk = item['servicecarrier_id'])
                    data.append({"y":item['total_count'],"label":airline.name}) 
                    
                all_data.append(data)
    print('all_data',all_data)    
    return all_data
    

def get_destination_by_month(request):
    # month = datetime.datetime.now().month
    month = 12
    all_year = PnrAirSegments.objects.annotate(year=ExtractYear('departuretime')).values('year').distinct()
    all_data = []
    for element in all_year:
        if element['year'] is not None:
            data = []

            print(element['year'])
            # destination
            
            queryset = PnrAirSegments.objects.annotate(total= Count('codedest_id')).filter( departuretime__month=month,departuretime__year = element['year']).values('codedest_id','total').annotate(total_count=Count('codedest_id')).filter(total_count__gt=10)
            if queryset.exists():
                data.append(str(element['year']))
                for item in queryset:
                    airport = Airport.objects.get(iata_code = item['codedest_id'])
                    
                    if airport.name is not None:
                        data.append({"y":item['total_count'],"label":airport.name})
                    if airport.name is None:
                        data.append({"y":item['total_count'],"label":item['codedest_id']}) 
                all_data.append(data)

    return all_data

def get_origin_by_month(request):
    # month = datetime.datetime.now().month
    month = 12
    all_year = PnrAirSegments.objects.annotate(year=ExtractYear('departuretime')).values('year').distinct()
    all_data = []
    for element in all_year:
        if element['year'] is not None:
            data = []
            
            queryset = PnrAirSegments.objects.annotate(total= Count('codeorg_id')).filter( departuretime__month=month,departuretime__year = element['year']).values('codeorg_id','total').annotate(total_count=Count('codeorg_id')).filter(total_count__gt=10)
            if queryset.exists():
                data.append(str(element['year']))
                for item in queryset:
                    airport = Airport.objects.get(iata_code = item['codeorg_id'])
                    
                    if airport.name is not None:
                        data.append({"y":item['total_count'],"label":airport.name})
                    if airport.name is None:
                        data.append({"y":item['total_count'],"label":item['codeorg_id']}) 
                all_data.append(data)

    return all_data

def get_passenger_by_age(request):


    queryset = Passenger.objects.annotate(lower_designation=Lower('designation')).values('lower_designation').annotate(total=Count('id'))
    data = []
    total_adt = 0
    total_chd = 0
    total = 0
    for item in queryset:
        total += item['total']

    for item in queryset:
        if item['lower_designation'] in ['bébé']:
            data.append({ "label": "Bébé", "y": (item['total'] * 100)/total })

        if item['lower_designation'] in ['enfant','inf','chd']:
            total_chd += item['total']

        if item['lower_designation'] in ['yth']:
            data.append({ "label": "Jeune", "y": (item['total'] * 100)/total })

        if item['lower_designation'] is None:
            data.append({ "label": "Inconnu", "y": (item['total'] * 100)/total })

        if item['lower_designation'] in ['mrs','ms','mlle','adt','m.','mme','mr','mstr','dr','cnn']:
            total_adt += item['total'] 
        
        
    data.append({ "label": "Adulte", "y": (total_adt * 100)/total }) 
    data.append({ "label": "Enfant", "y":  (total_chd * 100)/total }) 
    

    return data