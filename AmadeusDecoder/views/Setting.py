'''
Created on 8 Sep 2022

'''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import AmadeusDecoder.utilities.configuration_data as configs

@login_required(login_url='index')
def setting(request):  
    context = {'configs':configs}
    return render(request,'setting.html',context)    

@login_required(login_url='index')
def email_setting(request):
    return render(request,'email_setting.html')

@login_required(login_url='index')
def parsing_setting(request):
    return render(request,'parsing_setting.html')

@login_required(login_url='index')
def ftp_setting(request):
    return render(request,'ftp_setting.html')