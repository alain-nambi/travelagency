
'''
Created on 8 Sep 2022

'''
from AmadeusDecoder.models.user.Users import User

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,'login.html')

def loginPage(request):
    email = None
    password = None
    user = None
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password incorrect')
            return redirect('index')
    

def logoutUser(request):
    logout(request)
    return redirect('index')