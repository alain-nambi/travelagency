'''
Created on 8 Sep 2022

'''
import json
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from AmadeusDecoder.models.configuration.Configuration import Configuration
from AmadeusDecoder.utilities.ConfigReader import ConfigReader
import AmadeusDecoder.utilities.configuration_data as configs

@login_required(login_url='index')
def setting(request):
    context = {'configs':configs}
    return render(request,'setting.html',context)    

@login_required(login_url='index')
def email_setting(request):
    context = {'configs':configs, 'env':settings.ENVIRONMENT}
    return render(request,'email_setting.html',context)

@login_required(login_url='index')
def parsing_setting(request):
    pnr_config = Configuration.objects.filter(name="PNR Parser Tools").filter(Q(value_name__icontains="PNR")).all()
    pnr_contact_config = Configuration.objects.filter(name="PNR Parser Tools").filter(Q(value_name__icontains="Contact")).all()
    pnr_config_tools = Configuration.objects.filter(name="PNR Parser Tools").exclude(Q(value_name__icontains="Contact") | Q(value_name__icontains="PNR")).all()
    pnr_ticket_config = Configuration.objects.filter(name="PNR Parser Tools").filter(Q(value_name__icontains="ticket")).all()
     
    context = {'pnr_config':pnr_config, 'pnr_contact_config':pnr_contact_config, 'pnr_config_tools':pnr_config_tools, 'pnr_ticket_config':pnr_ticket_config}
    
    ticket_config = Configuration.objects.filter(name="Ticket Parser Tools").all()
    context['ticket_config'] = ticket_config
    
    tst_config = Configuration.objects.filter(name="TST Parser Tools").all()
    context['tst_config'] = tst_config
    
    zenith_passenger_config = Configuration.objects.filter(name="Zenith Parser Tools").filter(Q(value_name__icontains="Passenger")).all()
    context['zenith_passenger_config'] = zenith_passenger_config
    zenith_config = Configuration.objects.filter(name="Zenith Parser Tools").exclude(Q(value_name__icontains="Passenger")).all()
    context['zenith_config'] = zenith_config
    zenith_receipt_config = Configuration.objects.filter(name="Zenith Receipt Parser Tools").all()
    context['zenith_receipt_config'] = zenith_receipt_config
    
    emd_config = Configuration.objects.filter(name="EMD Parser Tools").all()
    context['emd_config'] = emd_config
    
    return render(request,'parsing_setting.html',context)

@login_required(login_url='index')
def ftp_setting(request):
    return render(request,'ftp_setting.html')

@login_required(login_url='index')
def updateGeneralSetting(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        currency_name = request.POST.get('currency_name')
        currency_code = request.POST.get('currency_code')
        language_code = request.POST.get('language_code')
        regional_country = json.loads(request.POST.get('regional_country'))
        Configuration.objects.filter(name="Company Information",value_name="Name").update(single_value=name)
        Configuration.objects.filter(name="Company Information",value_name="Currency name").update(single_value=currency_name)
        Configuration.objects.filter(name="Company Information",value_name="Currency code").update(single_value=currency_code)
        Configuration.objects.filter(name="Company Information",value_name="Language code").update(single_value=language_code)
        Configuration.objects.filter(name="Company Information",value_name="Regional country").update(array_value=regional_country)
        ConfigReader().load_config()
        
        return JsonResponse('ok',safe=False)
        
@login_required(login_url='index')
def saving_protocol_update(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        Configuration.objects.filter(name="Saving File Tools",environment=settings.ENVIRONMENT).update(dict_value={'link':link})
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)
    
@login_required(login_url='index')
def email_pnr_update(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        Configuration.objects.filter(value_name="Email PNR",environment=settings.ENVIRONMENT).update(dict_value={'address':email, 'password':password})
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)

@login_required(login_url='index')
def email_notif_sender_update(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        port = request.POST.get('port')
        smtp = request.POST.get('smtp')
        valuename = request.POST.get('valuename')
        
        Configuration.objects.filter(value_name=valuename,environment=settings.ENVIRONMENT).update(dict_value={'port':port,'smtp':smtp,'address':email, 'password':password})
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)

@login_required(login_url='index')
def email_notif_update(request):
    if request.method == 'POST':
        email = json.loads(request.POST.get('email'))
        valuename = request.POST.get('valuename')
        
        Configuration.objects.filter(value_name=valuename,environment=settings.ENVIRONMENT).update(array_value=email)
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)
    
@login_required(login_url='index')
def email_fees_update(request):
    if request.method == 'POST':
        email = json.loads(request.POST.get('email'))
        valuename = request.POST.get('valuename')
        print('--------------------------------------')
        print(email)
        print(valuename)
        Configuration.objects.filter(Q(value_name=valuename) & (Q(environment=settings.ENVIRONMENT) | Q(environment='all'))).update(array_value=email)
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)
     
@login_required(login_url='index')
def email_fee_sender_update(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        port = request.POST.get('port')
        smtp = request.POST.get('smtp')
        valuename = request.POST.get('valuename')
        
        Configuration.objects.filter(value_name=valuename,environment=settings.ENVIRONMENT).update(dict_value={'port':port,'smtp':smtp,'address':email, 'password':password})
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)
    
@login_required(login_url='index')
def parsing_update(request):
    tags = json.loads(request.POST.get('tags'))
    print('-----------------------------------------')
    value_name = request.POST.get('valuename')
    print(value_name)
    Configuration.objects.filter(value_name=value_name).update(array_value=tags)
    ConfigReader().load_config()
    return JsonResponse('ok',safe=False)
    
    