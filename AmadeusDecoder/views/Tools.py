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
from django.views.decorators.csrf import csrf_exempt

import requests
from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.Fee import Fee, OthersFee

from AmadeusDecoder.utilities.ProductImportParser import ProductParser, CustomerParser
from AmadeusDecoder.models.configuration.Configuration import Configuration
from AmadeusDecoder.models.invoice.CancelSaleOrder import CancelSaleOrder

@csrf_exempt
def cancel_order_sale_from_odoo(request):
    if request.method == 'POST':
        pnr_number = request.POST.get('pnr_number')
        invoice_number = request.POST.get('invoice_number')
        agent = request.POST.get('agent')
        client = request.POST.get('client')
        
        if pnr_number is not None and invoice_number is not None:
            try:
                pnr = Pnr.objects.get(number=pnr_number)
                passenger_invoices = PassengerInvoice.objects.filter(pnr_id=pnr.id, invoice_number=invoice_number).all()
                
                if passenger_invoices:
                    for passenger_invoice in passenger_invoices:
                        # Supprimer la facture passager correspondante si elle existe
                        PassengerInvoice.objects.filter(id=passenger_invoice.id).delete()
                        
                        if passenger_invoice.ticket_id:
                            # Supprimer le billet correspondant s'il existe
                            Ticket.objects.filter(id=passenger_invoice.ticket_id).update(is_invoiced=False)
                        
                        if passenger_invoice.fee_id:
                            # Supprimer les frais correspondants s'ils existent
                            Fee.objects.filter(id=passenger_invoice.fee_id).update(is_invoiced=False)
                            
                        if passenger_invoice.other_fee_id:
                            # Supprimer les autres frais correspondants s'ils existent
                            OthersFee.objects.filter(id=passenger_invoice.other_fee_id).update(is_invoiced=False)
                            
                    
                        print("HELLO")
                        print(passenger_invoice.client, passenger_invoice.ticket, passenger_invoice.fee)    
                        
                        cancel_sale_order = CancelSaleOrder(
                                                pnr=pnr,
                                                client=passenger_invoice.client,
                                                agent=agent,
                                                ticket=passenger_invoice.ticket,
                                                fee=passenger_invoice.fee,
                                                other_fee=passenger_invoice.other_fee,
                                                invoice_number=invoice_number
                                            )
                        
                        cancel_sale_order.save()                            
                    
                    return JsonResponse({'status': 'ok', 'message': f'PNR {pnr_number} a été décommandé sur gestion PNR'}, status=200)
            except Pnr.DoesNotExist:
                return JsonResponse({'message': 'Numéro de PNR introuvable'}, status=404)
            except PassengerInvoice.DoesNotExist:
                return JsonResponse({'message': 'Numéro de facture introuvable'}, status=404)
        else:
            return JsonResponse({'message': 'Numéro de PNR ou de facture non fourni'}, status=400)
    else:
        return JsonResponse({'message': 'Seules les requêtes POST sont autorisées'}, status=405)

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

# def server(request):
#     chemin_api_js = r"..\travelagency\AmadeusDecoder\static\js\pnr_unordering\pnr_unordering.js"
#     commande = ["node", chemin_api_js]
#     processus_api = subprocess.Popen(commande, shell=True)
#     print(processus_api.returncode)
#     return JsonResponse({'message': 'Le serveur NodeJS a été démarré'}, safe=False)
    

    