'''
Created on 8 Sep 2022

'''
import csv
import os
import json
import secrets 
from datetime import datetime, timezone
import requests
import random
import pandas as pd

import AmadeusDecoder.utilities.configuration_data as configs

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms.models import model_to_dict

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.pnr.PnrPassenger import PnrPassenger
from AmadeusDecoder.models.user.Users import User, UserCopying
from AmadeusDecoder.models.invoice.Clients import Client
from AmadeusDecoder.models.utilities.Comments import Comment, Response
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.Fee import Fee, ReducePnrFeeRequest, OthersFee
from AmadeusDecoder.models.invoice.Invoice import Invoice
from AmadeusDecoder.models.invoice.InvoiceDetails import InvoiceDetails
from AmadeusDecoder.models.pnr.Passenger import Passenger
from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
from AmadeusDecoder.models.invoice.Fee import Product
from AmadeusDecoder.models.pnrelements.PnrAirSegments import PnrAirSegments
from AmadeusDecoder.models.history.History import History
from AmadeusDecoder.models.configuration.Configuration import Configuration

from AmadeusDecoder.utilities.FtpConnection import upload_file
from AmadeusDecoder.utilities.SendMail import Sending
from AmadeusDecoder.utilities.ServiceFeesDecreaseRequest import ServiceFeesDecreaseRequest
import traceback

@login_required(login_url='index')
def home(request): 
    context = {}

    users = User.objects.exclude(username__in=('Moïse ISSOUFALI', 'Paul ISSOUFALI')).exclude(role=1).order_by('username')
    
    try:
        if request.COOKIES.get('filter_pnr') == "True":
            is_invoiced = True
        if request.COOKIES.get('filter_pnr') == "False":
            is_invoiced = False
        if request.COOKIES.get('filter_pnr') == "None":
            is_invoiced = None
        if request.COOKIES.get('filter_pnr') is None:
            is_invoiced = False
    except:
        is_invoiced = False
        
    # Récupère la valeur de l'objet cookie nommé "dateRangeFilter"
    date_range_filter = request.COOKIES.get('dateRangeFilter')

    # Initialise les variables start_date et end_date à None
    start_date, end_date = None, None

    # Vérifie si date_range_filter contient une valeur non nulle ou non vide
    if date_range_filter:

        # Itère sur une liste des formats de date possibles pour la conversion
        for format in ("%d-%m-%Y", "%Y-%m-%d"):

            try:
                # Convertit les deux dates start_date et end_date à partir de la chaîne de date dans date_range_filter
                start_date, end_date = [datetime.strptime(d, format) for d in date_range_filter.split(" * ")]

                # Rend les deux dates timezone-aware en utilisant le fuseau horaire UTC
                start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0, tzinfo=timezone.utc)
                end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59, tzinfo=timezone.utc)

                # Sort de la boucle for si la conversion réussit
                break
                
            except ValueError:
                # Passe à l'essai suivant si la conversion échoue
                pass

    # print("Date de début:", start_date)
    # print("Date de fin:", end_date)

    try:
        status_value_from_cookie = int(request.COOKIES.get('filter_pnr_by_status'))
    except:
        status_value_from_cookie = 0

    creation_date_order_by = request.COOKIES.get('creation_date_order_by')
    # desc : date order by descending
    # asc : date order by ascending
    try:
        if creation_date_order_by == "desc":
            date_order_by = "-"
        elif creation_date_order_by == "asc":
            date_order_by = ""
        else:
            date_order_by = "-"
    except:
        date_order_by = "-"
    # Set max timezone
    maximum_timezone = "2023-01-01 01:00:00.000000+03:00"
    
    filtered_creator = request.COOKIES.get('creator_pnr_filter')
    print("Creator: " + str(filtered_creator))
    print(type(filtered_creator))

    # Retrieve the value of the "isSortedByCreator" cookie from the request
    is_sorter_by_creator = request.COOKIES.get('isSortedByCreator')

    # Initialize the sort_creator variable to a default value
    # Set order_by username ascendant
    sort_creator = None

    # Determine the value of "sort_creator" based on the value of the cookie
    if is_sorter_by_creator is not None:
        sort_creator = is_sorter_by_creator

    # print(sort_creator)
    
    if request.user.id in [4, 5]: #==> [Farida et Mouniati peuvent voir chacun l'ensemble de leurs pnr]
        pnr_list = []
        pnr_count = 0
        issuing_users = request.user.copied_documents.all()

        # Create date filter query object or an empty query object if dates are absent
        date_filter = Q(system_creation_date__range=[start_date, end_date]) if start_date and end_date else Q()
        max_system_creation_date = Q(system_creation_date__gt=maximum_timezone)
        status_value = Q(status_value=status_value_from_cookie) if status_value_from_cookie in [0, 1] else Q()
        
        if is_invoiced is None:
            for issuing_user in issuing_users:
                pnr =   Pnr.objects.filter(
                            number=issuing_user.document, 
                        ).filter(
                            status_value,
                            date_filter,
                            max_system_creation_date,
                        ).first()
                    
                if pnr not in pnr_list and pnr is not None:
                    pnr_list.append(pnr)

            agent = Q()
            if filtered_creator is not None:
                agent = Q(agent_id=filtered_creator)
            else:
                agent = Q(agent_id=4) | Q(agent_id=5)

            pnr_obj =   Pnr.objects.filter(
                            status_value,
                        ).filter(
                            date_filter,
                            agent,
                            max_system_creation_date,
                        ).order_by(date_order_by + 'system_creation_date')
                    
            for pnr in pnr_obj:
                if pnr not in pnr_list:
                    pnr_list.append(pnr)

            # Sort the list based on the agent username or system creation date
            if sort_creator is not None:
                if sort_creator == 'agent__username':
                    # Sort Pnrs by agent's username and agent_id None in the last part of list
                    pnr_list = sorted(
                        pnr_list, 
                        key=lambda pnr: (
                            pnr.agent is None, 
                            pnr.agent.username if pnr.agent else ''
                        ), 
                        reverse=False
                    )
                elif sort_creator == '-agent__username':
                    # Sort Pnrs by agent's username in reverse order and agent_id None in the last part of list
                    pnr_list = sorted(
                        pnr_list, 
                        key=lambda pnr: (
                            pnr.agent.username if pnr.agent else ''
                        ), 
                        reverse=True
                    )
            else:
                # If no sorting parameter provided, sort by system creation date
                if date_order_by == "-":
                    # Sort Pnrs by system creation date in reverse order
                    pnr_list = sorted(pnr_list, key=lambda pnr: pnr.system_creation_date, reverse=True)
                else:
                    # Sort Pnrs by system creation date in ascending order
                    pnr_list = sorted(pnr_list, key=lambda pnr: pnr.system_creation_date, reverse=False)

            pnr_count = len(pnr_list)
        else:
            for issuing_user in issuing_users:
                pnr   = Pnr.objects.filter(
                            number=issuing_user.document,
                        ).filter(
                            status_value,
                            date_filter,
                            max_system_creation_date,
                        ).filter(is_invoiced=is_invoiced).first()
                
                if pnr not in pnr_list and pnr is not None:
                    pnr_list.append(pnr)

            agent = Q()
            if filtered_creator is not None:
                agent = Q(agent_id=filtered_creator)
            else:
                agent = Q(agent_id=4) | Q(agent_id=5)

            pnr_obj   = Pnr.objects.filter(
                            status_value,
                        ).filter( 
                            date_filter,
                            agent,
                            max_system_creation_date,
                        ).filter(is_invoiced=is_invoiced).order_by(date_order_by + 'system_creation_date')
            
            for pnr in pnr_obj:
                if pnr not in pnr_list:
                    pnr_list.append(pnr)

            # Sort the list based on the agent username or system creation date
            if sort_creator is not None:
                if sort_creator == 'agent__username':
                    # Sort Pnrs by agent's username and agent_id None in the last part of list
                    pnr_list = sorted(
                        pnr_list, 
                        key=lambda pnr: (
                            pnr.agent is None, 
                            pnr.agent.username if pnr.agent else ''
                        ), 
                        reverse=False
                    )
                elif sort_creator == '-agent__username':
                    # Sort Pnrs by agent's username in reverse order and agent_id None in the last part of list
                    pnr_list = sorted(
                        pnr_list, 
                        key=lambda pnr: (
                            pnr.agent.username if pnr.agent else ''
                        ), 
                        reverse=True
                    )
            else:
                # If no sorting parameter provided, sort by system creation date
                if date_order_by == "-":
                    # Sort Pnrs by system creation date in reverse order
                    pnr_list = sorted(pnr_list, key=lambda pnr: pnr.system_creation_date, reverse=True)
                else:
                    # Sort Pnrs by system creation date in ascending order
                    pnr_list = sorted(pnr_list, key=lambda pnr: pnr.system_creation_date, reverse=False)

            pnr_count = len(pnr_list)
            
            print("PNR COUNT")
            print(pnr_count)
        
        context['pnr_list'] = pnr_list
        object_list = context['pnr_list']
        context['pnr_count'] = pnr_count
        row_num = request.GET.get('paginate_by', 50) or 50
        page_num = request.GET.get('page', 1)
        paginator = Paginator(object_list, row_num)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context = {'page_obj': page_obj, 'row_num': row_num}
        context['users'] = users
        return render(request,'home.html', context)

    if request.user.role_id == 3:
        pnr_list = []
        pnr_count = 0
        issuing_users = request.user.copied_documents.all()

        status_value = Q(status_value=status_value_from_cookie) if status_value_from_cookie in [0, 1] else Q()
        is_invoiced = Q(is_invoiced=is_invoiced) if is_invoiced is not None else Q(is_invoiced=False)

        for issuing_user in issuing_users:                
            # Create date filter query object or an empty query object if dates are absent
            date_filter = Q(system_creation_date__range=[start_date, end_date]) if start_date and end_date else Q()
            max_system_creation_date = Q(system_creation_date__gt=maximum_timezone)

            # Get the Pnr object matching criteria in the query
            pnr =   Pnr.objects.filter(
                        number=issuing_user.document, 
                    ).filter(
                        is_invoiced,
                        status_value,
                        date_filter,
                        max_system_creation_date
                    ).first()

            # If Pnr is not already in the set and is not None, add it to the set and the list
            if pnr not in pnr_list and pnr is not None:
                pnr_list.append(pnr)

        print(f"PNR list without issuing users: {len(pnr_list)}")

        # Create date filter query object or an empty query object if dates are absent
        date_filter = Q(system_creation_date__range=[start_date, end_date]) if start_date and end_date else Q()

        agent = Q()
        if filtered_creator is not None:
            agent = Q(agent_id=filtered_creator)
        else:
            agent = Q(agent_id=request.user.id) | Q(agent_id=None)

        max_system_creation_date = Q(system_creation_date__gt=maximum_timezone)
        
        # Get the Pnr objects matching criteria in the query, filtered by agent and date constraints
        pnr_obj =   Pnr.objects.filter(
                        date_filter,
                        agent,
                        max_system_creation_date,
                        status_value,
                    ).filter(
                        is_invoiced,
                    ).order_by(
                        date_order_by + 'system_creation_date'
                    )

        # Get all PNRs that are not in the list
        for pnr in pnr_obj:
            if pnr not in pnr_list:
                pnr_list.append(pnr)

        print(f"PNR list with issuing users: {len(pnr_list)}")

        # Sort the list based on the agent username or system creation date
        if sort_creator is not None:
            if sort_creator == 'agent__username':
                # Sort Pnrs by agent's username and agent_id None in the last part of list
                pnr_list = sorted(
                    pnr_list, 
                    key=lambda pnr: (
                        pnr.agent is None, 
                        pnr.agent.username if pnr.agent else ''
                    ), 
                    reverse=False
                )
            elif sort_creator == '-agent__username':
                # Sort Pnrs by agent's username in reverse order and agent_id None in the last part of list
                pnr_list = sorted(
                    pnr_list, 
                    key=lambda pnr: (
                        pnr.agent.username if pnr.agent else ''
                    ), 
                    reverse=True
                )
        else:
            # If no sorting parameter provided, sort by system creation date
            if date_order_by == "-":
                # Sort Pnrs by system creation date in reverse order
                pnr_list = sorted(pnr_list, key=lambda pnr: pnr.system_creation_date, reverse=True)
            else:
                # Sort Pnrs by system creation date in ascending order
                pnr_list = sorted(pnr_list, key=lambda pnr: pnr.system_creation_date, reverse=False)
        
        # Compute count of Pnrs in the list
        pnr_count = len(pnr_list)


        context['pnr_list'] = pnr_list
        object_list = context['pnr_list']
        context['pnr_count'] = pnr_count
        row_num = request.GET.get('paginate_by', 50) or 50
        page_num = request.GET.get('page', 1)
        paginator = Paginator(object_list, row_num)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context = {'page_obj': page_obj, 'row_num': row_num}
        context['users'] = users
        return render(request,'home.html', context)
    else:
        status_value = Q(status_value=status_value_from_cookie) if status_value_from_cookie in [0, 1] else Q()

        if filtered_creator != '0' and filtered_creator is not None: 
            max_system_creation_date = Q(system_creation_date__gt=maximum_timezone)

            # Create date filter query object or an empty query object if dates are absent
            date_filter = Q(system_creation_date__range=[start_date, end_date]) if start_date and end_date else Q()

            pnr_queryset  = Pnr.objects.filter(
                                agent_id=filtered_creator
                            ).filter(
                                status_value,
                                max_system_creation_date,
                                date_filter,
                            )

            if is_invoiced is not None:
                pnr_queryset =  pnr_queryset.filter(Q(is_invoiced=is_invoiced))

            # Sort the list based on the agent username or system creation date
            if sort_creator is not None:
                if sort_creator == 'agent__username':
                    # Sort Pnrs by agent's username and agent_id None in the last part of list
                    pnr_list = sorted(
                        pnr_queryset, 
                        key=lambda pnr: (
                            pnr.agent is None, 
                            pnr.agent.username if pnr.agent else ''
                        ), 
                        reverse=False
                    )
                elif sort_creator == '-agent__username':
                    # Sort Pnrs by agent's username in reverse order and agent_id None in the last part of list
                    pnr_list = sorted(
                        pnr_queryset, 
                        key=lambda pnr: (
                            pnr.agent.username if pnr.agent else ''
                        ), 
                        reverse=True
                    )
            else:
                # If no sorting parameter provided, sort by system creation date
                if date_order_by == "-":
                    # Sort Pnrs by system creation date in reverse order
                    pnr_list = sorted(pnr_queryset, key=lambda pnr: pnr.system_creation_date, reverse=True)
                else:
                    # Sort Pnrs by system creation date in ascending order
                    pnr_list = sorted(pnr_queryset, key=lambda pnr: pnr.system_creation_date, reverse=False)

            pnr_list = list(pnr_list)
            pnr_count = pnr_queryset.count()

            print('Not all')
        elif filtered_creator == '0' or filtered_creator is None: ##### Si 'Tout' est sélectionner dans le filtre créateur
            max_system_creation_date = Q(system_creation_date__gt=maximum_timezone)

            # Create date filter query object or an empty query object if dates are absent
            date_filter = Q(system_creation_date__range=[start_date, end_date]) if start_date and end_date else Q()
        
            pnr_queryset =  Pnr.objects.filter(
                                status_value,
                            ).filter(
                                max_system_creation_date,
                                date_filter,
                            )

            if is_invoiced is not None:
                pnr_queryset =  pnr_queryset.filter(Q(is_invoiced=is_invoiced))

            # Sort the list based on the agent username or system creation date
            if sort_creator is not None:
                if sort_creator == 'agent__username':
                    # Sort Pnrs by agent's username and agent_id None in the last part of list
                    pnr_list = sorted(
                        pnr_queryset, 
                        key=lambda pnr: (
                            pnr.agent is None, 
                            pnr.agent.username if pnr.agent else ''
                        ), 
                        reverse=False
                    )
                elif sort_creator == '-agent__username':
                    # Sort Pnrs by agent's username in reverse order and agent_id None in the last part of list
                    pnr_list = sorted(
                        pnr_queryset, 
                        key=lambda pnr: (
                            pnr.agent.username if pnr.agent else ''
                        ), 
                        reverse=True
                    )
            else:
                # If no sorting parameter provided, sort by system creation date
                if date_order_by == "-":
                    # Sort Pnrs by system creation date in reverse order
                    pnr_list = sorted(pnr_queryset, key=lambda pnr: pnr.system_creation_date, reverse=True)
                else:
                    # Sort Pnrs by system creation date in ascending order
                    pnr_list = sorted(pnr_queryset, key=lambda pnr: pnr.system_creation_date, reverse=False)

            pnr_list = list(pnr_list)
            pnr_count = pnr_queryset.count()

            print('All')

        context['pnr_list'] = pnr_list
        context['pnr_count'] = pnr_count
        object_list = context['pnr_list']
        row_num = request.GET.get('paginate_by', 50) or 50
        page_num = request.GET.get('page', 1)
        paginator = Paginator(object_list, row_num)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger: 
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context = {'page_obj': page_obj, 'row_num': row_num}
        context['users'] = users
        return render(request,'home.html', context)

@login_required(login_url='index')
def pnr_details(request, pnr_id):
    context = {}
    if pnr_id is not None and pnr_id != '':
        pnr_detail = Pnr.objects.get(pk=pnr_id)
    print("55555") 
    print(pnr_id)
    print(pnr_detail.id)
    pnr_detail.update_read_status()
    context['pnr'] = pnr_detail
    context['passengers'] = pnr_detail.passengers.filter(passenger__passenger_status=1).all().order_by('id')
    context['contacts'] = pnr_detail.contacts.all()
    context['air_segments'] = pnr_detail.segments.filter(segment_type='Flight', air_segment_status=1).all().order_by('segmentorder')
    context['tickets'] = pnr_detail.tickets.filter(ticket_status=1).filter(Q(total__gt=0) | Q(is_no_adc=True) | (Q(is_refund=True) & Q(total__lt=0))).all().order_by('passenger_id')
    # context['tickets'] = pnr_detail.tickets.filter().all()
    context['other_fees'] = pnr_detail.others_fees.filter(other_fee_status=1, ticket=None).all()
    context['clients'] = Client.objects.all().order_by('intitule')
    context['users'] = User.objects.all()
    context['comments'] = Comment.objects.filter(pnr_id=pnr_id)
    context['responses'] = Response.objects.filter(pnr_id=pnr_id)
    context['products'] = Product.objects.all()
    context['raw_data'] = pnr_detail.pnr_data.all().order_by('-data_datetime')

    # PNR not invoiced 
    if pnr_detail.status_value == 0:
        __ticket_base = pnr_detail.tickets.filter(ticket_status=1).exclude(Q(total=0))
        __other_fee_base = pnr_detail.others_fees.filter(other_fee_status=1).exclude(~Q(ticket=None), ~Q(other_fee=None), total=0)
        __ticket_no_adc_base = pnr_detail.tickets.filter(ticket_status=1, total=0, is_no_adc=True)

        __cancellation = pnr_detail.others_fees.filter(Q(other_fee__in=__other_fee_base)|Q(ticket__in=__ticket_base) | Q(ticket__in=__ticket_no_adc_base))

        print('__________Cancellation____________')
        if __cancellation.exists():
            for cancellation in __cancellation:
                if cancellation.other_fee is not None:
                    cancellation.other_fee.is_invoiced = True
                    cancellation.other_fee.save()
                if cancellation.ticket is not None:
                    cancellation.ticket.is_invoiced = True
                    cancellation.ticket.save()
                cancellation.is_invoiced = True
                cancellation.save()

        if not __ticket_base.exists() and not __other_fee_base.exists() and not __ticket_no_adc_base.exists():
            pnr_detail.is_invoiced = False
            pnr_detail.save()
        elif __ticket_base.exists() and not __other_fee_base.exists() and not __ticket_no_adc_base.exists():
            print('Only ticket')
            __ticket_not_ordered = __ticket_base.filter(is_invoiced=False)
            if __ticket_not_ordered.exists():
                pnr_detail.is_invoiced = False
                pnr_detail.save()
            else:
                pnr_detail.is_invoiced = True
                pnr_detail.save()
        elif not __ticket_base.exists() and __other_fee_base.exists() and not __ticket_no_adc_base.exists():
            print('Only other fee')
            print(__other_fee_base)
            __other_fee_not_ordered = __other_fee_base.filter(is_invoiced=False)
            if __other_fee_not_ordered.exists():
                pnr_detail.is_invoiced = False
                pnr_detail.save()
            elif not __other_fee_not_ordered.exists():
                pnr_detail.is_invoiced = True
                pnr_detail.save()
        elif not __ticket_base.exists() and not __other_fee_base.exists() and __ticket_no_adc_base.exists():
            print('Only ticket no adc')
            __ticket_no_adc_not_ordered = __ticket_no_adc_base.filter(is_invoiced=False)
            if __ticket_no_adc_not_ordered.exists():
                pnr_detail.is_invoiced = False
                pnr_detail.save()
            else:
                pnr_detail.is_invoiced = True
                pnr_detail.save()
        else:
            print('All of them')
            __ticket_not_ordered = __ticket_base.filter(is_invoiced=False)
            __other_fee_not_ordered = __other_fee_base.filter(is_invoiced=False)
            __ticket_no_adc_not_ordered = __ticket_no_adc_base.filter(is_invoiced=False)
            if __ticket_not_ordered.exists() or __other_fee_not_ordered.exists() or __ticket_no_adc_not_ordered.exists():
                pnr_detail.is_invoiced = False
                pnr_detail.save()
            elif not __ticket_not_ordered.exists() and not __other_fee_not_ordered.exists() and not __ticket_no_adc_not_ordered.exists():
                pnr_detail.is_invoiced = True
                pnr_detail.save()

    return render(request,'pnr-details.html', context)

@login_required(login_url='index')
def get_pnr_user_copying(request):
    if request.method == 'POST':
        user_id = User.objects.get(pk=int(request.user.id))
        if 'DocumentNumber' in request.POST:
            document_number = request.POST['DocumentNumber']
            new_user = UserCopying(document=document_number, user_id=user_id)
            new_user.save()
    context = {}
    return JsonResponse(context)

@login_required(login_url='index')
def pnr_research(request):
    context = {}
    if request.method == 'POST' and request.POST.get('pnr_research'):
        maximum_timezone = "2023-01-01 01:00:00.000000+03:00"

        search_results = []
        
        pnr_research = request.POST.get('pnr_research')
        pnr_results = Pnr.objects.all().filter(Q(number__icontains=pnr_research)).filter(Q(system_creation_date__gt=maximum_timezone))
        for p1 in pnr_results :
            search_results.append(p1)
        # search with passenger
        _passengers = Passenger.objects.all().filter(Q(name__icontains=pnr_research) | Q(surname__icontains=pnr_research) )
        _passengers_results = []
        for p in _passengers :
            # print(p)
            
            pnr_passenger = PnrPassenger.objects.all().filter(passenger=p).first()
            if pnr_passenger is not None :
                pnr_object = Pnr.objects.all().filter(pk=pnr_passenger.pnr.pk).filter(Q(system_creation_date__gt=maximum_timezone)).first()
                # pnr_results |= res
                if pnr_object not in search_results and pnr_object is not None :
                    search_results.append(pnr_object)

        # Search with customer
        _customers = Client.objects.all().filter(Q(intitule__icontains=pnr_research) )
        customer_results = []
        for c in _customers :
            pnr_passenger_invoice = PassengerInvoice.objects.all().filter(client=c).first()
            if pnr_passenger_invoice is not None :
                pnr_cobject = Pnr.objects.all().filter(pk=pnr_passenger_invoice.pnr.pk).filter(Q(system_creation_date__gt=maximum_timezone)).first()
                # pnr_results |= res
                if pnr_cobject not in search_results and pnr_cobject is not None :
                    search_results.append(pnr_cobject)

        # for pnr in pnr_results :
        #     passenger = Passenger.objects.filter(passenger__pnr=pnr).first()
        #     pnr['first_passenger'] = passenger
        results = []
        for pnr in search_results:
            passenger_name = None
            passenger_surname = None
            values = {}
            values['id'] = pnr.id
            values['number'] = pnr.number
            first_passenger = pnr.passengers.first()
            if first_passenger is not None :
                passenger_name = first_passenger.passenger.name.upper() if first_passenger.passenger.name is not None else ''
                passenger_surname = first_passenger.passenger.surname.capitalize() if first_passenger.passenger.surname is not None else ''

            values['passenger_name'] = passenger_name
            values['passenger_surname'] = passenger_surname
            values['state'] = pnr.state
            values['system_creation_date'] = pnr.system_creation_date.strftime('%d/%m/%Y %H:%M')
            values['ticket_issuing_date'] = pnr.get_max_issuing_date() if pnr.get_max_issuing_date() is not None else ''
            values['total'] = '%.2f' % pnr.invoice.detail.total
            values['status'] = pnr.status
            values['opc'] = pnr.get_min_opc().strftime('%d/%m/%Y %H:%M') if pnr.get_min_opc() is not None else ''
            values['type'] = 'Zenith' if pnr.type == 'EWA' else pnr.type
            values['agent'] = pnr.agent.username if pnr.agent is not None else pnr.agent_code if pnr.agent_code is not None else ''
            values['pnr_emitter'] = pnr.get_emit_agent().username if pnr.get_emit_agent() is not None and pnr.status_value == 0 else ''
            values['agency'] = '%s: %s' % (pnr.agency.name, pnr.agency.code) if pnr.agency is not None else pnr.agency_name if pnr.type == 'EWA' else ''
            values['is_read'] = pnr.is_read
            values['status_value'] = pnr.status_value
            values['is_invoiced'] = pnr.is_invoiced
            
            if pnr.status == 'Non émis':
                # Add customer name to data result search
                if pnr.customer is not None:
                    values['customer'] = pnr.customer.intitule
            else:
                passenger_invoice_obj = PassengerInvoice.objects.filter(pnr_id=pnr.id)
                if passenger_invoice_obj.exists():            
                    for passenger_invoice in passenger_invoice_obj:
                        client_obj = Client.objects.filter(id=passenger_invoice.client_id)
                            
                    if client_obj.exists():
                        for client in client_obj:
                            values['customer'] = client.intitule

            results.append(values)
            


        # result_serialized = serializers.serialize('json', results)
        
        context['pnr_result'] = results
    
    return JsonResponse(context)

@login_required(login_url='index')
def pnr_search_by_pnr_number(request):
    context = {}
    if request.method == 'POST':
        pnr_number = request.POST.get('PnrNumber', None)
        if pnr_number is not None:
            pnr = Pnr.objects.all().filter(number=pnr_number).first()
            if pnr is not None:
                context['pnr_id'] = pnr.id
            else:
                context['pnr_id'] = []
        else:
            context['pnr_id'] = []
    return JsonResponse(context)

# @login_required(login_url='index')
def reduce_fee_request_accepted(request, request_id, amount, choice_type, token):  
    context = {}

    request_obj = ReducePnrFeeRequest.objects.get(pk=request_id, token=token)
    original_status = request_obj.status
    
    if request_obj and request_obj.status in (0, 3) :
        # update fee amount
        fee_obj = Fee.objects.get(pk=request_obj.fee.id)
        fee_amount = amount if amount is not None else request_obj.amount
        if choice_type == 'one':
            fee_obj.cost = fee_amount
            fee_obj.total = fee_amount
            fee_obj.save()
        elif choice_type == 'all':
            all_ticket_related_fees = Fee.objects.filter(pnr__id=fee_obj.pnr.id).all()
            for temp_related_ticket in all_ticket_related_fees:
                temp_related_ticket.cost = fee_amount
                temp_related_ticket.total = fee_amount
                temp_related_ticket.save()

        request_obj.status = 1 
        request_obj.save()

        context['request_status'] = 1
        context['message'] = "Demande de réduction acceptée."
        
        # send response
        service_fees_decrease_request_obj = ServiceFeesDecreaseRequest()
        # accepted
        if original_status == 0:
            service_fees_decrease_request_obj.send_decrease_request_response(request_obj, fee_amount, 1, choice_type)
        # modified
        elif original_status == 3:
            service_fees_decrease_request_obj.send_decrease_request_response(request_obj, fee_amount, 2, choice_type)
    else : 
        context['request_status'] = 0
        context['message'] = "Le lien a été expiré."

    return render(request,'validate-request.html', context) 

# @login_required(login_url='index')
def reduce_fee_request_rejected(request, request_id, choice_type, token):  
    context = {}

    request_obj = ReducePnrFeeRequest.objects.get(pk=request_id, token=token)

    if request_obj and request_obj.status in (0, 3) :
        request_obj.status = 2
        request_obj.save()

        context['request_status'] = 2
        context['message'] = "Demande de réduction refusée."
        
        # send response
        ServiceFeesDecreaseRequest().send_decrease_request_response(request_obj, 0, 0, choice_type)
    else :
        context['request_status'] = 0
        context['message'] = "Le lien a été expiré."

    return render(request,'validate-request.html', context) 

# @login_required(login_url='index')
def reduce_fee_request_modify(request, request_id, choice_type, token):  
    context = {}

    request_obj = ReducePnrFeeRequest.objects.get(pk=request_id, token=token)

    if request_obj and request_obj.status in (0, 3) :

        request_obj.status = 3 
        request_obj.save()

        context['request_status'] = 3
        context['request'] = request_obj
        context['choice_type'] = choice_type
        # Url token
        # UrlAccepted = request.build_absolute_uri(reverse('reduce_fee_request_accepted', args=(request_obj.id,str(feeAmount),token,)))
        UrlRejected = request.build_absolute_uri(reverse('reduce_fee_request_rejected', args=(request_obj.id,choice_type,token)))

        # context['UrlAccepted'] = UrlAccepted
        context['UrlRejected'] = UrlRejected
    else :
        context['request_status'] = 0
        context['message'] = "Le lien a été expiré."

    return render(request,'validate-request.html', context) 

@login_required(login_url='index')
def reduce_fee(request) :
    context = {}
    if request.method == 'POST' and request.POST.get('pnrId') and request.POST.get('feeId'):
        pnrId = request.POST.get('pnrId')
        feeId = request.POST.get('feeId')
        feeAmount = request.POST.get('feeAmount')
        feeOriginAmount = request.POST.get('feeOriginAmount')
        choiceType = request.POST.get('choiceType')
        motif = request.POST.get('motif')
        
        try :
            subject, message = ServiceFeesDecreaseRequest().inquiry_formatting(choiceType, request, feeId, pnrId, feeOriginAmount, feeAmount, motif)
            
            context['status'] = 1 
            context['message'] = "Demande envoyée avec succès."
            
            Sending.send_email_request(
                configs.FEE_REQUEST_SENDER['address'],
                configs.FEE_REQUEST_RECIPIENT,
                subject,
                message
            )
        except Exception as e :
            raise e
            context['status'] = 0
            context['message'] = "ERREUR: %s " % str(e)

    else :
        context['status'] = 0
        context['message'] = "ERREUR: Impossible d'envoyer la demande."
    
    return JsonResponse(context)

@login_required(login_url='index')
def save_pnr_detail_modification(request, pnr_id):
    context = {}
    if request.method == 'POST':
        if 'pnrId' and 'refCde' and 'ticketIdsChecked' and 'customerId' in request.POST:
            ticket_checked = json.loads(request.POST.get('ticketIdsChecked'))
            customer_id = request.POST.get('customerId')
            pnr_id = request.POST.get('pnrId')
            reference = request.POST.get('refCde')
            pnr = Pnr.objects.get(pk=int(pnr_id))
            user = User.objects.get(pk=int(request.user.id))
            if ticket_checked != [] and ticket_checked != '' and customer_id != '':
                customer = Client.objects.get(pk=int(customer_id))
                orders = PassengerInvoice.objects.filter(pnr=pnr)
                print(ticket_checked)


                if pnr.status_value == 0:
                    print('Entry issuing part')
                    if orders.filter(status='sale').exists():
                        print('Enty to issuing first part with : ' + str(ticket_checked))
                        count = 0
                        passenger_invoice = orders.filter(status='sale')
                        for ids in ticket_checked:
                            tickets = Ticket.objects.filter(pk=int(ids), pnr=pnr_id, ticket_status=1).exclude(ticket_type='TST')
                            for ticket in tickets:
                                if not passenger_invoice.filter(ticket=ticket.id).exists():
                                    invoice_tickets_passenger = PassengerInvoice(
                                        ticket=ticket, pnr=pnr, type=ticket.ticket_type, client=customer, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, fee=None, status='sale')
                                    invoice_tickets_passenger.save()


                                    fee_objects = Fee.objects.filter(ticket=ticket.id)
                                    if fee_objects.exists():
                                        for fee_item in fee_objects:
                                            invoice_fee_passenger = PassengerInvoice.objects.filter(fee=fee_item.id, pnr=int(pnr_id))
                                            if not invoice_fee_passenger.exists():
                                                invoice_fee_passenger = PassengerInvoice(
                                                    fee=fee_item, pnr=pnr, client=customer, type=fee_item.type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, status='sale')
                                                invoice_fee_passenger.save()

                    elif not orders.filter(status='sale').exists():
                        print('Enty to issuing second part with : ' + str(ticket_checked))
                        passenger_invoice = orders.filter(status='sale')
                        for ids in ticket_checked:
                            tickets = Ticket.objects.filter(pk=int(ids), pnr=int(pnr_id), ticket_status=1).exclude(ticket_type='TST')
                            for ticket in tickets:
                                if not passenger_invoice.filter(ticket=ticket.id).exists():
                                    invoice_tickets_passenger = PassengerInvoice(
                                        ticket=ticket, pnr=pnr, type=ticket.ticket_type, client=customer, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, fee=None, status='sale', other_fee=None)
                                    invoice_tickets_passenger.save()

                                    fee_objects = Fee.objects.filter(ticket=ticket.id)
                                    if fee_objects.exists():
                                        for fee_item in fee_objects:
                                            invoice_fee_passenger = PassengerInvoice.objects.filter(fee=fee_item.id, pnr=int(pnr_id))
                                            if not invoice_fee_passenger.exists():
                                                invoice_fee_passenger = PassengerInvoice(
                                                    fee=fee_item, pnr=pnr, client=customer, type=fee_item.type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, status='sale', other_fee=None)
                                                invoice_fee_passenger.save()

                elif pnr.status_value == 1:
                    count = 0
                    print('Enty to unissuing first part with : ' + str(ticket_checked))
                    ticket_objects = Ticket.objects.filter(pk__in=ticket_checked, pnr=int(pnr_id), ticket_status=1).exclude(ticket_type__in=['TKT', 'EMD'])
                    print('Unissuing ticket: ' + str(ticket_objects.count()))
                    if ticket_objects.exists():
                        for ticket_object in ticket_objects:
                            count+=1
                            print('Count : ' + str(count))
                            invoice_tickets_passenger = PassengerInvoice.objects.filter(ticket=ticket_object.id, pnr=int(pnr_id))
                            if not invoice_tickets_passenger.exists():
                                invoice_tickets_passenger = PassengerInvoice(ticket=ticket_object, pnr=pnr, type=ticket_object.ticket_type, client=customer, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, fee=None, status='quotation', other_fee=None)
                                invoice_tickets_passenger.save()
                                print('ticket unissued saved')

                            fee_objects = Fee.objects.filter(ticket=int(ticket_object.id))
                            if fee_objects.exists():
                                for fee_item in fee_objects:
                                    invoice_fee_passenger = PassengerInvoice.objects.filter(fee=fee_item.id, pnr=int(pnr_id))
                                    if not invoice_fee_passenger.exists():
                                        invoice_fee_passenger = PassengerInvoice(fee=fee_item, pnr=pnr, client=customer, type=fee_item.type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, status='quotation', other_fee=None)
                                        invoice_fee_passenger.save()
                                        print('fee unissued saved')
                
                pnr.customer_id = customer.id
                pnr.save()

            elif pnr.type == 'EWA' and pnr.status_value == 1:
                if customer_id != '':
                    invoice_ewa = Invoice.objects.filter(pnr=pnr_id)
                    customer = Client.objects.get(pk=int(customer_id))
                    if invoice_ewa.exists():
                        invoice_ewa_detail = invoice_ewa.first()
                        passenger_invoice = PassengerInvoice.objects.filter(pnr=int(pnr_id), status='quotation', invoice_id = invoice_ewa_detail)
                        print('EWA saved')
                        if not passenger_invoice.exists():
                            passenger_invoice = PassengerInvoice(ticket=None, pnr=pnr, type='Billet', client=customer, user_follower=user, is_checked=True, fee=None, status='quotation',invoice_id = invoice_ewa_detail, other_fee=None)
                            passenger_invoice.save()

                        pnr.customer_id = customer.id
                        pnr.save()

                pnr.customer_id = customer.id
                pnr.save() 

        if 'pnrId' and 'otherfeesIdsChecked' and 'customerId' and 'refCde' in request.POST:
            list_other_fees_id = json.loads(request.POST.get('otherfeesIdsChecked'))
            customer_id = request.POST.get('customerId')
            reference = request.POST.get('refCde')
            print('list other_fee: ' + str(list_other_fees_id))
            print('customer_id ' + str(customer_id))
            if list_other_fees_id != [] and list_other_fees_id != '' and customer_id != '':
                user = User.objects.get(pk=int(request.user.id))
                customer = Client.objects.get(pk=int(customer_id))
                pnr = Pnr.objects.get(pk=pnr_id)
                pnr.customer_id = customer.id
                pnr.save()

                if pnr.status_value == 0:
                    for other_fees_id in list_other_fees_id:
                        other_fees = OthersFee.objects.filter(pk=int(other_fees_id),pnr=int(pnr_id), other_fee_status=1)
                        for other_fees_item in other_fees:
                            invoice_fee_passenger = PassengerInvoice.objects.filter(fee=other_fees_item.id, pnr=int(pnr_id), status='sale')
                            if not invoice_fee_passenger.exists():
                                invoice_fee_passenger = PassengerInvoice(
                                    fee=None, pnr=pnr, client=customer, type=other_fees_item.fee_type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, other_fee=other_fees_item, status='sale')
                                invoice_fee_passenger.save()
                                other_fees_fee = Fee.objects.filter(other_fee=other_fees_item.id, pnr=pnr.id)
                                for fee_item in other_fees_fee:
                                    invoice_fee_passenger = PassengerInvoice.objects.filter(fee=fee_item.id, pnr=int(pnr_id))
                                    if not invoice_fee_passenger.exists():
                                        invoice_fee_passenger = PassengerInvoice(
                                            fee=fee_item, pnr=pnr, client=customer, type=fee_item.type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, other_fee=None, status='sale')
                                        invoice_fee_passenger.save()

                elif pnr.status_value == 1:
                    print('Unissuing other_fees')
                    other_fees = OthersFee.objects.filter(pnr=pnr_id, other_fee_status=1)
                    for other_fees_item in other_fees:
                        invoice_fee_passenger = PassengerInvoice.objects.filter(fee=other_fees_item.id, pnr=int(pnr_id), status='quotation')
                        if not invoice_fee_passenger.exists():
                            invoice_fee_passenger = PassengerInvoice(
                                fee=None, pnr=pnr, client=customer, type=other_fees_item.fee_type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, other_fee=other_fees_item, status='quotation')
                            invoice_fee_passenger.save()
                            other_fees_fee = Fee.objects.filter(other_fee=other_fees_item.id, pnr=pnr.id)
                            for fee_item in other_fees_fee:
                                invoice_fee_passenger = PassengerInvoice.objects.filter(fee=fee_item.id, pnr=int(pnr_id))
                                if not invoice_fee_passenger.exists():
                                    invoice_fee_passenger = PassengerInvoice(
                                        fee=fee_item, pnr=pnr, client=customer, type=fee_item.type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, other_fee=None, status='quotation')
                                    invoice_fee_passenger.save()
            
        if 'feeCost' in request.POST:
            fee_cost = json.loads(request.POST.get('feeCost'))
            
            for item in fee_cost:
                cost = item[1]
                service_fee = Fee.objects.filter(pk=int(item[0]))
                # get current total
                initial_total = 0
                try:
                    invoice_detail_obj = InvoiceDetails().get_invoice_detail_by_pnr(service_fee.first().pnr)
                    initial_total = invoice_detail_obj.total
                except:
                    traceback.print_exc()
                if service_fee.exists():
                    # get current fee cost
                    current_cost = service_fee.first().cost
                    # update cost and total by the new cost
                    # and update old_cost by the current cost
                    service_fee.update(cost=cost, total=cost, old_cost=current_cost)
                    # save fee update history
                    History().fee_history(service_fee.first(), request.user, current_cost, cost, initial_total)

    return JsonResponse(context)

@login_required(login_url='index')
def get_order(request, pnr_id):
    context = {}
    today = datetime.now().strftime('%Y%m%d%H%M%S') 
    fee = ''
    ticket = ''
    vendor_user = None
    user_copy = None
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) #get the parent folder of the current file
    config = Configuration.objects.filter(name='File saving configuration', value_name='Saving protocol', environment='test')

    
    file_dir = 'C:\\Users\\NEC04\\Documents\\Gestion PNR\\travelagency\\AmadeusDecoder\\export'
    customer_dir = 'C:\\Users\\NEC04\\Documents\\Gestion PNR\\travelagency\\AmadeusDecoder\\export'
    

    customer_row = {}
    fieldnames_order = [
        'LineID',
        'Type',
        'PNRNumber',
        'PNRType',
        'CustomerId',
        'OrderRef',
        'Agency',
        'Follower',
        'TicketNumber',
        'Civility',
        'PassengerFirstname',
        'PassengerLastname',
        'Segments',
        'DocCurrency',
        'Transport',
        'Tax',
        'Status',
        'Vendor',
        'TicketId',
        'IssueDate',
        'OrderNumber',
        'OtherFeeId'
    ]
    fieldnames_customer = [
        'id',
        'CT_Num',
        'CT_Intitule',
        'CT_Type',
        'CT_Classement',
        'CT_Contact',
        'CT_Adresse',
        'CT_Complement',
        'CT_CodePostal',
        'CT_Ville',
        'CT_Pays',
        'CT_Telephone',
        'CT_Email',
        'CT_Site'
    ]

    order_df = pd.DataFrame(columns=fieldnames_order)
    customer_df = pd.DataFrame(columns=fieldnames_customer)

    csv_order_lines = []
    csv_customer_lines = []

    if request.method== 'POST':
        if 'pnrId' and 'customerIdsChecked' in request.POST:
            pnr_id = request.POST.get('pnrId')
            reference = request.POST.get('refCde')
            customer_ids = json.loads(request.POST.get('customerIdsChecked'))

        pnr = Pnr.objects.get(pk=int(pnr_id))
        invoice = Invoice.objects.filter(pnr=int(pnr_id))
        if User.objects.filter(pk=int(request.user.id)).exists():
            user = User.objects.filter(pk=int(request.user.id)).first()

        if pnr.status == 'Emis':
            if pnr.get_emit_agent() is not None:
                vendor_user = pnr.get_emit_agent()
            elif pnr.agent is not None:
                vendor_user = pnr.agent

        if invoice.exists():
            invoice.update(reference=reference)
        
        pnr_quotation = PassengerInvoice.objects.filter(status='quotation', is_quotation=True, pnr=pnr_id)
        if pnr_quotation.exists():
            tickets = Ticket.objects.filter(pnr=pnr_id, ticket_status=1).exclude(ticket_type='TST')
            for ticket in tickets:
                if not PassengerInvoice.objects.filter(ticket=ticket.id).exists():
                    invoice_tickets_passenger = PassengerInvoice(
                        ticket=ticket, pnr=pnr, type=ticket.ticket_type, client=pnr.customer, reference=reference, user_follower=user, is_checked=True, is_invoiced=True, fee=None, status='sale')
                    invoice_tickets_passenger.save()
                    ticket.is_invoiced = True
                    ticket.save()

                    fee_objects = Fee.objects.filter(ticket=ticket.id)
                    if fee_objects.exists():
                        for fee_item in fee_objects:
                            invoice_fee_passenger = PassengerInvoice.objects.filter(fee=fee_item.id, pnr=int(pnr_id))
                            if not invoice_fee_passenger.exists():
                                invoice_fee_passenger = PassengerInvoice(
                                    fee=fee_item, pnr=pnr, client=pnr.customer, type=fee_item.type, reference=reference, user_follower=user, is_checked=True, is_invoiced=True, ticket=None, status='sale')
                                invoice_fee_passenger.save()
                                fee_item.is_invoiced = True
                                fee_item.save()


            other_fees = OthersFee.objects.filter(pnr=pnr_id, other_fee_status=1)
            for other_fees_item in other_fees:
                invoice_fee_passenger = PassengerInvoice.objects.filter(fee=other_fees_item.id, pnr=int(pnr_id))
                if not invoice_fee_passenger.exists():
                    invoice_fee_passenger = PassengerInvoice(
                        fee=None, pnr=pnr, client=pnr.customer, type=other_fees_item.fee_type, reference=reference, user_follower=user, is_checked=True, is_invoiced=True, ticket=None, other_fee=other_fees_item, status='sale')
                    invoice_fee_passenger.save()
                    other_fees_item.is_invoiced = True
                    other_fees_item.save()

                    other_fees_fee = Fee.objects.filter(other_fee=other_fees_item.id, pnr=pnr.id)
                    for fee_item in other_fees_fee:
                        invoice_fee_passenger = PassengerInvoice.objects.filter(fee=fee_item.id, pnr=int(pnr_id))
                        if not invoice_fee_passenger.exists():
                            invoice_fee_passenger = PassengerInvoice(
                                fee=fee_item, pnr=pnr, client=pnr.customer, type=fee_item.type, reference=reference, user_follower=user, is_checked=True, is_invoiced=True, ticket=None, other_fee=None, status='sale')
                            invoice_fee_passenger.save()
                            fee_item.is_invoiced = True
                            fee_item.save()

        for customer_id in customer_ids:
            "update the line of order of the current PNR to state invoiced"
            orders = PassengerInvoice.objects.filter(pnr=pnr_id, client=customer_id, is_invoiced=False)
            order_invoice_number = datetime.now().strftime('%Y%m%d%H%M') + str(random.randint(1,9)) # SET ORDER NUMBER
            for order in orders:
                segments_parts = []
                if order.status == 'sale':
                    segments_parts = []
                    pnr_order = Pnr.objects.get(pk=order.pnr.id)
                    if order.ticket is not None and order.ticket.ticket_status == 1:
                        ticket = Ticket.objects.get(pk=order.ticket.id)
                        ticket_ssr = ticket.ticket_ssrs.all()
                        # segment
                        if ticket.ticket_type != 'EMD':
                            segments_parts.append(ticket.ticket_parts.all().order_by('segment__id'))
                        elif ticket.ticket_type == 'EMD':
                            if ticket_ssr.exists():
                                for ticket_segment in ticket_ssr:
                                    segments_parts.append(ticket_segment.ssr.segments.all().order_by('id'))
                            else:
                                segments_parts.append(ticket.ticket_parts.all().order_by('segment__id'))
                        
                        air_segments = []
                        segment_names = []
                        segment_dates = []
                        
                        for segment in segments_parts:
                            for part in segment:
                                if part.segment.segment_type == 'Flight' :
                                    _segment = {
                                        'Name': part.segment.segmentorder,
                                        'Fly': '%s %s' % (part.segment.servicecarrier.iata, part.segment.flightno),
                                        'Class': part.segment.flightclass if part.segment.flightclass is not None else '',
                                        'Departure': part.segment.codeorg.iata_code,
                                        'Arrival': part.segment.codedest.iata_code,
                                        'DepartureDatetime' : part.segment.departuretime.strftime('%d/%m/%Y %H:%M') if part.segment.segment_state == 0 and part.segment.departuretime else part.segment.departuretime.strftime('%d/%m/%Y %H:%M') if part.segment.departuretime else '',
                                        'ArrivalDatetime' : part.segment.arrivaltime.strftime('%d/%m/%Y %H:%M') if part.segment.segment_state == 0 and part.segment.arrivaltime else '',   
                                    }
                                    air_segments.append(_segment)

                        type_ticket = ''
                        if ticket.is_refund:
                            type_ticket = 'Remboursement'
                        else:
                            type_ticket = ticket.ticket_type

                        csv_order_lines.append({
                            'LineID': order.id, # type: ignore
                            'Type': type_ticket,
                            'PNRNumber': pnr_order.number,
                            'PNRType': pnr_order.type,
                            'CustomerId': order.client.id, # type: ignore
                            'OrderRef': order.reference, 
                            'Agency': '%s: %s' % (pnr_order.agency.name, pnr_order.agency.code) if pnr_order.agency is not None else pnr_order.agency_name if pnr_order.type == 'EWA' else '',
                            'Follower': pnr_order.agent.username if pnr_order.agent is not None else pnr_order.agent_code if pnr_order.agent_code is not None else '',
                            'TicketNumber': ticket.number,
                            'Civility': ticket.passenger.designation, # type: ignore
                            'PassengerFirstname': ticket.passenger.name, # type: ignore
                            'PassengerLastname': ticket.passenger.surname, # type: ignore
                            'Segments': json.dumps(air_segments),
                            'DocCurrency': 'EUR',
                            'Transport': ticket.transport_cost,
                            'Tax': ticket.tax,
                            'Status': order.status,
                            'Vendor': vendor_user.username if vendor_user is not None else pnr.agent_code,
                            'TicketId': ticket.id if ticket.id is not None else '',
                            'IssueDate': ticket.issuing_date.strftime('%d/%m/%Y') if ticket.issuing_date is not None else '',
                            'OrderNumber': order_invoice_number,
                            'OtherFeeId': '',
                            'Designation':'',
                        })

                        if len(csv_order_lines) == 0:
                            break
                        else:
                            order.is_invoiced = True
                            order.invoice_number = order_invoice_number
                            order.save()
                            order.ticket.is_invoiced = True
                            order.ticket.save()

                    if order.fee is not None:
                        fee = Fee.objects.filter(pk=order.fee.id)
                        for item in fee:
                            if order.fee.ticket is not None and order.fee.ticket.ticket_status == 1 and order.fee.ticket.id == item.ticket.id:
                                csv_order_lines.append({
                                    'LineID': order.id,
                                    'Type': item.type,
                                    'PNRNumber': pnr_order.number,
                                    'PNRType': pnr_order.type,
                                    'CustomerId': order.client.id,
                                    'OrderRef': order.reference, 
                                    'Agency': '%s: %s' % (pnr_order.agency.name, pnr_order.agency.code) if pnr_order.agency is not None else pnr_order.agency_name if pnr_order.type == 'EWA' else '',
                                    'Follower': pnr_order.agent.username if pnr_order.agent is not None else pnr_order.agent_code if pnr_order.agent_code is not None else '',
                                    'TicketNumber': '',
                                    'Civility': '',
                                    'PassengerFirstname': '',
                                    'PassengerLastname': '',
                                    'Segments': '',                      
                                    'DocCurrency': 'EUR',
                                    'Transport': item.cost,
                                    'Tax': item.tax,
                                    'Status': order.status,
                                    'Vendor': vendor_user.username if vendor_user is not None else pnr.agent_code,
                                    'TicketId': item.ticket.id if item.ticket is not None else '',
                                    'IssueDate': '',
                                    'OrderNumber': order_invoice_number,
                                    'OtherFeeId': '',
                                    'Designation': '',
                                })
                                
                                if len(csv_order_lines) == 0:
                                    break
                                else:
                                    order.is_invoiced = True
                                    order.invoice_number = order_invoice_number
                                    order.save()
                                    order.fee.is_invoiced =True
                                    order.fee.save()

                    type_other_fee = ''
                    if order.other_fee is not None and order.other_fee.other_fee_status == 1:
                        other_fee = OthersFee.objects.filter(pk=order.other_fee.id)
                        for item in other_fee:
                            if item.fee_type == 'EMD' or item.fee_type == 'TKT' or item.fee_type == 'Cancellation' or item.fee_type == 'AVOIR COMPAGNIE':
                                type_other_fee = item.fee_type
                            else:
                                type_other_fee = 'EMD'
                            csv_order_lines.append({
                                'LineID': order.id,
                                'Type': type_other_fee,
                                'PNRNumber': pnr_order.number,
                                'PNRType': pnr_order.type,
                                'CustomerId': order.client.id,
                                'OrderRef': order.reference, 
                                'Agency': '%s: %s' % (pnr_order.agency.name, pnr_order.agency.code) if pnr_order.agency is not None else pnr_order.agency_name if pnr_order.type == 'EWA' else '',
                                'Follower': pnr_order.agent.username if pnr_order.agent is not None else pnr_order.agent_code if pnr_order.agent_code is not None else '',
                                'TicketNumber': '',
                                'Civility': '',
                                'PassengerFirstname': '',
                                'PassengerLastname': '',
                                'Segments': '',                      
                                'DocCurrency': 'EUR',
                                'Transport': item.cost,
                                'Tax': item.tax,
                                'Status': order.status,
                                'Vendor': vendor_user.username if vendor_user is not None else pnr.agent_code,
                                'TicketId': '',
                                'IssueDate': item.creation_date.strftime('%d/%m/%Y') if item.creation_date is not None else '',
                                'OrderNumber': order_invoice_number,
                                'OtherFeeId': item.id if item is not None else '',
                                'Designation': item.designation if item is not None else '',
                            })
                            
                            if len(csv_order_lines) == 0:
                                break
                            else:
                                order.is_invoiced = True
                                order.invoice_number = order_invoice_number
                                order.save()
                                order.other_fee.is_invoiced = True
                                order.other_fee.save()

                    if order.fee is not None:
                        fee = Fee.objects.filter(pk=order.fee.id)
                        for item in fee:
                            if order.fee.other_fee is not None and order.fee.other_fee.other_fee_status == 1 and order.fee.other_fee.id == item.other_fee.id:
                                csv_order_lines.append({
                                    'LineID': order.id,
                                    'Type': item.type,
                                    'PNRNumber': pnr_order.number,
                                    'PNRType': pnr_order.type,
                                    'CustomerId': order.client.id,
                                    'OrderRef': order.reference, 
                                    'Agency': '%s: %s' % (pnr_order.agency.name, pnr_order.agency.code) if pnr_order.agency is not None else pnr_order.agency_name if pnr_order.type == 'EWA' else '',
                                    'Follower': pnr_order.agent.username if pnr_order.agent is not None else pnr_order.agent_code if pnr_order.agent_code is not None else '',
                                    'TicketNumber': '',
                                    'Civility': '',
                                    'PassengerFirstname': '',
                                    'PassengerLastname': '',
                                    'Segments': '',                      
                                    'DocCurrency': 'EUR',
                                    'Transport': item.cost,
                                    'Tax': item.tax,
                                    'Status': order.status,
                                    'Vendor': vendor_user.username if vendor_user is not None else pnr.agent_code,
                                    'TicketId': '',
                                    'IssueDate': '',
                                    'OrderNumber': order_invoice_number,
                                    'OtherFeeId': item.other_fee.id if item.other_fee is not None else '',
                                    'Designation': ''
                                })
                                
                                if len(csv_order_lines) == 0:
                                    break
                                else:
                                    order.is_invoiced = True
                                    order.invoice_number = order_invoice_number
                                    order.save()
                                    order.fee.is_invoiced = True
                                    order.fee.save()
                
            customers = Client.objects.filter(pk=int(customer_id))
            for customer in customers:
                customer_row['id'] = customer.id
                customer_row['CT_Num'] = customer.ct_num.strip().replace('\n', '') if customer.ct_num is not None else ''
                customer_row['CT_Intitule'] = customer.intitule.strip().replace('\n', '') if customer.intitule is not None else ''
                customer_row['CT_Adresse'] = customer.address_1.strip().replace('\n', '') if customer.address_1 is not None else ''
                customer_row['CT_Type'] = customer.ct_type
                if customer.city is not None or customer.city != '':
                    customer_row['CT_Ville'] = customer.city.strip().replace('\n', '') if customer.city is not None else ''
                else:
                    customer_row['CT_Ville'] = ''
                if customer.classment is not None or customer.classment != '':
                    customer_row['CT_Classement'] = customer.classment.strip().replace('\n', '') if customer.classment is not None else ''
                else:
                    customer_row['CT_Classement'] = ''
                if customer.contact is not None or customer.contact != '':
                    customer_row['CT_Contact'] = customer.contact.strip().replace('\n', '') if customer.contact is not None else ''
                else:
                    customer_row['CT_Contact'] = ''
                if customer.complement is not None or customer.complement != '':
                    customer_row['CT_Complement'] = customer.complement.strip().replace('\n', '') if customer.complement is not None else ''
                else:
                    customer_row['CT_Complement'] = ''
                if customer.code_postal is not None or customer.code_postal != '':
                    customer_row['CT_CodePostal'] = customer.code_postal.strip().replace('\n', '') if customer.code_postal is not None else ''
                else:
                    customer_row['CT_CodePostal'] = ''
                if customer.telephone is not None or customer.telephone != '':
                    customer_row['CT_Telephone'] = customer.telephone.strip().replace('\n', '') if customer.telephone is not None else ''
                else:
                    customer_row['CT_Telephone'] = ''
                if customer.email is not None or customer.email != '':
                    customer_row['CT_Email'] = customer.email.strip().replace('\n', '') if customer.email is not None else ''
                else:
                    customer_row['CT_Email'] = ''
                if customer.site is not None or customer.site != '':
                    customer_row['CT_Site'] = customer.site.strip().replace('\n', '') if customer.site is not None else ''
                else:
                    customer_row['CT_Site'] = ''
                if customer.country is not None or customer.country != None:
                    customer_row['CT_Pays'] = customer.country.strip().replace('\n', '') if customer.country is not None else ''
                else:
                    customer_row['CT_Pays'] = ''
                csv_customer_lines.append(customer_row)

        order_df = pd.concat([order_df, pd.DataFrame(csv_order_lines)])
        customer_df = pd.concat([customer_df, pd.DataFrame(csv_customer_lines)])


        if not order_df.empty and not customer_df.empty:
            order_file = os.path.join(file_dir, 'FormatsSaleOrderExportOdoo{}.csv'.format(today))
            customer_file = os.path.join(customer_dir, 'CustomerExport{}.csv'.format(today))
            order_df.to_csv(order_file, index=False, sep=';')
            customer_df.to_csv(customer_file, index=False, sep=';')
            if config.exists() and config.first().single_value == 'FTP':
                hostname, port, password, username, order_repository, customer_repository, odoo_link = config.first().dict_value.get('hostname'), int(config.first().dict_value.get('port')), config.first().dict_value.get('password'), config.first().dict_value.get('username'), config.first().dict_value.get('repository') + '/Order/', config.first().dict_value.get('repository') + '/Customer/', config.first().dict_value.get('link')
                upload_file(order_file, order_repository, 'FormatsSaleOrderExportOdoo{}.csv'.format(today), username, password, hostname, port)
                upload_file(customer_file, customer_repository, 'CustomerExport{}.csv'.format(today), username, password, hostname, port)
                print("------------------Call Odoo import-----------------------")
                response = requests.get(odoo_link)

        ticket_not_order = Ticket.objects.filter(pnr=pnr_id, is_invoiced=False, ticket_status=1).exclude(total=0)
        ticket_no_adc_order = Ticket.objects.filter(pnr=pnr_id, is_invoiced=False, ticket_status=1).filter(Q(total=0) & Q(is_no_adc=True))
        other_fee_order = OthersFee.objects.filter(pnr=pnr_id, is_invoiced=False, other_fee_status=1).filter(Q(total__gt=0))

        if not ticket_not_order.exists() and not other_fee_order.exists() and not ticket_no_adc_order.exists():
            pnr.is_invoiced = True
            pnr.save()
        

    return JsonResponse(context)

@login_required(login_url='index')
def get_quotation(request, pnr_id):
    context = {}
    today = datetime.now().strftime('%Y%m%d%H%M%S') 
    fee = ''
    ticket = ''
    vendor_user = None
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) #get the parent folder of the current file

    file_dir = 'D:\\Projects\\Django\\Issoufali\\travelagency\\AmadeusDecoder\\export'
    customer_dir = 'D:\\Projects\\Django\\Issoufali\\travelagency\\AmadeusDecoder\\export'

    

    customer_row = {}
    fieldnames_order = [
        'LineID',
        'Type',
        'PNRNumber',
        'PNRType',
        'CustomerId',
        'OrderRef',
        'Agency',
        'Follower',
        'TicketNumber',
        'Civility',
        'PassengerFirstname',
        'PassengerLastname',
        'Segments',
        'DocCurrency',
        'Transport',
        'Tax',
        'Status',
        'Vendor',
        'TicketId',
        'IssueDate',
        'OrderNumber',
        'OtherFeeId',
        'OPC'
    ]
    fieldnames_customer = [
        'id',
        'CT_Num',
        'CT_Intitule',
        'CT_Type',
        'CT_Classement',
        'CT_Contact',
        'CT_Adresse',
        'CT_Complement',
        'CT_CodePostal',
        'CT_Ville',
        'CT_Pays',
        'CT_Telephone',
        'CT_Email',
        'CT_Site'
    ]

    quotation_df = pd.DataFrame(columns=fieldnames_order)
    customer_df = pd.DataFrame(columns=fieldnames_customer)

    csv_quotation_lines = []
    csv_customer_lines = []

    if request.method== 'POST':
        if 'pnrId' in request.POST:
            pnr_id = request.POST.get('pnrId')
            reference = request.POST.get('refCde')
            passengers_ids = json.loads(request.POST.get('passengerIds'))
            customer_object = request.POST.get('customerId')

        pnr = Pnr.objects.get(pk=int(pnr_id))
        invoice = Invoice.objects.filter(pnr=int(pnr_id))
        user = User.objects.get(pk=int(request.user.id))
        
        if pnr.agent is not None:
            vendor_user = pnr.agent

        if invoice.exists():
            invoice.update(reference=reference)

        orders = PassengerInvoice.objects.filter(pnr=pnr_id, status='quotation')
        customers = Client.objects.all()

        for order in orders:
            if order.is_quotation == False:
                pnr_order = Pnr.objects.get(pk=order.pnr.id)
                if order.ticket is not None:
                    ticket = Ticket.objects.get(pk=order.ticket.id)
                    segments_parts = ticket.ticket_parts.all().order_by('segment__id')
                    tst_ticket_passengers = ticket.ticket_tst_parts.filter(ticket_id=ticket.id)
                    tst_passenger_name, names = [], ''
                    tst_passenger_firstname, firstnames = [], ''
                    tst_passenger_designation, designations = [], ''
                    if tst_ticket_passengers is not None:
                        for tst_ticket in tst_ticket_passengers:
                            passenger = Passenger.objects.get(pk=int(tst_ticket.passenger_id))
                            tst_passenger_name.append(passenger.name if passenger.name is not None else '')
                            tst_passenger_firstname.append(passenger.surname if passenger.surname is not None else '')
                            tst_passenger_designation.append(passenger.designation if passenger.designation is not None else '')

                    # segment
                    air_segments = []
                    segment_names = []
                    segment_dates = []
                    if segments_parts is not None:
                        for part in segments_parts:
                            if part.segment.segment_type == 'Flight' :
                                _segment = {
                                    'Name': part.segment.segmentorder,
                                    'Fly': '%s %s' % (part.segment.servicecarrier.iata, part.segment.flightno),
                                    'Class': part.segment.flightclass if part.segment.flightclass is not None else '',
                                    'Departure': part.segment.codeorg.iata_code,
                                    'Arrival': part.segment.codedest.iata_code,
                                    'DepartureDatetime' : part.segment.departuretime.strftime('%d/%m/%Y %H:%M') if part.segment.segment_state == 0 and part.segment.departuretime else part.segment.departuretime.strftime('%d/%m/%Y %H:%M') if part.segment.departuretime else '',
                                    'ArrivalDatetime' : part.segment.arrivaltime.strftime('%d/%m/%Y %H:%M') if part.segment.segment_state == 0 and part.segment.arrivaltime else '',   
                                }
                                air_segments.append(_segment)
                        
                    csv_quotation_lines.append({
                        'LineID': order.id,
                        'Type': order.type,
                        'PNRNumber': pnr_order.number,
                        'PNRType': pnr_order.type,
                        'CustomerId': order.client.id,
                        'OrderRef': order.reference if order.reference is not None else '', 
                        'Agency': '%s: %s' % (pnr_order.agency.name, pnr_order.agency.code) if pnr_order.agency is not None else pnr_order.agency_name if pnr_order.type == 'EWA' else '',
                        'Follower': pnr_order.agent.username if pnr_order.agent is not None else pnr_order.agent_code if pnr_order.agent_code is not None else '',
                        'TicketNumber': ticket.number,
                        'Civility': ', '.join(tst_passenger_designation),
                        'PassengerFirstname': ', '.join(tst_passenger_firstname),
                        'PassengerLastname': ', '.join(tst_passenger_name),
                        'Segments': json.dumps(air_segments),
                        'DocCurrency': 'EUR',
                        'Transport': ticket.transport_cost,
                        'Tax': ticket.tax,
                        'Status': 'quotation',
                        'Vendor': vendor_user.username if vendor_user is not None else pnr.agent_code,
                        'TicketId': ticket.id if ticket is not None else '',
                        'IssueDate': '',
                        'OrderNumber': '',
                        'OtherFeeId': '',
                        'OPC': pnr_order.get_min_opc()
                    })
                    
                    if len(csv_quotation_lines) > 0 :
                        order.is_quotation = True
                        order.save()

                if order.fee is not None:
                    fee = Fee.objects.filter(pk=order.fee.id)
                    for item in fee:
                        if order.fee.ticket is not None and order.fee.ticket.id == item.ticket.id:
                            csv_quotation_lines.append({
                                'LineID': order.id,
                                'Type': item.type,
                                'PNRNumber': pnr_order.number,
                                'PNRType': pnr_order.type,
                                'CustomerId': order.client.id,
                                'OrderRef': order.reference, 
                                'Agency': '%s: %s' % (pnr_order.agency.name, pnr_order.agency.code) if pnr_order.agency is not None else pnr_order.agency_name if pnr_order.type == 'EWA' else '',
                                'Follower': pnr_order.agent.username if pnr_order.agent is not None else pnr_order.agent_code if pnr_order.agent_code is not None else '',
                                'TicketNumber': '',
                                'Civility': '',
                                'PassengerFirstname': '',
                                'PassengerLastname': '',
                                'Segments': '',                     
                                'DocCurrency': 'EUR',
                                'Transport': item.cost,
                                'Tax': item.tax,
                                'Status': 'quotation',
                                'Vendor': vendor_user.username if vendor_user is not None else pnr.agent_code,
                                'TicketId': item.ticket.id if item.ticket is not None else '',
                                'IssueDate': '',
                                'OrderNumber': '',
                                'OtherFeeId': '',
                                'OPC': pnr_order.get_min_opc()
                            })
                            
                            if len(csv_quotation_lines) > 0 :
                                order.is_quotation = True
                                order.save()
                            
                if order.other_fee is not None:
                    other_fee = OthersFee.objects.filter(pk=order.other_fee.id)
                    for item in other_fee:
                        if item.fee_type == 'EMD' and item.fee_type == 'TKT' and item.fee_type == 'Cancellation' and item.fee_type == 'AVOIR COMPAGNIE':
                            type_other_fee = item.fee_type
                        else:
                            type_other_fee = item.designation
                        csv_quotation_lines.append({
                            'LineID': order.id,
                            'Type': type_other_fee,
                            'PNRNumber': pnr_order.number,
                            'PNRType': pnr_order.type,
                            'CustomerId': order.client.id,
                            'OrderRef': order.reference, 
                            'Agency': '%s: %s' % (pnr_order.agency.name, pnr_order.agency.code) if pnr_order.agency is not None else pnr_order.agency_name if pnr_order.type == 'EWA' else '',
                            'Follower': pnr_order.agent.username if pnr_order.agent is not None else pnr_order.agent_code if pnr_order.agent_code is not None else '',
                            'TicketNumber': '',
                            'Civility': '',
                            'PassengerFirstname': '',
                            'PassengerLastname': '',
                            'Segments': '',                      
                            'DocCurrency': 'EUR',
                            'Transport': item.cost,
                            'Tax': item.tax,
                            'Status': order.status,
                            'Vendor': vendor_user.username if vendor_user is not None else pnr.agent_code,
                            'TicketId': '',
                            'IssueDate': '',
                            'OrderNumber': '',
                            'OtherFeeId': item.id if item is not None else '',
                            'OPC': pnr_order.get_min_opc()
                        })
                        
                        if len(csv_quotation_lines) > 0 :
                            order.is_quotation = True
                            order.save()

                if order.invoice_id is not None:
                    segments_parts = PnrAirSegments.objects.filter(pnr=pnr_id)
                    air_segments = []
                    segment_names = []
                    segment_dates = []
                    if segments_parts is not None:
                        for part in segments_parts:
                            if part.segment_type == 'Flight' :
                                segment_names.append('%s %s' % (part.servicecarrier.iata, part.flightno))
                                air_segments.append(part.codeorg.iata_code)
                                air_segments.append(part.codedest.iata_code)
                                air_segments.append(part.codeorg.iata_code)
                                air_segments.append(part.codedest.iata_code)
                                segment_dates.append(part.departuretime.strftime('%d/%m/%Y %H:%M') if part.segment_state == 0 else part.departuretime.strftime('%d/%m/%Y'))
                                segment_dates.append(part.arrivaltime.strftime('%d/%m/%Y %H:%M') if part.segment_state == 0 else '')
                    
                    csv_quotation_lines.append({
                        'LineID': order.id,
                        'Type': 'Billet',
                        'PNRNumber': pnr_order.number,
                        'PNRType': pnr_order.type,
                        'CustomerId': order.client.id,
                        'OrderRef': order.reference, 
                        'Agency': '%s: %s' % (pnr_order.agency.name, pnr_order.agency.code) if pnr_order.agency is not None else pnr_order.agency_name if pnr_order.type == 'EWA' else '',
                        'Follower': pnr_order.agent.username if pnr_order.agent is not None else pnr_order.agent_code if pnr_order.agent_code is not None else '',
                        'TicketNumber': '',
                        'Civility': '',
                        'PassengerFirstname': '',
                        'PassengerLastname': '',
                        'Segments': json.dumps(air_segments),
                        'DocCurrency': 'EUR',
                        'Transport': order.invoice_id.detail.total if order.invoice_id is not None else '0',
                        'Tax': '0',
                        'Status': 'quotation',
                        'Vendor': vendor_user.username if vendor_user is not None else pnr.agent_code,
                        'TicketId': '',
                        'IssueDate': '',
                        'OrderNumber': '',
                        'OtherFeeId': item.other_fee.id if item.other_fee is not None else '',
                        'OPC': pnr_order.get_min_opc()
                    })
                    
                    if len(csv_quotation_lines) > 0 :
                        order.is_quotation = True
                        order.save()

        customers = Client.objects.filter(pk=int(customer_object))
        if customers.exists():
            customer = customers.first()
            customer_row['id'] = customer.id
            customer_row['CT_Num'] = customer.ct_num
            customer_row['CT_Intitule'] = customer.intitule
            customer_row['CT_Adresse'] = customer.address_1
            customer_row['CT_Type'] = customer.ct_type
            if customer.city is not None or customer.city != '':
                customer_row['CT_Ville'] = customer.city
            else:
                customer_row['CT_Ville'] = ''
            if customer.classment is not None or customer.classment != '':
                customer_row['CT_Classement'] = customer.classment
            else:
                customer_row['CT_Classement'] = ''
            if customer.contact is not None or customer.contact != '':
                customer_row['CT_Contact'] = customer.contact
            else:
                customer_row['CT_Contact'] = ''
            if customer.complement is not None or customer.complement != '':
                customer_row['CT_Complement'] = customer.complement
            else:
                customer_row['CT_Complement'] = ''
            if customer.code_postal is not None or customer.code_postal != '':
                customer_row['CT_CodePostal'] = customer.code_postal
            else:
                customer_row['CT_CodePostal'] = ''
            if customer.telephone is not None or customer.telephone != '':
                customer_row['CT_Telephone'] = customer.telephone
            else:
                customer_row['CT_Telephone'] = ''
            if customer.email is not None or customer.email != '':
                customer_row['CT_Email'] = customer.email
            else:
                customer_row['CT_Email'] = ''
            if customer.site is not None or customer.site != '':
                customer_row['CT_Site'] = customer.site
            else:
                customer_row['CT_Site'] = ''
            if customer.country is not None or customer.country != None:
                customer_row['CT_Pays'] = customer.country
            else:
                customer_row['CT_Pays'] = ''
            csv_customer_lines.append(customer_row)

        quotation_df = pd.concat([quotation_df, pd.DataFrame(csv_quotation_lines)])
        customer_df = pd.concat([customer_df, pd.DataFrame(csv_customer_lines)])

        if not quotation_df.empty and not customer_df.empty:
            quotation_df.to_csv(os.path.join(file_dir, 'FormatsSaleOrderExportOdoo{}.csv'.format(today)), index=False, sep=';')
            customer_df.to_csv(os.path.join(customer_dir, 'CustomerExport{}.csv'.format(today)), index=False, sep=';')

        print("------------------Call Odoo import-----------------------")
        response = requests.get("https://testodoo.issoufali.phidia.fr/web/syncorders")
        print(response.content)
        

    return JsonResponse(context)

@login_required(login_url='index')
def import_product(request, pnr_id):
    if request.method == 'POST':
        if 'listNewProduct' in request.POST:
            product = json.loads(request.POST.get('listNewProduct'))
            pnr = Pnr.objects.get(pk=int(pnr_id))
            other_fees = OthersFee.objects.filter(pnr=pnr_id, product_id=product[0])
            other_fees = OthersFee(designation=product[2], cost=product[3], tax=product[4], total=product[5], pnr=pnr, fee_type=product[1], passenger_segment=product[6], reference=product[7], quantity=1)
            other_fees.save()
            
            # save creator user to user copying
            try:
                user_id = request.user.id
                user_copying = UserCopying()
                user_copying.document = pnr.number
                user_copying.user_id = User.objects.get(pk=int(user_id))
                user_copying.save()
            except:
                print("User copying fetching error")

    return JsonResponse({})

@login_required(login_url='index')
def get_product(request, pnr_id):
    context = {}
    if request.method == 'POST':
        if 'productId' in request.POST:
            product_id = request.POST.get('productId')
            product = Product.objects.filter(pk=product_id)

        if product.exists():
            context['products'] = list(product.values())
    return JsonResponse(context)

@login_required(login_url='index')
def find_customer(request, pnr_id):
    context = {}
    if request.method == 'POST':
        if 'value' in request.POST:
            value = json.loads(request.POST.get('value'))
            q = Q()
            if len(value) > 0:
                list_clients = []
                if len(value) == 1:
                    string = value[0].split(" ")
                    for word in string:
                        q &= Q(intitule__icontains = word)
                    clients = Client.objects.filter(q)
                    if clients.exists():
                        client = clients.first()
                        context = {
                            "isCustomerFind": True, 
                            "clientId": client.id,
                            "clientIntitule": client.intitule,
                            "clientAddress": client.address_1 + " " + client.address_2 if client.address_1 is not None and client.address_2 is not None else client.address_1 if client.address_1 is not None else "",
                            "clientCity": client.city if client.city is not None else "",
                            "clientCountry": client.country if client.country is not None else "",
                            "clientPostalCode": client.code_postal if client.code_postal is not None else "",
                            "clientDepartment": client.departement if client.departement is not None else "",
                            "clientEmail": client.email if client.email is not None else "",
                            "clientPhone": client.telephone if client.telephone is not None else "",
                        }
                    else:
                        context["isCustomerFind"] = False
                if len(value) == 2:
                    string = value[0].strip().split(" ") + value[1].strip().split(" ")
                    print(string)
                    for word in string:
                        q &= Q(intitule__icontains = word)
                    clients = Client.objects.filter(q)
                    if clients.exists():
                        client = clients.first()
                        context = {
                            "isCustomerFind": True, 
                            "clientId": client.id,
                            "clientIntitule": client.intitule,
                            "clientAddress": client.address_1 + " " + client.address_2 if client.address_1 is not None and client.address_2 is not None else client.address_1 if client.address_1 is not None else "",
                            "clientCity": client.city if client.city is not None else "",
                            "clientCountry": client.country if client.country is not None else "",
                            "clientPostalCode": client.code_postal if client.code_postal is not None else "",
                            "clientDepartment": client.departement if client.departement is not None else "",
                            "clientEmail": client.email if client.email is not None else "",
                            "clientPhone": client.telephone if client.telephone is not None else "",
                        }
                    else:
                        context["isCustomerFind"] = False
            else:
                context["isCustomerFind"] = False
            
    return JsonResponse(context)