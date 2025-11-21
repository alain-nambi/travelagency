'''
Created on 8 Sep 2022

'''
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timezone
from AmadeusDecoder.models.invoice.Ticket import Ticket

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

    pnr_not_invoiced = get_ticket_created_today_not_invoiced(request)
    context['pnr_not_invoiced'] = pnr_not_invoiced
    context['notif_number'] = len(pnr_not_invoiced)
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

# ------- Notification ---------------------------------
def get_ticket_created_today_not_invoiced(request):
    # get number of ticket not invoiced today
    today = datetime.now().date()

    start_date = datetime(today.year, today.month, today.day, 0, 0, 0, tzinfo=timezone.utc)
    end_date = datetime(today.year, today.month, today.day, 23, 59, 59, tzinfo=timezone.utc)
    
    print('REQUEST USER : ',request.user.id)
    current_user = User.objects.get(id= request.user.id)
    print('CURRENT USER : ',current_user)
    if current_user.role_id == 1:
        tickets = Ticket.objects.filter(pnr_id__system_creation_date__range=[start_date, end_date], is_invoiced= False, fare=0, ticket_status=1, state=0)
    else:
        tickets = Ticket.objects.filter(pnr__agent_id = current_user.id,pnr_id__system_creation_date__range=[start_date, end_date], is_invoiced= False, fare=0, ticket_status=1, state=0)
    
    print('PNRS : ',tickets)
    nbre_pnr = tickets.count()
    print('------------- NOTIF NUMBER----------------- : ',nbre_pnr)

    return tickets
