'''
Created on 8 Sep 2022

'''
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from AmadeusDecoder.models.invoice.Clients import Client
from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice, Pnr

@login_required(login_url='index')
def create_customer(request):
    context = {}

    exists = 0
    if request.method == 'POST':
        if 'Name' and 'FirstName' and 'Address' and 'Country' and 'City' and 'Type' and 'Company' and 'Code_postal' and 'Departement' and 'Email' and 'Phone' in request.POST:
            name = request.POST.get('Name')
            first_name = request.POST.get('FirstName')
            address = request.POST.get('Address')
            email = request.POST.get('Email')
            telephone = request.POST.get('Phone')
            country = request.POST.get('Country')
            city = request.POST.get('City')
            type = request.POST.get('Type')
            company = request.POST.get('Company')
            code_postal = request.POST.get('Code_postal')
            departement = request.POST.get('Departement')

            if type == 'Particulier':
                intitule_string = str(name.strip()) + ' ' + str(first_name.strip())
            else:
                intitule_string = str(company.strip())
                
            intitule = intitule_string.split(' ')
            q = Q()
            last_name, first_name = '', ''
            new_customer = None

            for word in intitule:
                q &= Q(intitule__iexact = word)
            
            customer = Client.objects.filter(q)
            if customer.exists():
                exists = 1
                new_customer = customer.first()
            else:
                exists = 0
                if type == 'Particulier':
                    last_name=name.strip()
                    first_name=first_name.strip()

                elif type == 'Société':
                    last_name=None
                    first_name=None

                new_customer = Client(last_name=last_name,
                                first_name=first_name,
                                intitule=intitule_string.strip(), 
                                address_1=address.strip(),
                                country=country.strip(), 
                                city=city.strip(), 
                                type=type, 
                                code_postal=code_postal.strip(), 
                                departement=departement.strip(), 
                                email=email.strip(), 
                                telephone=telephone.strip())
                new_customer.save() 
            
            context['name'] = name
            context['first_name'] = first_name
            context['intitule'] = intitule_string if type == 'Particulier' else company
            context['customer_id'] = new_customer.id if new_customer is not None else ''
            context['exist'] = exists

    return JsonResponse(context)


@login_required(login_url='index')
def modify_customer_info(request):
    context = {}
    if request.method == 'POST':
        if 'Address' and 'Address_2' and 'Country' and 'City' and 'Code_postal' and 'Departement' and 'Email' and 'Phone' and 'Id' in request.POST:
            id = request.POST.get('Id')
            address = request.POST.get('Address')
            address_2 = request.POST.get('Address_2')
            email = request.POST.get('Email')
            telephone = request.POST.get('Phone')
            country = request.POST.get('Country')
            city = request.POST.get('City')
            code_postal = request.POST.get('Code_postal')
            departement = request.POST.get('Departement')
            customer = Client.objects.filter(pk=id)

            if address is not None and address != '': customer.update(address_1= address)
            if address_2 is not None and address_2 != '': customer.update(address_2= address_2)
            if email is not None and email != '': customer.update(email= email)
            if telephone is not None and telephone != '': customer.update(telephone= telephone)
            if country is not None and country != '': customer.update(country= country)
            if city is not None and city != '': customer.update(city= city)
            if code_postal is not None and code_postal != '': customer.update(code_postal= code_postal)
            if departement is not None and departement != '': customer.update(departement= departement)

    return JsonResponse(context)


@login_required(login_url='index')
def modify_customer_in_passenger_invoice(request):
    context = {}
    if request.method == 'POST':
        if 'PnrId' and 'OldCustomerId' and 'NewCustomerId' in request.POST:
            pnr_id = request.POST.get('PnrId')
            old_client_id = request.POST.get('OldCustomerId')
            new_client_id = request.POST.get('NewCustomerId')

            if pnr_id is not None and old_client_id is not None and new_client_id is not None:
                pnr = Pnr.objects.get(id=pnr_id)
                if pnr.status == 'Emis':
                    # issued pnr
                    passenger_invoice = PassengerInvoice.objects.filter(pnr=pnr_id, client=old_client_id, is_invoiced=False).exclude(status='quotation')
                    if passenger_invoice.exists():
                        passenger_invoice.update(client=new_client_id)
                        context['pnrIssuedUpdated'] = True
                    else:
                        context['pnrIssuedUpdated'] = False
                        
                else:
                    pnr = Pnr.objects.filter(id=pnr_id)
                    if pnr.exists():
                        pnr.update(customer=new_client_id)
                        context['pnrNotIssuedUpdated'] = True            
                    else:
                        context['pnrNotIssuedUpdated'] = False
                        
                    # not issued pnr (update in passenger_invoice table)
                    passenger_invoice = PassengerInvoice.objects.filter(pnr=pnr_id, client=old_client_id, is_quotation=False).exclude(status='sale')
                    if passenger_invoice.exists():
                        passenger_invoice.update(client=new_client_id)
                        context['pnrNotIssuedUpdated'] = True
                        
                        
    return JsonResponse(context)

@login_required(login_url='index')
def delete_customer(request, pnr_id):
    context = {}

    if request.method == 'POST':
        pnr = Pnr.objects.get(pk=pnr_id)
        if 'customerId' in request.POST:
            customer_id = request.POST.get('customerId')
            if customer_id != '':
                if pnr.status_value == 0:
                    orders = PassengerInvoice.objects.filter(pnr=pnr_id, client=customer_id, status='sale', is_invoiced=False)
                elif pnr.status_value == 1:
                    orders = PassengerInvoice.objects.filter(pnr=pnr_id, client=customer_id, status='quotation')
                if orders.exists():
                    orders.delete()
                    if pnr.status_value == 1:
                        pnr.customer = None
                        pnr.save()

    return JsonResponse(context)


@login_required(login_url='index')
def customers(request):  
    context = {}
    context['clients'] = Client.objects.all()
    
    object_list = context['clients']
    row_num = request.GET.get('paginate_by', 50) or 50
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, row_num)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger: 
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {'page_obj': page_obj, 'row_num': row_num}
    return render(request,'manage_customers.html', context)    

