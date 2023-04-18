'''
Created on 8 Sep 2022

'''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from AmadeusDecoder.models.pnr.Pnr import Pnr 

@login_required(login_url='index')
def dashboard(request):  
    context = {}
    pnr_0 = Pnr.objects.filter(state=0).count()
    pnr_1 = Pnr.objects.filter(state=1).count()
    pnr_2 = Pnr.objects.filter(state=2).count()
    pnr_emis = Pnr.objects.filter(status='Emis').count()
    pnr_Non_émis = Pnr.objects.filter(status='Non émis').count()
    context['pnr_0'] = pnr_0
    context['pnr_1'] = pnr_1
    context['pnr_2'] = pnr_2
    context['pnr_emis'] = pnr_emis
    context['pnr_Non_émis'] = pnr_Non_émis
    return render(request,'dashboard.html', context) 