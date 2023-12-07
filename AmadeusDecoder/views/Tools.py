'''
Created on 8 Sep 2022

'''
import os
import shlex
import subprocess
import time

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
from AmadeusDecoder.models.pnr.Pnr import Pnr

from AmadeusDecoder.utilities.ProductImportParser import ProductParser, CustomerParser
from AmadeusDecoder.models.configuration.Configuration import Configuration

@login_required(login_url='index')
def tools(request):  
    return render(request,'tools.html')


def call_product_import(request):
    
    status = ''
    try:
        directory = '/opt/issoufali/odoo/issoufali-addons/sync_products/data/exported/'
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
        directory = '/opt/issoufali/odoo/issoufali-addons/export_contacts/data/exported/'
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
    

    