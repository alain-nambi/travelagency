'''
Created on 8 Sep 2022

'''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from AmadeusDecoder.utilities.ProductImportParser import ProductParser, CustomerParser

@login_required(login_url='index')
def tools(request):  
    return render(request,'tools.html')


def call_product_import(request):
    path_to_file = '/opt/odoo/issoufali-addons/sync_products/data/exported/Products.csv'
    ProductParser.import_product(path_to_file)

    return None


def call_customer_import(request):
    path_to_file = '/opt/odoo/issoufali-addons/sync_contacts/data/exported/Contacts.csv'
    CustomerParser.import_customer(path_to_file)

    return None
