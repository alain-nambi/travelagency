'''
Created on 8 Sep 2022

'''
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.models.user.Users import Role
from AmadeusDecoder.forms import UserForm
@login_required(login_url='index')
def users(request):
    context = {}
    context['users'] = User.objects.all()
    context['roles'] = Role.objects.all()
    
    object_list = context['users']
    row_num = request.GET.get('paginate_by', 25) or 25
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, row_num)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger: 
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {'page_obj': page_obj, 'row_num': row_num}
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

@login_required(login_url='index')
def user_details(request,user_id):
    context={}
    user = User.objects.get(pk=user_id)
    roles = Role.objects.all()

    context['user'] = user
    context['roles'] = roles
    return render(request,'user-details.html',context)

@login_required(login_url='index')
def archive_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        connected_user_id = request.get('connected_user')
        password = request.POST.get('password')

        connected_user = User.objects.get(pk= connected_user_id)
        if connected_user.