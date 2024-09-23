'''
Created on 8 Sep 2022

'''
import os
import json
from datetime import datetime, timezone
import requests
import random
import pandas as pd

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms.models import model_to_dict
from django.conf import settings
from AmadeusDecoder.models.invoice.TicketPassengerSegment import OtherFeeSegment, TicketPassengerSegment

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.pnr.PnrPassenger import PnrPassenger
from AmadeusDecoder.models.user.Users import User, UserCopying
from AmadeusDecoder.models.invoice.Clients import Client
from AmadeusDecoder.models.utilities.Comments import Comment, Response
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.Fee import Fee, ReducePnrFeeRequest, OthersFee
from AmadeusDecoder.models.invoice.Invoice import Invoice, InvoicesCanceled
from AmadeusDecoder.models.invoice.InvoiceDetails import InvoiceDetails
from AmadeusDecoder.models.pnr.Passenger import Passenger
from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
from AmadeusDecoder.models.invoice.Fee import Product
from AmadeusDecoder.models.pnrelements.PnrAirSegments import PnrAirSegments
from AmadeusDecoder.models.history.History import History
from AmadeusDecoder.models.configuration.Configuration import Configuration

from AmadeusDecoder.utilities.FtpConnection import upload_file
from AmadeusDecoder.utilities.SendMail import Sending
import traceback

import AmadeusDecoder.utilities.configuration_data as configs

# FEE_REQUEST_SENDER = {"port":587, "smtp":"smtp.gmail.com", "address":"feerequest.issoufali.pnr@gmail.com", "password":"tnkunwvygtdkxfxg"}
# FEE_REQUEST_RECIPIENT = ['superviseur@agences-issoufali.com','pp@phidia.onmicrosoft.com','mihaja@phidia.onmicrosoft.com','tahina@phidia.onmicrosoft.com']

FEE_REQUEST_SENDER = configs.FEE_REQUEST_SENDER
FEE_REQUEST_RECIPIENT = configs.FEE_REQUEST_RECIPIENT


from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.pnr.OptimizedPnrList import OptimisedPnrList


@login_required(login_url='index')
def home_copy(request):
    def format_date_range(date_range):
        if date_range:
            for fmt in ("%d-%m-%Y", "%Y-%m-%d"):
                try:
                    start_date, end_date = [datetime.strptime(d, fmt) for d in date_range.split(" * ")]
                    return (
                        start_date.replace(hour=0, minute=0, second=0, tzinfo=timezone.utc),
                        end_date.replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
                    )
                except ValueError:
                    continue
        return None, None

    def format_filter_creator(pnr_creator):
        try:
            parsed_creator = json.loads(pnr_creator)
            # Check if 'Empty' is in the list
            if 'Empty' in parsed_creator:
                return "no_creator"
            else:
                # Ensure all elements are valid integers
                return [int(user_id) for user_id in parsed_creator if str(user_id).isdigit()]
        except (json.JSONDecodeError, TypeError, ValueError):
            return None

    # Query users and set filters
    users = User.objects.exclude(
                username__in=('Moïse ISSOUFALI', 'Paul ISSOUFALI')
            ).exclude(role=1).order_by('username').values('id', 'username')

    # Get filters from cookies
    pnr_creator_filter_cookies = request.COOKIES.get('creator_pnr_filter')
    date_range_filter_cookies = request.COOKIES.get('dateRangeFilter')
    is_invoiced_filter_cookies = request.COOKIES.get('filter_pnr')
    agency_name_filter_cookies = request.COOKIES.get('agency_name_filter')
    pnr_status_filter_cookies = request.COOKIES.get('filter_pnr_by_status')
    sorted_creator_filter_cookies = request.COOKIES.get('isSortedByCreator')
    
    sorted_creator_filter = {
        "agent__username": "creator",
        "-agent__username": "-creator"
    }.get(sorted_creator_filter_cookies, None)

    # Get all PNR users's following
    pnr_follower = format_filter_creator(pnr_creator_filter_cookies)
    
    # print(pnr_follower)

    # Processing all available filters
    start_date_range_filter, end_date_range_filter = format_date_range(date_range_filter_cookies)

    # PNR order FILTER (sort)
    pnr_order_list_filter = {
        "asc": "date_of_creation",
        "desc": "-date_of_creation"
    }.get(request.COOKIES.get("creation_date_order_by"), "-date_of_creation")

    # Status invoice PNR FILTER
    is_invoiced_filter = {
        "True": True,
        "False": False,
        "None": None
    }.get(is_invoiced_filter_cookies, False)

    # User following PNR FILTER
    pnr_follower_filter = None
    if pnr_follower:
        pnr_follower_filter = list(users.filter(id__in=pnr_follower).values_list('username', flat=True)) if pnr_follower != "no_creator" else pnr_follower

    # Agency names FILTER
    agency_name_filter = agency_name_filter_cookies

    # PNR status FILTER (Émis ou Non émis)
    pnr_status_filter = {
        '0': 'Emis',
        '1': 'Non émis',
        "2": None
    }.get(pnr_status_filter_cookies)

    # Setting Q filters
    filters = Q()

    # Date range filter
    if start_date_range_filter and end_date_range_filter:
        filters &= Q(date_of_creation__range=[start_date_range_filter, end_date_range_filter])

    # Invoiced status filter
    if is_invoiced_filter is not None:
        filters &= Q(is_invoiced=is_invoiced_filter)

    # PNR follower filter
    if pnr_follower_filter:
        if pnr_follower_filter == 'no_creator':
            filters &= Q(creator=None) | Q(creator="")
        else:
            filters &= Q(creator__in=pnr_follower_filter) | Q(emitter__in=pnr_follower_filter)
            
    # print(pnr_follower_filter)

    # Agency name filter
    if agency_name_filter:
        if agency_name_filter == "0":
            filters &= Q(agency_office_name=None, agency_office_code=None, agency_name='')
        else:
            filters &= Q(agency_office_name__icontains=agency_name_filter) | Q(agency_name__icontains=agency_name_filter)

    # PNR status filter
    if pnr_status_filter:
        filters &= Q(status__iexact=pnr_status_filter)
        
    # Process search query
    search_query = request.GET.get('search_query', '').strip()
    # print(f'Search Query *** {search_query}')
    
    if search_query:
        filters &= Q(number__icontains=search_query) | Q(passengers__icontains=search_query) | \
                   Q(agency_office_code__icontains=search_query) | Q(agency_office_name__icontains=search_query) | Q(agency_name__icontains=search_query) | \
                   Q(creator__icontains=search_query) | Q(emitter__icontains=search_query) | \
                   Q(client__icontains=search_query)
                   
    pnr_list = []
    
    # Get the filtered list and paginate
    if pnr_order_list_filter:
        pnr_list = OptimisedPnrList.objects.filter(filters).order_by(pnr_order_list_filter)
    if sorted_creator_filter:
        pnr_list = OptimisedPnrList.objects.filter(filters).order_by(sorted_creator_filter)

    # Define user-specific filters
    special_usernames = ['Mouniati', 'Farida']
    special_user_ids = [4, 5]

    # Check if the user meets the special condition for Farida and Mouniati user
    if request.user.username in special_usernames or request.user.id in special_user_ids:
        user_filter = Q(creator__iexact='Mouniati') | Q(emitter__iexact='Mouniati') | \
                      Q(creator__iexact='Farida') | Q(emitter__iexact='Farida')
        
        if pnr_follower_filter == 'no_creator':
            pnr_list = pnr_list.filter(Q(creator__isnull=True) | Q(creator=""))
        else:
            pnr_list = pnr_list.filter(user_filter)

    # Check if the user is a comptoir agent with role_id equals to 3
    elif request.user.role_id == 3:
        user_filter = Q(creator__iexact=request.user.username) | Q(emitter__iexact=request.user.username)
        
        if pnr_follower_filter == 'no_creator':
            pnr_list = pnr_list.filter(Q(creator__isnull=True) | Q(creator=""))
        else:
            pnr_list = pnr_list.filter(user_filter)

    
    paginator = Paginator(pnr_list, request.GET.get('paginate_by', 25))
    
    page_num = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)
    
    # Context
    context = {
        'page_obj': page_obj,
        'row_num': paginator.per_page,
        'pnr_count': paginator.count,
        'users': users,
        'search_query': search_query,
    }

    return render(request, 'home-copy.html', context)


@login_required(login_url='index')
def pnr_details(request, pnr_id):
    context = {}
    if pnr_id is not None and pnr_id != '':
        pnr_detail = Pnr.objects.get(pk=pnr_id)
    pnr_detail.update_read_status()
    
    # update ticket status to ticket_status=1 when ticket is present in passenger_invoice table
    pnr_detail.update_ticket_status_present_in_passenger_invoice()
    
    # This function is responsible for attaching tickets to the first passenger and available segments.
    # It is applicable only for Passenger Name Records (PNRs) with a single passenger.
    pnr_detail.attach_ticket_to_first_passenger_segment()
    
    # This function is responsible for updating the fare cost of a ticket or other fees to ensure they are correct.
    pnr_detail.rectify_fare_cost()
    
    context['pnr'] = pnr_detail
    context['passengers'] = pnr_detail.passengers.filter(passenger__passenger_status=1).all().order_by('id')
    context['contacts'] = pnr_detail.contacts.all()
    context['air_segments'] = pnr_detail.segments.filter(segment_type='Flight', air_segment_status=1).all().order_by('segmentorder')
    context['tickets'] = pnr_detail.tickets.filter(Q(ticket_status=1) | Q(is_invoiced=True)).filter(Q(total__gt=0) | Q(is_no_adc=True) | (Q(is_refund=True) & Q(total__lt=0))).all().order_by('number')
    # context['tickets'] = pnr_detail.tickets.filter().all()
    context['other_fees'] = pnr_detail.others_fees.filter((Q(other_fee_status=1) & Q(ticket=None)) | Q(is_invoiced=True)).all()
    # context['clients'] = Client.objects.all().order_by('intitule')
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

        __cancellation = pnr_detail.others_fees.filter(Q(other_fee__in=__other_fee_base)|Q(ticket__in=__ticket_base) | Q(ticket__in=__ticket_no_adc_base)).exclude(fee_type='outsourcing')

        print('__________Cancellation____________')
        print('Ther is the cancellation: ' + str(__cancellation))
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
            if pnr_detail.tickets.filter(Q(ticket_status=0)|Q(ticket_status=3)).filter(is_invoiced=True) or pnr_detail.others_fees.filter(Q(other_fee_status=0)|Q(other_fee_status=3)).filter(is_invoiced=True):
                pnr_detail.is_invoiced = True
                pnr_detail.save()
            else:
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
    maximum_timezone = "2023-01-01 01:00:00.000000+03:00"
    
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the PnrNumber from the POST data
        value = request.POST.get('PnrNumber', None)
        
        value_length = len(value)
        
        # Check if the value is not None
        if value is not None:
            try:
                # If the value length is 6, search for a Pnr with this number
                if value_length == 6:
                    pnr = Pnr.objects.filter(number=value,
                                             system_creation_date__gt=maximum_timezone).first()
                    
                    context['pnr_id'] = pnr.id if pnr else []
                
                # Determine if the value length and characteristics match the criteria
                # -R means refund : to make ability to search refund
                if (value_length >= 13 and value.isdigit()) or value_length == 16 or (value_length >= 13 and '-R' in value):
                    # Search for a Ticket with this number
                    ticket = Ticket.objects.filter(
                        number__icontains=value,
                        ticket_status=1,
                        pnr__system_creation_date__gt=maximum_timezone
                    ).first()
                    
                    # Print the ticket for debugging
                    print("TICKET => ", ticket)
                    
                    if ticket:
                        context['pnr_id'] = ticket.pnr.id
                    else:
                        # If no ticket is found, search for an OthersFee with this designation
                        other_fee = OthersFee.objects.filter(
                            designation__icontains=value, 
                            other_fee_status=1,
                            pnr__system_creation_date__gt=maximum_timezone
                        ).first()
                        
                        # Print the other fee for debugging
                        print("OTHER FEE => ", other_fee)
                        
                        context['pnr_id'] = other_fee.pnr.id if other_fee else []
                else:
                    # If the value length doesn't match the criteria, set pnr_id to an empty list
                    context['pnr_id'] = []
            except Exception as e:
                # Log the exception for debugging purposes
                print(f"Error occurred: {e}")
                context['pnr_id'] = []
        else:
            # If value is None, set pnr_id to an empty list
            context['pnr_id'] = []
    
    # Return the context as a JSON response
    return JsonResponse(context)

# @login_required(login_url='index')
def reduce_fee_request_accepted(request, request_id, amount, choice_type, token):
    from AmadeusDecoder.utilities.ServiceFeesDecreaseRequest import ServiceFeesDecreaseRequest
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
    from AmadeusDecoder.utilities.ServiceFeesDecreaseRequest import ServiceFeesDecreaseRequest
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
    from AmadeusDecoder.utilities.ServiceFeesDecreaseRequest import ServiceFeesDecreaseRequest
    context = {}
    if request.method == 'POST' and request.POST.get('pnrId') and request.POST.get('feeId'):
        pnrId = request.POST.get('pnrId')
        feeId = request.POST.get('feeId')
        feeAmount = request.POST.get('feeAmount')
        feeOriginAmount = request.POST.get('feeOriginAmount')
        choiceType = request.POST.get('choiceType')
        motif = request.POST.get('motif')
        userId = request.POST.get('userId')

        # Code à vérifier car changement radical dans le processus de demande de diminution de frais de service
        if pnrId is not None and feeId is not None:
            reduce_fee_request_ongoing = ReducePnrFeeRequest.objects.filter(pnr=pnrId, fee=feeId, status=0).last()
            print(reduce_fee_request_ongoing)
            if reduce_fee_request_ongoing is not None:
                fee_amount = round(reduce_fee_request_ongoing.amount, 2)
                fee_origin = round(reduce_fee_request_ongoing.origin_amount, 2)
                date_creation = reduce_fee_request_ongoing.system_creation_date
                user = reduce_fee_request_ongoing.user.username

                context['status'] = 3
                context['fee_amount'] = fee_amount
                context['fee_origin'] = fee_origin
                context['user'] = user
                context['date_creation'] = date_creation
            else:
                try :
                    # subject, message = ServiceFeesDecreaseRequest().inquiry_formatting(choiceType, request, feeId, pnrId, feeOriginAmount, feeAmount, motif)
                    #  Accepter directement la demande
                    pnr = Pnr.objects.get(pk=pnrId)
                    fee = Fee.objects.get(pk = feeId)
                    user = User.objects.get(pk=userId)
                    
                    # get current total
                    initial_total = 0
                    invoice_detail_obj = InvoiceDetails().get_invoice_detail_by_pnr(pnr)
                    initial_total = invoice_detail_obj.total
                    
                    
                    if choiceType == 'one':
                        reduce_fee_request = ReducePnrFeeRequest(pnr=pnr,fee=fee,status=1,origin_amount=feeOriginAmount,amount=feeAmount,motif=motif,user=user)
                        reduce_fee_request.save()
                        fee.cost = feeAmount
                        fee.total = feeAmount
                        fee.save()
                        # save fee update history
                        History().fee_history(fee, user, feeOriginAmount, feeAmount, initial_total)

                    elif choiceType == 'all':
                        all_ticket_related_fees = Fee.objects.filter(pnr__id=fee.pnr.id, is_invoiced=False).all()
                        for temp_related_ticket in all_ticket_related_fees:
                            reduce_fee_request = ReducePnrFeeRequest(pnr=pnr,fee=temp_related_ticket,status=1,origin_amount=temp_related_ticket.cost,amount=feeAmount,motif=motif,user=user)
                            reduce_fee_request.save()
                            # save fee update history
                            History().fee_history(temp_related_ticket, user, temp_related_ticket.cost, feeAmount, initial_total)
                            temp_related_ticket.cost = feeAmount
                            temp_related_ticket.total = feeAmount
                            temp_related_ticket.save()
                    

                    context['status'] = 1 
                    context['message'] = "Demande acceptée avec succès."
                    
                    # Sending.send_email_request(
                    #     FEE_REQUEST_SENDER['address'],
                    #     FEE_REQUEST_RECIPIENT,
                    #     subject,
                    #     message
                    # )
                except Exception as e :
                    context['status'] = 0
                    context['message'] = "ERREUR: %s " % str(e)
        else:
            context['status'] = 0
            context['message'] = "ERREUR: Impossible d'envoyer la demande."

    else :
        context['status'] = 0
        context['message'] = "ERREUR: Impossible d'envoyer la demande."
    
    return JsonResponse(context)

@login_required(login_url='index')
def save_pnr_detail_modification(request, pnr_id):
    context = {}
    context['ticket_status'] = ''
    context['other_fee_status'] = ''
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
                passenger_invoice = PassengerInvoice.objects.filter(pnr=pnr)


                if pnr.status_value == 0:
                    print('Entry issuing part')
                    if passenger_invoice.filter(status='sale').exists():
                        print('Enty to issuing first part with : ' + str(ticket_checked))
                        for ids in ticket_checked:
                            tickets = Ticket.objects.filter(pk=int(ids), pnr=pnr_id, ticket_status=1).exclude(ticket_type='TST')
                            for ticket in tickets:
                                try:
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
                                                else:
                                                    invoice_fee_passenger.filter(is_invoiced=False).update(
                                                        fee=fee_item, pnr=pnr, client=customer, type=fee_item.type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, status='sale')
                                        context['ticket_status'] = 'success'
                                    else:
                                        context['ticket_status'] = 'failed'
                                        break
                                except:
                                    context['ticket_status'] = 'failed'
                                    break

                    elif not passenger_invoice.filter(status='sale').exists():
                        print('Enty to issuing second part with : ' + str(ticket_checked))
                        for ids in ticket_checked:
                            tickets = Ticket.objects.filter(pk=int(ids), pnr=int(pnr_id), ticket_status=1).exclude(ticket_type='TST')
                            for ticket in tickets:
                                try:
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
                                                else:
                                                    invoice_fee_passenger.filter(is_invoiced=False).update(fee=fee_item, pnr=pnr, client=customer, type=fee_item.type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, status='sale')
                                        context['ticket_status'] = 'success'
                                    else:
                                        context['ticket_status'] = 'failed'
                                        break
                                except:
                                    context['ticket_status'] = 'failed'
                                    break

                elif pnr.status_value == 1:
                    print('Enty to unissuing first part with : ' + str(ticket_checked))
                    ticket_objects = Ticket.objects.filter(pk__in=ticket_checked, pnr=int(pnr_id), ticket_status=1).exclude(ticket_type__in=['TKT', 'EMD'])
                    print('Unissuing ticket: ' + str(ticket_objects.count()))
                    if ticket_objects.exists():
                        for ticket_object in ticket_objects:
                            try:
                                invoice_tickets_passenger = PassengerInvoice.objects.filter(ticket=ticket_object.id, pnr=int(pnr_id))
                                if invoice_tickets_passenger.exists():
                                    invoice_tickets_passenger.update(ticket=ticket_object, pnr=pnr, type=ticket_object.ticket_type, client=customer, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, fee=None, status='quotation', other_fee=None)
                                    print('ticket unissued updated')
                                else:
                                    invoice_tickets_passenger = PassengerInvoice(ticket=ticket_object, pnr=pnr, type=ticket_object.ticket_type, client=customer, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, fee=None, status='quotation', other_fee=None)
                                    invoice_tickets_passenger.save()
                                    print('ticket unissued saved')

                                fee_objects = Fee.objects.filter(ticket=int(ticket_object.id))
                                if fee_objects.exists():
                                    for fee_item in fee_objects:
                                        invoice_fee_passenger = PassengerInvoice.objects.filter(fee=fee_item.id, pnr=int(pnr_id))
                                        if invoice_fee_passenger.exists():
                                            invoice_fee_passenger.update(fee=fee_item, pnr=pnr, client=customer, type=fee_item.type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, status='quotation', other_fee=None)
                                            print('fee unissued updated')
                                        else:
                                            invoice_fee_passenger = PassengerInvoice(fee=fee_item, pnr=pnr, client=customer, type=fee_item.type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, status='quotation', other_fee=None)
                                            invoice_fee_passenger.save()
                                            print('fee unissued saved')
                                context['ticket_status'] = 'success'
                            except:
                                context['ticket_status'] = 'failed'
                                break
                
                pnr.customer_id = customer.id
                pnr.save()

            if pnr.type == 'EWA' and pnr.status_value == 1:
                if customer_id != '':
                    invoice_ewa = Invoice.objects.filter(pnr=pnr_id)
                    customer = Client.objects.get(pk=int(customer_id))
                    if invoice_ewa.exists():
                        try:
                            invoice_ewa_detail = invoice_ewa.first()
                            passenger_invoice = PassengerInvoice.objects.filter(pnr=int(pnr_id), status='quotation', invoice_id = invoice_ewa_detail)
                            print('EWA saved')
                            if not passenger_invoice.exists():
                                passenger_invoice = PassengerInvoice(ticket=None, pnr=pnr, type='Billet', client=customer, user_follower=user, is_checked=True, fee=None, status='quotation',invoice_id = invoice_ewa_detail, other_fee=None)
                                passenger_invoice.save()
                            else:
                                passenger_invoice.update(ticket=None, pnr=pnr, type='Billet', client=customer, user_follower=user, is_checked=True, fee=None, status='quotation',invoice_id = invoice_ewa_detail, other_fee=None)

                            pnr.customer_id = customer.id
                            pnr.save()
                            context['ticket_status'] = 'success'
                        except:
                            context['ticket_status'] = 'failed'

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
                            try:
                                invoice_fee_passenger = PassengerInvoice.objects.filter(fee=other_fees_item.id, pnr=int(pnr_id))
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
                                        else:
                                            invoice_fee_passenger.filter(is_invoiced=False).update(fee=fee_item, pnr=pnr, client=customer, type=fee_item.type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, other_fee=None, status='sale')
                                    context['ticket_status'] = 'success'
                                elif invoice_fee_passenger.exists():
                                    context['ticket_status'] = 'failed'
                                    break
                            except:
                                context['other_fee_status'] = 'failed'
                                break

                elif pnr.status_value == 1:
                    print('Unissuing other_fees')
                    other_fees = OthersFee.objects.filter(pnr=pnr_id, other_fee_status=1)
                    for other_fees_item in other_fees:
                        try:
                            invoice_fee_passenger = PassengerInvoice.objects.filter(fee=other_fees_item.id, pnr=int(pnr_id))
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
                                    else:
                                        invoice_fee_passenger.filter(is_invoiced=False).update(fee=fee_item, pnr=pnr, client=customer, type=fee_item.type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, other_fee=None, status='quotation')
                            elif invoice_fee_passenger.exists() and pnr.type == 'EWA':
                                invoice_fee_passenger.filter(is_invoiced=False).update(fee=None, pnr=pnr, client=customer, type=other_fees_item.fee_type, reference=reference, user_follower=user, is_checked=True, is_invoiced=False, ticket=None, other_fee=other_fees_item, status='quotation')
                            context['ticket_status'] = 'success'
                        except:
                            context['other_fee_status'] = 'failed'
                            break

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
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) #get the parent folder of the current file
    config = Configuration.objects.filter(name='Saving File Tools', value_name='File protocol', environment=settings.ENVIRONMENT)

    
    file_dir = '/opt/odoo/issoufali-addons/import_saleorder/data/source'
    customer_dir = '/opt/odoo/issoufali-addons/contacts_from_incadea/data/source'
    
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

        print("Customers checked are: " + str(customer_ids))
        for customer_id in customer_ids:
            "update the line of order of the current PNR to state invoiced"
            orders = PassengerInvoice.objects.filter(pnr=pnr_id, client=customer_id, is_invoiced=False)
            order_invoice_number = datetime.now().strftime('%Y%m%d%H%M') + str(random.randint(1,9)) # SET ORDER NUMBER
            for order in orders:
                segments_parts = []
                if order.status == 'sale' and order.is_invoiced == False:
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
                                # print("DEBUGGING SEGMENT PART")
                                # print(part)
                                # print(part.segment)
                                if part.segment and part.segment.segment_type is not None and part.segment.segment_type == 'Flight':
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
                
            customer = Client.objects.get(pk=int(customer_id))
            csv_customer_lines.append({
                'id': customer.id,
                'CT_Num': customer.ct_num.strip().replace('\n', '') if customer.ct_num is not None else '',
                'CT_Intitule': customer.intitule.strip().replace('\n', '') if customer.intitule is not None else '',
                'CT_Adresse': customer.address_1.strip().replace('\n', '') if customer.address_1 is not None else '',
                'CT_Type': customer.ct_type,
                'CT_Ville': customer.city.strip().replace('\n', '') if customer.city is not None else '',
                'CT_Classement': customer.classment.strip().replace('\n', '') if customer.classment is not None else '',
                'CT_Contact': customer.contact.strip().replace('\n', '') if customer.contact is not None else '',
                'CT_Complement': customer.complement.strip().replace('\n', '') if customer.complement is not None else '',
                'CT_CodePostal': customer.code_postal.strip().replace('\n', '') if customer.code_postal is not None else '',
                'CT_Telephone': customer.telephone.strip().replace('\n', '') if customer.telephone is not None else '',
                'CT_Email': customer.email.strip().replace('\n', '') if customer.email is not None else '',
                'CT_Site': customer.site.strip().replace('\n', '') if customer.site is not None else '',
                'CT_Pays': customer.country.strip().replace('\n', '') if customer.country is not None else ''
            })

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
            if config.exists() and config.first().single_value == 'Local':
                odoo_link = config.first().dict_value.get('link')
                print("------------------Call Odoo import-----------------------")
                response = requests.get(odoo_link)
                print(response.content)

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
    config = Configuration.objects.filter(name='File saving configuration', value_name='Saving protocol', environment=settings.ENVIRONMENT)

    file_dir = '/opt/odoo/issoufali-addons/import_saleorder/data/source'
    customer_dir = '/opt/odoo/issoufali-addons/contacts_from_incadea/data/source'
    
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
                            if part.segment and part.segment.segment_type is not None and part.segment.segment_type == 'Flight':
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

        customer = Client.objects.get(pk=int(customer_object))
        csv_customer_lines.append({
            'id': customer.id,
            'CT_Num': customer.ct_num.strip().replace('\n', '') if customer.ct_num is not None else '',
            'CT_Intitule': customer.intitule.strip().replace('\n', '') if customer.intitule is not None else '',
            'CT_Adresse': customer.address_1.strip().replace('\n', '') if customer.address_1 is not None else '',
            'CT_Type': customer.ct_type,
            'CT_Ville': customer.city.strip().replace('\n', '') if customer.city is not None else '',
            'CT_Classement': customer.classment.strip().replace('\n', '') if customer.classment is not None else '',
            'CT_Contact': customer.contact.strip().replace('\n', '') if customer.contact is not None else '',
            'CT_Complement': customer.complement.strip().replace('\n', '') if customer.complement is not None else '',
            'CT_CodePostal': customer.code_postal.strip().replace('\n', '') if customer.code_postal is not None else '',
            'CT_Telephone': customer.telephone.strip().replace('\n', '') if customer.telephone is not None else '',
            'CT_Email': customer.email.strip().replace('\n', '') if customer.email is not None else '',
            'CT_Site': customer.site.strip().replace('\n', '') if customer.site is not None else '',
            'CT_Pays': customer.country.strip().replace('\n', '') if customer.country is not None else ''
        })

        quotation_df = pd.concat([quotation_df, pd.DataFrame(csv_quotation_lines)])
        customer_df = pd.concat([customer_df, pd.DataFrame(csv_customer_lines)])

        if not quotation_df.empty and not customer_df.empty:
            quotation_file = os.path.join(file_dir, 'FormatsSaleOrderExportOdoo{}.csv'.format(today))
            customer_file = os.path.join(customer_dir, 'CustomerExport{}.csv'.format(today))
            quotation_df.to_csv(quotation_file, index=False, sep=';')
            customer_df.to_csv(customer_file, index=False, sep=';')
            if config.exists() and config.first().single_value == 'FTP':
                hostname, port, password, username, order_repository, customer_repository, odoo_link = config.first().dict_value.get('hostname'), int(config.first().dict_value.get('port')), config.first().dict_value.get('password'), config.first().dict_value.get('username'), config.first().dict_value.get('repository') + '/Order/', config.first().dict_value.get('repository') + '/Customer/', config.first().dict_value.get('link')
                upload_file(quotation_file, order_repository, 'FormatsSaleOrderExportOdoo{}.csv'.format(today), username, password, hostname, port)
                upload_file(customer_file, customer_repository, 'CustomerExport{}.csv'.format(today), username, password, hostname, port)
                print("------------------Call Odoo import-----------------------")
                response = requests.get(odoo_link)
            if config.exists() and config.first().single_value == 'Local':
                odoo_link = config.first().dict_value.get('link')
                print("------------------Call Odoo import-----------------------")
                response = requests.get(odoo_link)
        

    return JsonResponse(context)

@login_required(login_url='index')
def import_product(request, pnr_id):
    if request.method == 'POST':
        emitter = User.objects.get(pk=request.user.id)
        if 'listNewProduct' in request.POST:
            product = json.loads(request.POST.get('listNewProduct'))
            pnr = Pnr.objects.get(pk=int(pnr_id))
            
            if product[0] == '19':
                if float(product[3]) > 0:
                    product[3] = -abs(product[3])
                    
                other_fees = OthersFee(designation=product[7], cost=product[3], total=product[4],
                                        pnr=pnr, fee_type=product[1],reference=product[6], 
                                        quantity=1, is_subjected_to_fee=False, creation_date=datetime.now(), emitter=emitter)
                other_fees.save()
                
                for segment in product[9]:
                    segment = PnrAirSegments.objects.get(pk=segment.get('value'))
                    passenger = Passenger.objects.get(pk=product[8])
                    passenger_segment = OtherFeeSegment(segment=segment,other_fee= other_fees, passenger=passenger)
                    passenger_segment.save()
            
            else:
                other_fees = OthersFee.objects.filter(pnr=pnr_id, product_id=product[0])
                other_fees = OthersFee(designation=product[2], cost=product[3], tax=product[4], total=product[5],
                                        pnr=pnr, fee_type=product[1], passenger_segment=product[6], reference=product[7], emitter=emitter,
                                        quantity=1, is_subjected_to_fee=False, creation_date=datetime.now())
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

# Define a function that requires a login to access
@login_required(login_url='index')
def search_client_by_intitule(request):
    # Get the search term from the request POST data or set it to an empty string if not present
    term = request.POST.get('term', '')
    # If the search term is empty, return an empty JSON response
    if not term:
        return JsonResponse([], safe=False)
    # Filter the Client objects that have an 'intitule' field containing the search term,
    # then select only the 'id' and 'intitule' fields to optimize performance
    clients = Client.objects.filter(intitule__icontains=term).values('id', 'intitule')
    # Convert the filtered QuerySet into a list
    client_list = list(clients)
    # Return the filtered list as a JSON response with the 'safe' argument set to False to allow serializing lists
    return JsonResponse(client_list, safe=False)

@login_required(login_url='index')
def get_all_countries(request):
    if request.method == 'GET':
        countries = configs.COUTRIES_DATA
        country_list = list(countries)
        
        return JsonResponse(country_list, safe=False)
    
@login_required(login_url='index')
def get_all_departments(request):
    if request.method == 'GET':
        departments = configs.DEPARTMENTS_FRANCE
        department_list = list(departments)
        
        return JsonResponse(department_list, safe=False)
    # if request.method == 'POST':
    #     nom_departement = request.POST.get('nom_departement')
    #     if nom_departement:
    #         departments = configs.DEPARTMENTS_FRANCE.filter(nom=nom_departement)
    #         print(departments)
    #         department_list = list(departments)
            
    #         return JsonResponse(department_list, safe=False)

@login_required(login_url='index')
def get_all_municipalities(request):
    if request.method == 'POST':
        code_departement = request.POST.get('code_departement')
        nom_departement = request.POST.get('nom_departement')
        if code_departement:
            municipalities  =   configs.MUNICIPALITIES_FRANCE.filter(
                                    code_departement=code_departement
                                )
            municipality_list = list(municipalities)
            
            return JsonResponse(municipality_list, safe=False)
        if nom_departement:
            municipalities  =   configs.MUNICIPALITIES_FRANCE.filter(
                                    nom=nom_departement
                                )
            municipality_list = list(municipalities)
            
            return JsonResponse(municipality_list, safe=False)
        return JsonResponse([], safe=False)
    
@login_required(login_url="index")
def get_all_products(request):
    if request.method == 'GET':
        product_designation_list = []
        product_objects = Product.objects.all()

        if product_objects.exists():
            for product in product_objects:
                product_designation_list.append(product.designation)
            return JsonResponse({"product_designation_list": product_designation_list}, safe=False)

        return JsonResponse([], safe=False)
    
@login_required(login_url="index")
def remove_other_fee_service(request):
    if request.method == 'POST':
        other_fee_id = request.POST.get('other_fee_id')
        other_fee = OthersFee.objects.filter(id=other_fee_id).first()

        if other_fee:
            other_fee.delete()
            context = {
                'status': 'deleted',
                'designation': other_fee.designation,
                'total': other_fee.total
            }
            return JsonResponse(context, safe=False)

        return JsonResponse({'status': 'not_found'})

# décommander  un PNR
@login_required(login_url="index")
def unorder_pnr(request):
    if request.method == 'POST':
        pnr_number = request.POST.get('pnr_number')
        invoice_number = request.POST.get('invoice_number')
        motif = request.POST.get('motif')
        user_id = request.POST.get('user_id')
        
        if motif is None:
            return JsonResponse({'message': 'Veuillez ajouter un motif'})

        
        pnr = Pnr.objects.get(number=pnr_number)
        passenger_invoices = PassengerInvoice.objects.filter(pnr_id=pnr.id, invoice_number=invoice_number).all()
        
        if passenger_invoices:
            for passenger_invoice in passenger_invoices:
                # delete the corresponding passenger invoice if it exist
                PassengerInvoice.objects.filter(id=passenger_invoice.id).delete()
                
                if passenger_invoice.ticket_id:
                    #  delete the corresponding ticket if it exist
                    Ticket.objects.filter(id=passenger_invoice.ticket_id).update(is_invoiced=False)
                
                if passenger_invoice.fee_id:
                    #  delete the corresponding fee if it exist
                    Fee.objects.filter(id=passenger_invoice.fee_id).update(is_invoiced=False)
                    
                if passenger_invoice.other_fee_id:
                    # delete the corresponding other fee if it exist
                    OthersFee.objects.filter(id=passenger_invoice.other_fee_id).update(is_invoiced=False)

                if passenger_invoice.ticket_id or passenger_invoice.other_fee_id or passenger_invoice.fee_id:
                    # save in the InvoicesCanceled
                    invoices_canceled = InvoicesCanceled(pnr_id=pnr.id,invoice_number=invoice_number,motif=motif,ticket_id=passenger_invoice.ticket_id, other_fee_id = passenger_invoice.other_fee_id,user_id=user_id, fee_id=passenger_invoice.fee_id) 
                    invoices_canceled.save()
                
        
        return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'error'})

@login_required(login_url="index")
# cancel order in passeger invoice
def uncheck_ticket_in_passenger_invoiced(request):
    if request.method == 'POST':
        pnr_number = request.POST.get('pnr_id')

        if pnr_number:
            passenger_invoice_obj = PassengerInvoice.objects.filter(pnr_id=pnr_number).exclude(is_invoiced=True)
        
            if passenger_invoice_obj:
                for passenger_invoice in passenger_invoice_obj:
                    # delete the corresponding passenger invoice if it exist
                    PassengerInvoice.objects.filter(id=passenger_invoice.id).delete()
                    
                    if passenger_invoice.ticket_id:
                        #  delete the corresponding ticket if it exist
                        Ticket.objects.filter(id=passenger_invoice.ticket_id).update(is_invoiced=False)
                    
                    if passenger_invoice.fee_id:
                        #  delete the corresponding fee if it exist
                        Fee.objects.filter(id=passenger_invoice.fee_id).update(is_invoiced=False)
                        
                    if passenger_invoice.other_fee_id:
                        # delete the corresponding other fee if it exist
                        OthersFee.objects.filter(id=passenger_invoice.other_fee_id).update(is_invoiced=False)
        
        return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'error'})
    
@login_required(login_url="index")
def get_all_pnr_unordered(request):
    context = {}
    invoices_canceled_list = InvoicesCanceled.objects.all().distinct('pnr_id')
    
    pnr_count = invoices_canceled_list.count()
    
    context['pnr_list'] = invoices_canceled_list
    object_list = context['pnr_list']
    row_num = request.GET.get('paginate_by', 20) or 20
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, row_num)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger: 
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {'page_obj': page_obj, 'row_num': row_num, 'pnr_count' : pnr_count}
    
    return render(request,'unordered_pnr.html', context)

@login_required(login_url="index")
def unordered_pnr_research(request):
    context = {}
    
    if request.method == 'POST' and request.POST.get('pnr_research'):
        search_results = []
        
        pnr_research = request.POST.get('pnr_research')
        pnr_results = InvoicesCanceled.objects.all().filter(Q(invoice_number__icontains=pnr_research) | Q(pnr__id__icontains=pnr_research)| Q(motif__icontains=pnr_research) | Q(pnr__number__icontains=pnr_research)).distinct('pnr_id')
        
        if pnr_results.exists():
            for p1 in pnr_results :
                search_results.append(p1)
        print(search_results)
        
        _passengers = Passenger.objects.all().filter(Q(name__icontains=pnr_research) | Q(surname__icontains=pnr_research) )
        
        for p in _passengers :
            
            pnr_passenger = PnrPassenger.objects.all().filter(passenger=p).first()
            if pnr_passenger is not None :
                pnr_object = InvoicesCanceled.objects.all().filter(pnr_id=pnr_passenger.pnr.pk).distinct()
                
                if pnr_object.exists() and pnr_object not in search_results and pnr_object is not None :
                    search_results.extend(pnr_object)
        print(search_results)
        
        # Search with customer
        _customers = Client.objects.all().filter(Q(intitule__icontains=pnr_research) )
        
        for c in _customers :
            pnr_passenger_invoice = PassengerInvoice.objects.all().filter(client=c).first()
            if pnr_passenger_invoice is not None :
                pnr_cobject = InvoicesCanceled.objects.all().filter(pnr_id=pnr_passenger_invoice.pnr.pk).distinct()
                
                if pnr_cobject.exists() and pnr_cobject not in search_results and pnr_cobject is not None :
                    search_results.extend(pnr_cobject)
                
        _users = User.objects.all().filter(Q(username__icontains=pnr_research))        
        for user in _users:
            pnr_invoices = InvoicesCanceled.objects.all().filter(user_id=user.pk).distinct()
            
            if pnr_invoices.exists() and pnr_invoices not in search_results and pnr_invoices is not None :
                search_results.extend(pnr_invoices)
                    
        print(search_results)
        
        results = []
        for invoice in search_results:
            
            values = {}
            values['pnr_id'] = invoice.pnr.id
            values['pnr_number'] = invoice.pnr.number
            values['invoice_number'] = invoice.invoice_number
            values['motif'] = invoice.motif
            values['date'] = invoice.date
            values['user'] = invoice.user.username
            results.append(values)
        pnr_count = len(results)
        
        context = {'results' : results, 'pnr_count' :  pnr_count}
    return JsonResponse(context)
        
def liste_commandes(request):
    return render(request,'commandes_modal.html') 

# Supprimer les tickets non commandés
def ticket_delete(request):
    if request.method == 'POST':
        ticketId = request.POST.get('ticketId')
        ticketTable = request.POST.get('ticketTable')
        ticketNumber = request.POST.get('ticketNumber')

        print('------------------------------------------------------')
        print(ticketId)
        
        # for ticket
        if ticketTable == 'ticket':
            ticket = Ticket.objects.get(pk=ticketId)
            ticket.ticket_status = 0
            ticket.save()

            # Verify in PassengerInvoice
            passengers_invoice = PassengerInvoice.objects.filter(ticket_id = ticketId)
            # delete the corresponding passenger invoice
            if passengers_invoice is not None:
                for passenger_invoice in passengers_invoice:
                    print('PASSENGER INVOICE VAR')
                    passenger_invoice.delete()
                
            # get the corresponding fee
            fees = Fee.objects.filter(ticket_id=ticketId)
            # delete the corresponding passenger invoice
            if fees is not None:
                for fee in fees:
                    print('FEE VAR')
                    passenger_invoice_fee = PassengerInvoice.objects.filter(fee_id=fee.id)
                    passenger_invoice_fee.delete()


        # for other fees
        else:
            other_fee = OthersFee.objects.get(pk=ticketId)
            other_fee.other_fee_status = 0
            other_fee.save()

            passengers_invoice = PassengerInvoice.objects.filter(other_fee_id=ticketId)
            if passengers_invoice is not None:
                for passenger_invoice in passengers_invoice:
                    # delete the corresponding passenger invoice
                    passenger_invoice.delete()

            # get its corresponding fee
            fees = Fee.objects.filter(other_fee_id=ticketId)
            if fees is not None:
                for fee in fees:
                    # delete its corresponding passenger invoice
                    print('FEE VAR')
                    passenger_invoice_fee = PassengerInvoice.objects.filter(fee_id=fee.id)
                    passenger_invoice_fee.delete()


        return JsonResponse({'status':'ok'})
