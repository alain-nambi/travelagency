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