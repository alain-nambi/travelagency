'''
Created on 8 Sep 2022

'''
from datetime import datetime,timezone
import json
import traceback
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from AmadeusDecoder.models.configuration.Configuration import Configuration, Config
from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.utilities.AmadeusParser import AmadeusParser
from AmadeusDecoder.utilities.ConfigReader import ConfigReader
from AmadeusDecoder.utilities.ZenithParser import ReceiptException, ZenithParser
import AmadeusDecoder.utilities.configuration_data as configs

@login_required(login_url='index')
def setting(request):  
    return render(request,'setting/setting.html')    
