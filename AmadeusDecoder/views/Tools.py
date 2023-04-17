'''
Created on 8 Sep 2022

'''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='index')
def tools(request):  
    return render(request,'tools.html')    