'''
Created on 8 Sep 2022

'''
from base64 import b64encode
from datetime import datetime,timezone
import json
import os
import traceback
from django.http import FileResponse, JsonResponse
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from AmadeusDecoder.models.configuration.Configuration import Configuration, Config
from AmadeusDecoder.utilities.AmadeusParser import AmadeusParser
from AmadeusDecoder.utilities.ConfigReader import ConfigReader
from AmadeusDecoder.utilities.ZenithParser import ZenithParser
from AmadeusDecoder.utilities.ZenithParserReceipt import ZenithParserReceipt
import AmadeusDecoder.utilities.configuration_data as configs

@login_required(login_url='index')
def setting(request):

    ConfigReader().load_config()
    context = {'state':"true",'state_file_protocol':"true",'configs':configs,'env':settings.ENVIRONMENT}
    
    if configs.COMPANY_NAME is None and configs.COMPANY_CURRENCY_NAME is None and configs.COMPANY_CURRENCY_CODE is None and configs.COMPANY_LANGUAGE_CODE is None:
        context['state'] = "false"
    
    if configs.FILE_PROTOCOL is None:
        context['state_file_protocol'] = "false"

    return render(request,'setting.html',context)    

@login_required(login_url='index')
def email_setting(request):
    ConfigReader().load_config()

    configurations = Configuration.objects.filter(name="Email Source").filter(Q(environment=settings.ENVIRONMENT)).filter(Q(value_name__icontains="recipients")).all()

    value_name_to_exclude = [config.value_name for config in configurations]
    email_recipients_value_name = Config.objects.filter(name="Email Source").filter(Q(value_name__icontains="recipients")).exclude(value_name__in=value_name_to_exclude).all()

    context = {'configs':configs, 'env':settings.ENVIRONMENT,'state_email_pnr':"true",'state_email_recipients':"complet",'state_email_sender':"complet",'email_recipients_value_name':email_recipients_value_name}
    
    email_recipients = Configuration.objects.filter(name="Email Source").filter(Q(value_name__icontains="notification recipients")).filter(Q(environment=settings.ENVIRONMENT)).all()
    context['email_recipients'] = email_recipients
    if not email_recipients.exists():
        context['state_email_recipients']="vide"
    if len(email_recipients_value_name) !=0 and len(email_recipients) !=0:
        context['state_email_recipients'] = "incomplet" 
    if configs.EMAIL_PNR == {}: 
        context['state_email_pnr'] = "false"


    email_sender_configurations = Configuration.objects.filter(name="Email Source").filter(Q(environment=settings.ENVIRONMENT)).filter(Q(value_name__icontains="sender")).all()
    email_sender_value_name_to_exclude = [config.value_name for config in email_sender_configurations]
    email_sender_value_name = Config.objects.filter(name="Email Source").filter(Q(value_name__icontains="sender")).exclude(value_name__in=email_sender_value_name_to_exclude).all()
    email_sender = Configuration.objects.filter(name="Email Source").filter(Q(value_name__icontains="sender")).filter(Q(environment=settings.ENVIRONMENT)).all()
    context['email_sender'] = email_sender
    context ['email_sender_value_name'] = email_sender_value_name
    if not email_sender.exists():
        context['state_email_sender']="vide"
    if len(email_sender_value_name) !=0 and len(email_sender) !=0:
        context['state_email_sender'] = "incomplet" 

        
    email_fee_sender_config = []
    email_fee_sender_config.extend( Configuration.objects.filter(name="Email Source").filter(Q(environment=settings.ENVIRONMENT)).filter(Q(value_name__icontains="Fee")).filter(Q(value_name__icontains="sender")).all() )
    
    email_fee_sender_config.extend( Configuration.objects.filter(Q(environment=settings.ENVIRONMENT)).filter(Q(name="Report Email") | Q(name="Fee Request Tools")).filter(Q(value_name__icontains="sender")).all())
    
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print(email_fee_sender_config)
    
    email_fee_sender_value_name_to_be_exclude = [config.value_name for config in email_fee_sender_config]
    
    print(email_fee_sender_value_name_to_be_exclude)
    
    email_fee_sender = []
    email_fee_sender.extend( Configuration.objects.filter(name="Email Source").filter(Q(environment=settings.ENVIRONMENT)).filter(Q(value_name__icontains="Fee")).filter(Q(value_name__icontains="sender")).all() )
    
    email_fee_sender.extend( Configuration.objects.filter(Q(environment=settings.ENVIRONMENT)).filter(Q(name="Report Email") | Q(name="Fee Request Tools")).filter(Q(value_name__icontains="sender")).all())
    
    email_fee_sender_value_name = []
    email_fee_sender_value_name.extend( Config.objects.filter(name="Email Source").filter(Q(value_name__icontains="Fee")).filter(Q(value_name__icontains="sender")).exclude(value_name__in=email_fee_sender_value_name_to_be_exclude).all() )
    email_fee_sender_value_name.extend( Config.objects.filter(Q(name="Report Email") | Q(name="Fee Request Tools")).filter(Q(value_name__icontains="sender")).exclude(value_name__in=email_fee_sender_value_name_to_be_exclude).all())
    

    context['email_fee_sender_value_name'] = email_fee_sender_value_name
    context['email_fee_sender'] = email_fee_sender
    context['state_email_fee_sender'] = "complet"
    if not email_fee_sender :
        context['state_email_fee_sender']="vide"
    if len(email_fee_sender_value_name) !=0 and len(email_fee_sender) !=0:
        context['state_email_fee_sender'] = "incomplet" 
    
    email_fee_configurations = Configuration.objects.filter(name="Email Source").filter(Q(environment=settings.ENVIRONMENT)).filter(Q(name="Email Source") | Q(name="Report Email") | Q(name="Fee Request Tools")).filter(Q(value_name__icontains="recipient")).all()
    
    email_fee_value_name_to_exclude = [config.value_name for config in email_fee_configurations]
    
    email_fee_recipients = Configuration.objects.filter(Q(name="Email Source") | Q(name="Report Email") | Q(name="Fee Request Tools")).filter(Q(environment=settings.ENVIRONMENT) | Q(environment="all")).filter(Q(value_name__icontains="recipient")).filter(Q(value_name__icontains="fee")).all()
    
    email_fee_value_name = Config.objects.filter(Q(name="Email Source") | Q(name="Report Email") | Q(name="Fee Request Tools")).filter(Q(value_name__icontains="recipient")).filter(Q(value_name__icontains="fee")).exclude(value_name__in=email_fee_value_name_to_exclude).all()

    context['email_fee_value_name'] = email_fee_value_name
    context['email_fee_recipients'] = email_fee_recipients
    context['state_email_fee'] = "complet"
    if not email_fee_recipients.exists():
        context['state_email_fee']="vide"
    if len(email_fee_value_name) !=0 and len(email_fee_recipients) !=0:
        context['state_email_fee'] = "incomplet" 

        
    return render(request,'email_setting.html',context)

@login_required(login_url='index')
def parsing_setting(request):
    ConfigReader().load_config()
    
    configurations = Configuration.objects.filter(name="PNR Parser Tools").all()
    value_name_to_exclude = [config.value_name for config in configurations]
    pnr_value_name = Config.objects.filter(name="PNR Parser Tools").exclude(value_name__in=value_name_to_exclude).all()
    
    pnr_config = Configuration.objects.filter(name="PNR Parser Tools").filter(Q(value_name__icontains="PNR")).all()
    pnr_contact_config = Configuration.objects.filter(name="PNR Parser Tools").filter(Q(value_name__icontains="Contact")).all()
    pnr_config_tools = Configuration.objects.filter(name="PNR Parser Tools").exclude(Q(value_name__icontains="Contact") | Q(value_name__icontains="PNR") |Q(value_name__icontains="ticket") ).all()
    pnr_ticket_config = Configuration.objects.filter(name="PNR Parser Tools").filter(Q(value_name__icontains="ticket")).all()
    context = {'pnr_config':pnr_config, 'pnr_contact_config':pnr_contact_config, 'pnr_config_tools':pnr_config_tools, 'pnr_ticket_config':pnr_ticket_config,'pnr_state':'complet'}

    if not pnr_config.exists() or not pnr_contact_config.exists() or not pnr_config_tools.exists() or not pnr_ticket_config.exists() or len(pnr_value_name) != 0:
        context['pnr_state'] = "incomplet"
        
    if not pnr_config.exists() and not pnr_contact_config.exists() and not pnr_config_tools.exists() and not pnr_ticket_config.exists():
        context['pnr_state'] = "vide"

    ticket_configurations = Configuration.objects.filter(name="Ticket Parser Tools").all()
    ticket_value_name = Config.objects.filter(name="Ticket Parser Tools").exclude(value_name__in=[config.value_name for config in ticket_configurations]).all()
    context['ticket_value_name'] = ticket_value_name
    context['ticket_state'] = "complet"
    ticket_config = Configuration.objects.filter(name="Ticket Parser Tools").all()
    context['ticket_config'] = ticket_config
    if len(ticket_value_name) !=0 and len(ticket_config) !=0:
        context['ticket_state'] = "incomplet" 
    if not ticket_config.exists():
        context['ticket_state'] = "vide"
        
    tst_configurations = Configuration.objects.filter(name="TST Parser Tools").all()
    tst_value_name = Config.objects.filter(name="TST Parser Tools").exclude(value_name__in=[config.value_name for config in tst_configurations]).all()
    context['tst_value_name'] = tst_value_name
    context['tst_state'] = "complet"
    tst_config = Configuration.objects.filter(name="TST Parser Tools").all()
    context['tst_config'] = tst_config
    if len(tst_value_name) !=0 and len(tst_config) !=0:
        context['tst_state'] = "incomplet" 
    if not tst_config.exists():
        context['tst_state'] = "vide"
    
    zenith_configurations = Configuration.objects.filter(name="Zenith Parser Tools").all()
    zenith_value_name = Config.objects.filter(name="Zenith Parser Tools").exclude(value_name__in=[config.value_name for config in zenith_configurations]).all()
    context['zenith_value_name'] = zenith_value_name
    context['zenith_state'] = "complet"
    zenith_passenger_config = Configuration.objects.filter(name="Zenith Parser Tools").filter(Q(value_name__icontains="Passenger")).all()
    context['zenith_passenger_config'] = zenith_passenger_config
    zenith_config = Configuration.objects.filter(name="Zenith Parser Tools").exclude(Q(value_name__icontains="Passenger")).all()
    context['zenith_config'] = zenith_config
    if len(zenith_value_name) !=0 and len(zenith_config) !=0:
        context['zenith_state'] = "incomplet" 
    if not zenith_config.exists():
        context['zenith_state'] = "vide"
        
    
    zenith_receipt_configurations = Configuration.objects.filter(name="Zenith Receipt Parser Tools").all()
    zenith_receipt_value_name = Config.objects.filter(name="Zenith Receipt Parser Tools").exclude(value_name__in=[config.value_name for config in zenith_receipt_configurations]).all()
    context['zenith_receipt_value_name'] = zenith_receipt_value_name
    context['zenith_receipt_state'] = "complet"
    zenith_receipt_config = Configuration.objects.filter(name="Zenith Receipt Parser Tools").all()
    context['zenith_receipt_config'] = zenith_receipt_config
    if len(zenith_receipt_value_name) !=0 and len(zenith_receipt_config)!= 0:
        context['zenith_receipt_state'] = "incomplet" 
    if not zenith_receipt_config.exists():
        context['zenith_receipt_state'] = "vide"

    
    emd_configurations = Configuration.objects.filter(name="EMD Parser Tools").all()
    emd_value_name = Config.objects.filter(name="EMD Parser Tools").exclude(value_name__in=[config.value_name for config in emd_configurations]).all()
    context['emd_value_name'] = emd_value_name
    context['emd_state'] = "complet"
    emd_config = Configuration.objects.filter(name="EMD Parser Tools").exclude(value_name="EMD statuses").all()
    context['emd_config'] = emd_config
    emd_statues = Configuration.objects.filter(name="EMD Parser Tools",value_name="EMD statuses").first()
    if len(emd_value_name) !=0 and len(emd_config)!= 0:
        context['emd_state'] = "incomplet" 
    if not emd_config.exists():
        context['emd_state'] = "vide"
    if emd_statues is not None:
        context['emd_statues'] = emd_statues.dict_value.items()
        
    

    context['pnr_value_name'] = pnr_value_name
    print(context['pnr_state'])
    return render(request,'parsing_setting.html',context)

@login_required(login_url='index')
def ftp_setting(request):
    return render(request,'ftp_setting.html')

# ---------------- All Update Function -----------------

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
        hostname = request.POST.get('hostname')
        port = request.POST.get('port')
        username = request.POST.get('username')
        password = request.POST.get('password')
        repository = request.POST.get('repository')
        storage = request.POST.get('storage')
        
        if hostname is not None and port is not None and username is not None and password is not None and repository is not None:
            dict_value = {"hostname":hostname, "port":port, "username":username, "password":password, "repository":repository, "link":link}
        else:
            dict_value = {"link":link}

        Configuration.objects.filter(name="Saving File Tools",environment=settings.ENVIRONMENT).update(single_value=storage,dict_value=dict_value)
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
        Configuration.objects.filter(value_name=valuename).update(array_value=email)
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
    value_name = request.POST.get('valuename')
    array_of_array_value = []

    for tag in tags:
        tag = tag.split(',')
        print(tag)
        array_of_array_value.append(tag)
       
    if value_name == "Itinerary header possible format":
        Configuration.objects.filter(value_name=value_name).update(array_of_array_value=array_of_array_value)
    else:
        Configuration.objects.filter(value_name=value_name).update(array_value=tags)

    ConfigReader().load_config()
    return JsonResponse('ok',safe=False)
    
# ---------------------------- All Create Function -----------------------
@login_required(login_url='index')
def general_information_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        currency_name = request.POST.get('currency_name')
        currency_code = request.POST.get('currency_code')
        language_code = request.POST.get('language_code')
        regional_country = json.loads(request.POST.get('regional_country'))
        
        company_name_config = Configuration(environment='all',name='Company Information',to_be_applied_on="Global",value_name='Name',single_value=name)
        company_currency_config = Configuration(environment='all',name='Company Information',to_be_applied_on="Global",value_name='Currency name',single_value=currency_name)
        company_currency_code_config = Configuration(environment='all',name='Company Information',to_be_applied_on="Global",value_name='Currency code',single_value=currency_code)
        company_language_config = Configuration(environment='all',name='Company Information',to_be_applied_on="Global",value_name='Language code',single_value=language_code)
        company_regional_country_config = Configuration(environment='all',name='Company Information',to_be_applied_on="Global",value_name='Regional country',array_value=regional_country)
        
        company_currency_code_config.save()
        company_currency_config.save()
        company_language_config.save()
        company_regional_country_config.save()
        company_name_config.save()

        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)

@login_required(login_url='index')
def general_file_protocol_create(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        hostname = request.POST.get('hostname')
        port = request.POST.get('port')
        username = request.POST.get('username')
        password = request.POST.get('password')
        repository = request.POST.get('repository')
        storage = request.POST.get('storage')
        
        config = Config.objects.get(value_name = 'File protocol')
        
        if hostname is not None and port is not None and username is not None and password is not None and repository is not None:
            dict_value = {"hostname":hostname, "port":port, "username":username, "password":password, "repository":repository, "link":link}
        else:
            dict_value = {"link":link}

        config_file_protocol =  Configuration(environment=settings.ENVIRONMENT,name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,single_value=storage,dict_value= dict_value)
        config_file_protocol.save()
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)

@login_required(login_url='index')
def email_pnr_create(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        dict_value = {"address":email,"password":password}
        email_pnr_config = Configuration(environment=settings.ENVIRONMENT,name='Email Source',to_be_applied_on="Global",value_name='Email PNR',dict_value=dict_value)
        email_pnr_config.save()
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)

@login_required(login_url='index')
def email_notification_recipients_create(request):
    if request.method == 'POST':
        email = json.loads(request.POST.get('email'))
        value_name_id = request.POST.get('value_name_id')
        config = Config.objects.get(pk=value_name_id)
        
        email_notif_config = Configuration(environment=settings.ENVIRONMENT,name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,array_value=email)
        email_notif_config.save()
        
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)
    
@login_required(login_url='index')
def email_notification_sender_create(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        value_name_id = request.POST.get('value_name_id')
        password = request.POST.get('password')
        smtp = request.POST.get('smtp')
        port = request.POST.get('port')
        
        config = Config.objects.get(pk=value_name_id)
        dict_value = {"address":email,"password":password,"smtp":smtp,"port":port}
        email_notif_config = Configuration(environment=settings.ENVIRONMENT,name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,dict_value=dict_value)
        email_notif_config.save()
        
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)

@login_required(login_url='index')
def email_fee_sender_create(request):
    if request.method == 'POST':
        config_id = request.POST.get('config_id')
        config = Config.objects.get(id=config_id)
        email = request.POST.get('email')
        password = request.POST.get('password')
        smtp = request.POST.get('smtp')
        port = request.POST.get('port')
        dict_value={'port':port,'smtp':smtp,'address':email, 'password':password}
        
        email_notif_config = Configuration(environment=settings.ENVIRONMENT,name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,dict_value=dict_value)
        email_notif_config.save()
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)
    
@login_required(login_url='index')
def email_fee_recipient_create(request):
    if request.method == 'POST':
        config_id = request.POST.get('value_name')
        value = json.loads(request.POST.get('value'))
        config = Config.objects.get(id=config_id)
        fee_receipt_config = Configuration(environment=settings.ENVIRONMENT,name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,array_value=value)
        if config.name =="Fee Request Tools":
            fee_receipt_config = Configuration(environment="all",name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,array_value=value)

        
        fee_receipt_config.save()
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)
    
    # All Parsing Create Function

@login_required(login_url='index')
def pnr_parsing_create(request):
    if request.method == 'POST':
        value_name_id = request.POST.get('value_name')
        value = json.loads(request.POST.get('value'))
        
        config = Config.objects.get(pk=value_name_id)
        
        pnr_config = Configuration(environment="all",name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,array_value=value)
        dict_value={}
        if config.value_name == 'Contact type names':
            for element in value:
                cle, valeur = element.split(':')
                dict_value[cle] = valeur
                
            pnr_config = Configuration(environment="all",name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,dict_value=dict_value)
            
        pnr_config.save()
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)
    
@login_required(login_url='index')
def ticket_parsing_create(request):
    if request.method == 'POST':
        value_name_id = request.POST.get('value_name')
        value = json.loads(request.POST.get('value'))
        
        config = Config.objects.get(pk=value_name_id)
        
        ticket_config = Configuration(environment="all",name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,array_value=value)
        ticket_config.save()
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)
    
@login_required(login_url='index')
def tst_parsing_create(request):
    if request.method == 'POST':
        value_name_id = request.POST.get('value_name')
        value = json.loads(request.POST.get('value'))
        
        config = Config.objects.get(pk=value_name_id)
        
        tst_config = Configuration(environment="all",name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,array_value=value)
        tst_config.save()
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)
    
@login_required(login_url='index')
def zenith_parsing_create(request):
    if request.method == 'POST':
        value_name_id = request.POST.get('value_name')
        value = json.loads(request.POST.get('value'))
        array_of_array_value = []
        for element in value:
            element = element.split(',')
            array_of_array_value.append(element)

        config = Config.objects.get(pk=value_name_id)

        if config.id == 57:
            zenith_config = Configuration(environment="all",name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,array_of_array_value=array_of_array_value)
        else:
            zenith_config = Configuration(environment="all",name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,array_value=value)
            
        zenith_config.save()
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)

@login_required(login_url='index')
def zenith_receipt_parsing_create(request):
    if request.method == 'POST':
        value_name_id = request.POST.get('value_name')
        value = json.loads(request.POST.get('value'))
        
        config = Config.objects.get(pk=value_name_id)
        
        zenith_receipt_config = Configuration(environment="all",name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,array_value=value)
        zenith_receipt_config.save()
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)
    
@login_required(login_url='index')
def emd_parsing_create(request):
    if request.method == 'POST':
        value_name_id = request.POST.get('value_name')
        value = json.loads(request.POST.get('value'))
        
        config = Config.objects.get(pk=value_name_id)
        
        zenith_receipt_config = Configuration(environment="all",name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,array_value=value)
        dict_value={}
        if config.value_name == 'EMD statuses':
            for element in value:
                cle, valeur = element.split(':')
                dict_value[cle] = valeur
                
            zenith_receipt_config = Configuration(environment="all",name=config.name,to_be_applied_on=config.to_be_applied_on,value_name=config.value_name,dict_value=dict_value)
        zenith_receipt_config.save()
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)

@login_required(login_url='index')
def emd_statues_update(request):
    if request.method == 'POST':
        dict_value={}
        statues = json.loads(request.POST.get('statues'))
        config = Configuration.objects.filter(name='EMD Parser Tools',value_name='EMD statuses').first()
                
        config.dict_value = statues
        config.save()
        ConfigReader().load_config()
        return JsonResponse('ok',safe=False)
    
    
def test_parsing(request):
    return render(request,'test_parsing.html')  

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

            temp.parse_pnr(temp.get_email_date())
            temp.get_creator_emitter()
            
            
        except:
            trace_str = traceback.format_exc()
            print(trace_str)
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

        with open(chemin,'r') as fichier:
            lines = fichier.readlines()

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
                            temp.parse_pnr(contents[j:], needed_content, temp.get_email_date())
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
                            temp.parse_emd(temp.needed_content(contents[j:]), temp.get_email_date())
                            break
                        except:
                            print('File (EMD) with error: ' + file)
                            traceback.print_exc()
                            context['error'] = traceback.format_exc()
                            context['status'] = 1
                            context['message'] = 'File (EMD) with error: ' + file
                    if contents[j].startswith('TKT'):
                        try:
                            temp.parse_ticket(temp.needed_content(contents[j:]), temp.get_email_date())
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
        context['content'] = data
        return JsonResponse(context, safe=False)
            
    except:
        context['error'] = traceback.format_exc()
        return JsonResponse(context, safe=False)


