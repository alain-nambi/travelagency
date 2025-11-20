'''
Created on 8 Sep 2022

'''
from datetime import datetime, timezone
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
    context['clients'] = Client.objects.all().order_by('intitule')
    pnr_not_invoiced = get_pnr_created_today_not_invoiced(request)
    context['pnr_not_invoiced'] = pnr_not_invoiced
    context['notif_number'] = len(pnr_not_invoiced)
    
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
    context['page_obj'] =  page_obj
    context['row_num'] =  row_num
    context['pnr_count'] = paginator.count

    return render(request,'manage_customers.html', context)    

# ------- Notification ---------------------------------
def get_pnr_created_today_not_invoiced(request):
    # get number of pnr not invoiced today
    today = datetime.now().date()
    
    start_date = datetime(today.year, today.month, today.day, 0, 0, 0, tzinfo=timezone.utc)
    end_date = datetime(today.year, today.month, today.day, 23, 59, 59, tzinfo=timezone.utc)

    pnrs = Pnr.objects.filter(agent_id= request.user.id,system_creation_date__range=[start_date, end_date], is_invoiced= False)
    nbre_pnr = pnrs.count()
    return pnrs

def customer_details(request,customer_id):
    details = Client.objects.get(pk=customer_id)
    context = {'customer' : details}
    return render(request,'customer.html',context)

@login_required(login_url='index')
def modify_customer(request):
    context = {}
    if request.method == 'POST':
        
        id = request.POST.get('Id')
        address = request.POST.get('Address')
        address_2 = request.POST.get('Address_2')
        email = request.POST.get('Email')
        telephone = request.POST.get('Phone')
        country = request.POST.get('Country')
        city = request.POST.get('City')
        code_postal = request.POST.get('Code_postal')
        departement = request.POST.get('Departement')
        intitule = request.POST.get('intitule')
        
        customer = Client.objects.filter(pk=id)     
        
        connected_user_id = request.POST.get('connected_user')
        password = request.POST.get('password')
        
        connected_user = User.objects.get(pk=connected_user_id)
        connected_user_authenticated = authenticate(request, username=connected_user.email, password=password)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        
        print(telephone)
        if connected_user_authenticated is not None:
            if address is not None and address != '': customer.update(address_1= address)
            if address_2 is not None and address_2 != '': customer.update(address_2= address_2)
            if email is not None and email != '': customer.update(email= email)
            if telephone is not None and telephone != '': 
                print('telephone var mi')
                customer.update(telephone= telephone)
            if country is not None and country != '': customer.update(country= country)
            if city is not None and city != '': customer.update(city= city)
            if code_postal is not None and code_postal != '': customer.update(code_postal= code_postal)
            if departement is not None and departement != '': customer.update(departement= departement)
            if intitule is not None and intitule != '': customer.update(intitule= intitule)
            
            context['message'] = "Informations modifiées"
            context['status'] = 200

        else:
            context['message'] = "Mot de passe incorrect"
            context['status'] = 10

    return JsonResponse(context)

def search_customers(request):
    query = request.GET.get('query', '') # Utilisez request.GET pour les recherches
    page_number = request.GET.get('page', 1) # Pour la pagination après recherche
    
    print("QUERY :", query)
    print("page_number :", page_number)
    

    if query:
        # Recherche insensible à la casse sur plusieurs champs
        customers = Client.objects.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(address_1__icontains=query) |
            Q(type__icontains=query) |
            Q(country__icontains=query) |
            Q(intitule__icontains=query) # Incluez le champ intitule
        ).order_by('last_name', 'first_name', 'intitule') # Tri par intitule aussi

        # Exclure les noms nuls ou vides, comme discuté précédemment
        # customers = customers.filter(
        #     ~Q(last_name__isnull=True) | ~Q(first_name__isnull=True) | ~Q(intitule__isnull=True)
        # ).exclude(last_name__exact='').exclude(first_name__exact='').exclude(intitule__exact='')

    else:
        customers = Client.objects.all().order_by('last_name', 'first_name', 'intitule')
        # Exclure les noms nuls ou vides
        customers = customers.filter(
            ~Q(last_name__isnull=True) | ~Q(first_name__isnull=True) | ~Q(intitule__isnull=True)
        ).exclude(last_name__exact='').exclude(first_name__exact='').exclude(intitule__exact='')


    # --- Gestion de la pagination (si nécessaire) ---
    from django.core.paginator import Paginator
    paginator = Paginator(customers, 50) # 10 clients par page
    page_obj = paginator.get_page(page_number)

    # Préparer les données pour la réponse JSON
    results = []
    for client in page_obj:
        # Construisez un dictionnaire pour chaque client
        # et gérez la logique last_name/first_name/intitule ici aussi si vous voulez
        # que le front-end reçoive la valeur "finale"
        display_name_col1 = ''
        display_name_col2 = ''

        if client.last_name and client.first_name:
            display_name_col1 = client.last_name
            display_name_col2 = client.first_name
        elif client.last_name:
            display_name_col1 = client.last_name
        elif client.first_name:
            display_name_col1 = client.first_name
        else:
            display_name_col1 = client.intitule if client.intitule else ''

        results.append({
            'id': client.id,
            'last_name': display_name_col1, # Ceci est le contenu de la 1ère colonne
            'first_name': display_name_col2, # Ceci est le contenu de la 2ème colonne
            'intitule': client.intitule,
            'address_1': client.address_1,
            'type': client.type,
            'country': client.country,
            # Ajoutez d'autres champs si nécessaire
        })
        print("***************** RESULT ************ :",results)
        

    return JsonResponse({
        'results': results,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'total_results': paginator.count,
    })