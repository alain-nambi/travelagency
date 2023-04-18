'''
Created on 8 Sep 2022

'''
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.models.user.Users import Role
from AmadeusDecoder.forms import UserForm
@login_required(login_url='index')
def users(request):
    context = {}
    context['users'] = User.objects.all()
    context['roles'] = Role.objects.all()
    return render(request,'manage_users.html', context)


@login_required(login_url='index')
def register(request):
    context = {}
    form = UserForm()

    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
        context['form'] = form
        return redirect('users')
    else:
        context['form'] = form

    context['users'] = User.objects.all()
    
    return render(request,'add-user.html', context)


