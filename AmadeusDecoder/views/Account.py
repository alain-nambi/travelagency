
'''
Created on 8 Sep 2022

'''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from AmadeusDecoder.models.user.Users import User

@login_required(login_url='index')
def account(request):  
    context = {}
    return render(request,'account.html', context) 