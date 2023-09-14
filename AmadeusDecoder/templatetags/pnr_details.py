'''
Created on 29 Sep 2022

@author: Famenontsoa
'''
from datetime import datetime, timezone
from django import template
from django.db.models import Q
import json
import traceback

import AmadeusDecoder.utilities.configuration_data as configs

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.models.user.Users import Office
from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
from AmadeusDecoder.models.invoice.Ticket import Ticket

register = template.Library()

AIRPORT_AGENCY_CODE = configs.AIRPORT_AGENCY_CODE

@register.filter(name='get_all_username')
def get_all_username(_userId):
    user_obj = User.objects.all()
    return json.dumps([{"id": user.id, "username": user.username} for user in user_obj])

@register.filter(name='ticket_datetime_invoice_created')
def get_ticket_datetime_invoice_created(pnr_id, ticket_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    passenger_invoices = PassengerInvoice.objects.filter(pnr_id=pnr_id, ticket_id=ticket_id).exclude(status='quotation')
    if passenger_invoices.exists():
        for passenger_invoice in passenger_invoices:
            if passenger_invoice.is_invoiced:
                return passenger_invoice.date_creation
    else:
        return None
    
@register.filter(name='fee_datetime_invoice_created')
def get_fee_datetime_invoice_created(pnr_id, fee_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    passenger_invoices = PassengerInvoice.objects.filter(pnr_id=pnr_id, fee_id=fee_id).exclude(status='quotation')
    if passenger_invoices.exists():
        for passenger_invoice in passenger_invoices:
            if passenger_invoice.is_invoiced:
                return passenger_invoice.date_creation
    else:
        return None
    
@register.filter(name='other_fee_datetime_invoice_created')
def get_fee_datetime_invoice_created(pnr_id, other_fee):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    passenger_invoices = PassengerInvoice.objects.filter(pnr_id=pnr_id, other_fee=other_fee).exclude(status='quotation')
    if passenger_invoices.exists():
        for passenger_invoice in passenger_invoices:
            if passenger_invoice.is_invoiced:
                return passenger_invoice.date_creation
    else:
        return None

@register.filter(name='opc')
def get_min_opc(pnr):
    try:
        return pnr.get_min_opc()
    except:
        return ''
    
@register.filter(name='ssrs')
def get_all_pnr_ssrs(pnr):
    from AmadeusDecoder.models.pnrelements.SpecialServiceRequestBase import SpecialServiceRequestBase
    try:
        all_pnr_related_ssrs = SpecialServiceRequestBase.objects.filter(pnr_id=pnr.id).all().order_by('id')
        return all_pnr_related_ssrs
    except:
        return []

@register.filter(name='ssr_description')
def get_ssr_description(ssr_base):
    from AmadeusDecoder.models.pnrelements.SpecialServiceRequestDescription import SpecialServiceRequestDescription
    try:
        ssr_description = SpecialServiceRequestDescription.objects.filter(ssr_id=ssr_base.ssr_id, lang='fr').first()
        return ssr_description
    except:
        return ''

@register.filter(name='ticket_ssr_opc')
def get_opc(segment, ssr):
    from AmadeusDecoder.models.pnrelements.ConfirmationDeadline import ConfirmationDeadline
    confirmation_deadline = ConfirmationDeadline()
    if segment is not None:
        confirmation_deadline.segment = segment
    elif ssr is not None:
        confirmation_deadline.ssr = ssr
        
    try:
        return confirmation_deadline.get_confirmation_deadline().doc_date
    except:
        return ''
    
@register.filter(name='ssr_opc')
def get_ssr_opc(ssr):
    from AmadeusDecoder.models.pnrelements.ConfirmationDeadline import ConfirmationDeadline
    confirmation_deadline = ConfirmationDeadline()
    confirmation_deadline.ssr = ssr
    
    try:
        return confirmation_deadline.get_confirmation_deadline_ssr_modal().doc_date
    except:
        return ''
    
@register.filter(name='ssr_passenger_segment')
def get_ssr_passenger_segment(ssr_base):
    from AmadeusDecoder.models.pnrelements.SpecialServiceRequestBase import SpecialServiceRequestBase
    passengers = ''
    segments = ''
    ans = ''
    try:
        ssr_base = SpecialServiceRequestBase.objects.get(pk=ssr_base.id)
        for passenger in ssr_base.passengers.all().order_by('passenger__order'):
            passengers += passenger.passenger.order + '-'
        for segment in  ssr_base.segments.all().order_by('segment__segmentorder'):
            segments += segment.segment.segmentorder + '-'
        
        if passengers != '':
            ans += passengers[:-1]
        if segments != '':
            ans += '/' + segments[:-1]
        return ans
    except:
        return ''
    
@register.filter(name='auxiliary_segment')
def get_svc(pnr):
    from AmadeusDecoder.models.pnrelements.PnrAirSegments import PnrAirSegments
    try:
        svc_segments = PnrAirSegments.objects.filter(pnr__id=pnr.id, segment_type='SVC').all()
        if len(svc_segments) == 0:
            return False
        return svc_segments
    except:
        return False

@register.filter(name='pnr_remarks')
def get_all_pnr_remarks(pnr):
    from AmadeusDecoder.models.pnrelements.PnrRemark import PnrRemark
    try:
        remarks = PnrRemark().get_all_pnr_remark(pnr)
        if len(remarks) == 0:
            return False
        return remarks
    except:
        return False
    
@register.filter(name='ticket_issuing_date')
def get_issuing_date(pnr):
    try:
        return pnr.get_max_issuing_date()
    except:
        return None
    
@register.filter(name='pnr_emitter')
def get_pnr_emitter(pnr):
    try:
        return pnr.get_emit_agent()
    except:
        return None
    
@register.filter(name='pnr_office')
def get_pnr_office(pnr):
    try:   
        # Make agency name uniformised     
        agence_name_uniformised = ['GSA ISSOUFALI Dzaoudzi', 'GSA ISSOUFALI Jumbo Score', 'GSA ISSOUFALI Mamoudzou']
        if str(pnr.get_pnr_office()).strip() in agence_name_uniformised:
            return str(pnr.get_pnr_office()).strip().removeprefix("GSA ISSOUFALI")
        return pnr.get_pnr_office()
    except:
        return None
    
@register.filter(name='pnr_creator')
def get_pnr_creator(pnr):
    try:
        return pnr.get_creator_agent()
    except:
        return None
    
@register.filter(name='company_currency')
def get_company_currency(company_name):
    import AmadeusDecoder.utilities.configuration_data as configs
    try:
        return configs.COMPANY_CURRENCY_CODE
    except:
        return ''

@register.filter(name='pnr_count')
def get_all_pnr(request):
    pnr_count = 0

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
    
    try:
        filtered_creator = request.COOKIES.get('creator_pnr_filter')
        filtered_creator_cookie = None
        if str(json.loads(filtered_creator)[0]) == "0":
            filtered_creator_cookie = None
        elif str(json.loads(filtered_creator)[0]) == 'Empty':
            filtered_creator_cookie = 'Empty'
        else:
            filtered_creator_cookie = [int(user_id) for user_id in json.loads(filtered_creator)]
            
        # print(filtered_creator_cookie)
        # print(type(filtered_creator_cookie))
    except Exception as e:
        filtered_creator_cookie = None
        # print(f"Error on filter creator ${e}")

    # Retrieve the value of the "isSortedByCreator" cookie from the request
    is_sorter_by_creator = request.COOKIES.get('isSortedByCreator')

    # Initialize the sort_creator variable to a default value
    # Set order_by username ascendant
    sort_creator = None

    # Determine the value of "sort_creator" based on the value of the cookie
    if is_sorter_by_creator is not None:
        sort_creator = is_sorter_by_creator

    # print(sort_creator)
    
    agency_name_filter = request.COOKIES.get('agency_name_filter')
    
    agency_name = Q()
    if agency_name_filter and agency_name_filter != "0":
        agency_name = Q(agency_name__icontains=agency_name_filter) | Q(agency__name__icontains=agency_name_filter) if agency_name_filter else Q()
    elif agency_name_filter == "0":
        agency_name = Q(agency_name="", agent_code="", agency=None)
        
    # print(f"AGENCY NAME : {agency_name}")
    
    if request.user.id in [4, 5]: #==> [Farida et Mouniati peuvent voir chacun l'ensemble de leurs pnr]
        pnr_list = []
        pnr_count = 0
        issuing_users = request.user.copied_documents.all()

        # Create date filter query object or an empty query object if dates are absent
        date_filter = Q(system_creation_date__range=[start_date, end_date]) if start_date and end_date else Q()
        max_system_creation_date = Q(system_creation_date__gt=maximum_timezone)
        status_value = Q(status_value=status_value_from_cookie) if status_value_from_cookie in [0, 1] else Q()
        
        agent = Q()
        if filtered_creator_cookie == 'Empty':
            agent = Q(agent_id=None)
        elif filtered_creator_cookie is not None and filtered_creator_cookie != 'Empty':
            agent = Q(agent_id__in=filtered_creator_cookie)
        else:
            agent = Q(agent_id=4) | Q(agent_id=5)
        
        if is_invoiced is None:
            for issuing_user in issuing_users:
                pnr =   Pnr.objects.filter(
                            number=issuing_user.document, 
                        ).filter(
                            status_value,
                            date_filter,
                            max_system_creation_date,
                            agency_name,
                            agent
                        ).first()
                    
                if pnr not in pnr_list and pnr is not None:
                    pnr_list.append(pnr)

            pnr_obj =   Pnr.objects.filter(
                            status_value,
                        ).filter(
                            date_filter,
                            agent,
                            max_system_creation_date,
                            agency_name,
                            agent,
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
                            agency_name
                        ).filter(is_invoiced=is_invoiced).first()
                
                if pnr not in pnr_list and pnr is not None:
                    pnr_list.append(pnr)
                
            pnr_obj   = Pnr.objects.filter(
                            status_value,
                        ).filter( 
                            date_filter,
                            agent,
                            max_system_creation_date,
                            agency_name
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
        
        return pnr_count

    if request.user.role_id == 3:
        pnr_list = []
        pnr_count = 0
        issuing_users = request.user.copied_documents.all()

        status_value = Q(status_value=status_value_from_cookie) if status_value_from_cookie in [0, 1] else Q()
        is_invoiced = Q(is_invoiced=is_invoiced) if is_invoiced is not None else Q(is_invoiced=False)

        agent = Q()
        if filtered_creator_cookie == 'Empty':
            agent = Q(agent_id=None)
        elif filtered_creator_cookie is not None and filtered_creator_cookie != 'Empty':
            agent = Q(agent_id__in=filtered_creator_cookie)
        else:
            agent = Q(agent_id=request.user.id) | Q(agent_id=None)

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
                        max_system_creation_date,
                        agency_name,
                        agent,
                    ).first()

            # If Pnr is not already in the set and is not None, add it to the set and the list
            if pnr not in pnr_list and pnr is not None:
                pnr_list.append(pnr)

        print(f"PNR list without issuing users: {len(pnr_list)}")

        # Create date filter query object or an empty query object if dates are absent
        date_filter = Q(system_creation_date__range=[start_date, end_date]) if start_date and end_date else Q()

        max_system_creation_date = Q(system_creation_date__gt=maximum_timezone)
        
        # Get the Pnr objects matching criteria in the query, filtered by agent and date constraints
        pnr_obj =   Pnr.objects.filter(
                        date_filter,
                        agent,
                        max_system_creation_date,
                        status_value,
                        agency_name,
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


        return pnr_count
    else:
        status_value = Q(status_value=status_value_from_cookie) if status_value_from_cookie in [0, 1] else Q()
        
        pnr_list = []
        pnr_count = 0
        
        if filtered_creator_cookie is not None and filtered_creator_cookie != 'Empty': 
            max_system_creation_date = Q(system_creation_date__gt=maximum_timezone)

            # Create date filter query object or an empty query object if dates are absent
            date_filter = Q(system_creation_date__range=[start_date, end_date]) if start_date and end_date else Q()

            pnr_queryset  = Pnr.objects.filter(
                                Q(agent_id__in=filtered_creator_cookie)
                            ).filter(
                                status_value,
                                max_system_creation_date,
                                date_filter,
                                agency_name,
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
        elif filtered_creator_cookie is None : ##### Si 'Tout' est sélectionner dans le filtre créateur
            print('Creator selected is not non attribué and is all')
            if filtered_creator_cookie != 'Empty':
                max_system_creation_date = Q(system_creation_date__gt=maximum_timezone)

                # Create date filter query object or an empty query object if dates are absent
                date_filter = Q(system_creation_date__range=[start_date, end_date]) if start_date and end_date else Q()
            
                pnr_queryset =  Pnr.objects.filter(
                                    status_value,
                                    max_system_creation_date,
                                    date_filter,
                                    agency_name,
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

        elif filtered_creator_cookie == 'Empty':
            max_system_creation_date = Q(system_creation_date__gt=maximum_timezone)

            # Create date filter query object or an empty query object if dates are absent
            date_filter = Q(system_creation_date__range=[start_date, end_date]) if start_date and end_date else Q()

            pnr_queryset  = Pnr.objects.filter(
                                Q(agent_id=None),
                                status_value,
                                max_system_creation_date,
                                date_filter,
                                agency_name
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

            print('no creator')

        return pnr_count
@register.filter(name='first_passenger')
def get_first_passenger(pnr):
    from AmadeusDecoder.models.pnr.Passenger import Passenger
    try:
        passenger = Passenger.objects.filter(passenger__pnr=pnr).first()
        if passenger is not None:
            return passenger
        else:
            return ''
    except:
        return ''

@register.filter(name='passenger_segment_mail_missing')
def get_passenger_segment_missing(pnr):
    # from AmadeusDecoder.models.invoice.Ticket import Ticket
    tickets = pnr.tickets.filter(state=2).all()
    tickets_passenger_segment = []
    for ticket in tickets :
        res = ''
        try:
            if ticket.passenger.order is not None :
                res += ticket.passenger.order
            else :
                passengers = ''
                for ticket_passenger_tst in ticket.ticket_tst_parts.all():
                    passengers += ticket_passenger_tst.passenger.order + '-'
                res += passengers[:-1]
    
            segments = ''
            for passengerSegment in ticket.ticket_parts.all().order_by('segment__id'):
                segments += passengerSegment.segment.segmentorder + '-'
            for ssrs in  ticket.ticket_ssrs.all():
                segments += ssrs.ssr.order_line + '-'
    
            res += '/'
            res += segments[:-1]
    
            tickets_passenger_segment.append(res)
        except:
            traceback.print_exc()
    

    return " , ".join(tickets_passenger_segment)


@register.filter(name='get_next')
def get_next_pnr(pnr):
    from AmadeusDecoder.models.pnr.Pnr import Pnr
    next_pnr = Pnr.objects.filter(id__gt=pnr.id).order_by('id').first()

    return next_pnr  


@register.filter(name='get_prev')
def get_prev_pnr(pnr):
    from AmadeusDecoder.models.pnr.Pnr import Pnr
    previous_pnr= Pnr.objects.filter(id__lt=pnr.id).order_by('id').last()

    return previous_pnr  


@register.filter(name='get_order_customer')
def get_order_customer(pnr):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    order = PassengerInvoice.objects.filter(pnr=pnr.id, status="quotation")
    if order.exists() :
        return order
    else:
        return None

# Other fees: Ancillary/EWA/Passenger/Segment
# passenger
@register.filter(name='ancillary_passenger')
def get_ancillary_passenger(other_fee):
    try:
        temp_passenger = other_fee.related_segments.first().passenger
        if temp_passenger is not None:
            return other_fee.related_segments.first().passenger 
    except:
        return ''

# passenger/segment
@register.filter(name='ancillary_passenger_segment')
def get_ancillary_passenger_segment(other_fee):
    try:
        temp_passenger = get_ancillary_passenger(other_fee)
        temp_segment = other_fee.related_segments.first().segment
        if temp_passenger is not None and temp_segment is not None:
            return temp_passenger.order + '/' + temp_segment.segmentorder
    except:
        return ''



@register.filter(name='passenger_order_status')
def get_passenger_order_status(pnr):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    passenger_invoices = PassengerInvoice.objects.filter(pnr=pnr.id).exclude(ticket=None).exclude(status='quotation')
    if passenger_invoices.exists():
        return passenger_invoices
    else:
        return None

@register.filter(name='passenger_order_status_invoiced')
def get_passenger_order_status_invoiced(pnr, customer_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    passenger_invoices = PassengerInvoice.objects.filter(
                            pnr_id=pnr.id, 
                            client_id=customer_id
                        ).exclude(status='quotation')

    ticket_is_invoiced = []
    other_fee_is_invoiced = []

    if passenger_invoices.exists():
        for passenger in passenger_invoices:
            if passenger.other_fee is not None:
                other_fee_is_invoiced.append(passenger.is_invoiced)
            if passenger.ticket is not None:
                ticket_is_invoiced.append(passenger.is_invoiced)
        if False in ticket_is_invoiced or False in other_fee_is_invoiced:
            return False
        else:
            return True
    else:
        return None


"""
    Uses: Filter record(s) on PassengerInvoice of the current PNR that are quotation, and test if all of the lines are in status is_quotation, return True if it is otherwise return False
    Return value: (Boolean)
    Parameter: pnr id 
"""
@register.filter(name='ticket_quotation_status')
def get_ticket_quotation_status(pnr):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    tickets_quotation = PassengerInvoice.objects.filter(pnr=pnr.id).exclude(ticket=None).exclude(status='sale')
    is_quotation = []
    if tickets_quotation.exists():
        for ticket in tickets_quotation:
            is_quotation.append(ticket.is_quotation)
        print(is_quotation)
        if False in is_quotation:
            return False
        else:
            return True
    else:
        return None


@register.filter(name='order_with_quotation')
def get_order_with_quotation(pnr):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    ticket_quotation_line = PassengerInvoice.objects.filter(pnr=pnr.id, status='quotation', is_quotation=True)
    ticket_order_line = PassengerInvoice.objects.filter(pnr=pnr.id, status='sale')
    if ticket_order_line.exists() and ticket_quotation_line.exists():
        return True
    elif not ticket_order_line.exists() and ticket_quotation_line.exists():
        return False

    
@register.filter(name='passenger_is_invoiced_in_passenger_invoice')
def get_passenger_is_invoiced_in_passenger_invoice(pnr):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    passenger_invoices = PassengerInvoice.objects.filter(pnr=pnr.id).exclude(status="quotation")
    is_invoice = []

    if passenger_invoices.exists():
        for passenger in passenger_invoices:
            if passenger.ticket is not None and passenger.ticket.ticket_status == 1:
                is_invoice.append(passenger.is_invoiced)
            if passenger.other_fee is not None and passenger.other_fee.other_fee_status == 1:
                is_invoice.append(passenger.is_invoiced)
            if passenger.fee is not None and passenger.fee.ticket is not None and passenger.fee.ticket.ticket_status == 1:
                is_invoice.append(passenger.is_invoiced)
            if passenger.fee is not None and passenger.fee.other_fee is not None and passenger.fee.other_fee.other_fee_status == 1:
                is_invoice.append(passenger.is_invoiced)
        if False in is_invoice:
            return False
        else:
            return True
    else:
        return None

# @register.filter(name='detail_customer')
# def get_detail_customer(id):
#     from AmadeusDecoder.models.invoice.Clients import Client
#     customer = Client.objects.get(pk=int(id))
#     if customer is not None:
#         return customer
#     else:
#         return None

@register.filter(name='passenger_existence')
def get_passenger(passenger_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.invoice.Ticket import Ticket
    if passenger_id != '' and passenger_id is not None:
        ticket = Ticket.objects.filter(passenger=passenger_id, ticket_status=1)
        if ticket.exists():
            ticket_obj = ticket.first()
            passenger_invoice = PassengerInvoice.objects.filter(ticket=ticket_obj.id)
            if passenger_invoice.exists():
                return True
            else:
                return False
    else:
        return False

@register.filter(name='ticket_passenger_status')
def get_ticket_status(passenger_id):
    from AmadeusDecoder.models.invoice.Ticket import Ticket
    if passenger_id != '' and passenger_id is not None:
        ticket = Ticket.objects.filter(passenger=passenger_id)
        tickets = Ticket.objects.filter(passenger=passenger_id).filter(Q(ticket_status=0) | Q(ticket_status=3))
        
        if ticket.exists():
            if (ticket.count() == tickets.count()):
                return True
            else:
                return False
        
    else:
        return False


@register.filter(name='passenger_is_invoiced')
def get_passenger_is_invoiced(passenger_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.invoice.Ticket import Ticket
    if passenger_id != '' and passenger_id is not None:
        ticket = Ticket.objects.filter(passenger=passenger_id, ticket_status=1).exclude(ticket_type='TST')
        if ticket.exists():
            ticket_obj = ticket.first()
            passenger_invoice = PassengerInvoice.objects.filter(ticket=ticket_obj.id, is_invoiced=True)
            if passenger_invoice.exists():
                return True
            else:
                return False
    else:
        return False

@register.filter(name='passenger_is_quotation')
def get_passenger_is_quotation(passenger_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.invoice.Ticket import Ticket
    if passenger_id != '' and passenger_id is not None:
        ticket = Ticket.objects.filter(passenger=passenger_id, ticket_status=1, ticket_type='TST')
        if ticket.exists():
            ticket_obj = ticket.first()
            passenger_invoice = PassengerInvoice.objects.filter(ticket=ticket_obj.id, is_quotation=True)
            if passenger_invoice.exists():
                return True
            else:
                return False
    else:
        return False


@register.filter(name='order_for_confirmation')
def get_order_for_confirmation(passenger_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.invoice.Ticket import Ticket
    if passenger_id != '' and passenger_id is not None:
        ticket = Ticket.objects.filter(passenger=passenger_id, ticket_status=1)
        if ticket.exists():
            ticket_obj = ticket.first()
            passenger_invoice = PassengerInvoice.objects.filter(ticket=ticket_obj.id, is_invoiced=True)
            if passenger_invoice.exists():
                return True
            else:
                return False
    else:
        return False


@register.filter(name='other_fees_orders')
def get_other_fees_orders(other_fee):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    other_fees_orders = PassengerInvoice.objects.filter(other_fee=other_fee)
    if other_fees_orders.exists():
        return other_fees_orders.first()
    else:
        return None


@register.filter(name='other_fees_fees_orders')
def get_other_fees_fees_orders(fee):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    other_fees_fees_orders = PassengerInvoice.objects.filter(fee=fee)
    if other_fees_fees_orders.exists():
        return other_fees_fees_orders
    else:
        return None
    
@register.filter(name='passenger_informations')
def get_passenger_information(pnr):
    from AmadeusDecoder.models.pnr.Pnr import Pnr
    from AmadeusDecoder.models.pnr.PnrPassenger import PnrPassenger
    from AmadeusDecoder.models.pnr.Passenger import Passenger
    from AmadeusDecoder.models.pnr.Contact import Contact
    
    context = {}
    pnr_passengers = PnrPassenger.objects.filter(pnr=pnr.id)
    
    def get_passenger_info(pnr, context):
        context['name'] = pnr.passenger.name
        context['surname'] = pnr.passenger.surname
        contacts = Contact.objects.filter(pnr_id=pnr.pnr_id)
        emails = contacts.filter(contacttype='Email')
        phones = contacts.filter(contacttype='Phone')
        context['phone'] = [phone.value for phone in phones]
        context['email'] = [email.value for email in emails]
        return json.dumps(context)
    
    if pnr_passengers.exists():
        if len(pnr_passengers) > 0 and len(pnr_passengers) < 2:
            pnr = pnr_passengers.first()
            return get_passenger_info(pnr, context)
        else:
            for pnr in pnr_passengers:
                if pnr.passenger.order == 'P1':
                    if pnr.passenger.designation is not None:
                        if pnr.passenger.designation.upper() not in ['INF', 'BÉBÉ', 'CHD', 'ENFANT']:
                            return get_passenger_info(pnr, context)
                    else:
                        return get_passenger_info(pnr, context)
                if pnr.passenger.order == 'P2':
                    if pnr.passenger.designation is not None:
                        if pnr.passenger.designation.upper() not in ['INF', 'BÉBÉ', 'CHD', 'ENFANT']:
                            return get_passenger_info(pnr, context)
                        if pnr.passenger.designation.upper() not in ['INF', 'BÉBÉ']:
                            return get_passenger_info(pnr, context)
                    else:
                        return get_passenger_info(pnr, context)
                if pnr.passenger.order == 'P3':
                    if pnr.passenger.designation is not None:
                        if pnr.passenger.designation.upper() not in ['INF', 'BÉBÉ', 'CHD', 'ENFANT']:
                            return get_passenger_info(pnr, context)
                        if pnr.passenger.designation.upper() not in ['INF', 'BÉBÉ']:
                            return get_passenger_info(pnr, context)
                    else:
                        return get_passenger_info(pnr, context)
                if pnr.passenger.order == 'P4':
                    if pnr.passenger.designation is not None:
                        if pnr.passenger.designation.upper() not in ['INF', 'BÉBÉ', 'CHD', 'ENFANT']:
                            return get_passenger_info(pnr, context)
                        if pnr.passenger.designation.upper() not in ['INF', 'BÉBÉ']:
                            return get_passenger_info(pnr, context)
                    else:
                        return get_passenger_info(pnr, context)
                if pnr.passenger.order == 'P5':
                    if pnr.passenger.designation is not None:
                        if pnr.passenger.designation.upper() not in ['INF', 'BÉBÉ', 'CHD', 'ENFANT']:
                            return get_passenger_info(pnr, context)
                        if pnr.passenger.designation.upper() not in ['INF', 'BÉBÉ']:
                            return get_passenger_info(pnr, context)
                    else:
                        return get_passenger_info(pnr, context)
                if pnr.passenger.order == 'P6':
                    if pnr.passenger.designation is not None:
                        if pnr.passenger.designation.upper() not in ['INF', 'BÉBÉ', 'CHD', 'ENFANT']:
                            return get_passenger_info(pnr, context)
                        if pnr.passenger.designation.upper() not in ['INF', 'BÉBÉ']:
                            return get_passenger_info(pnr, context)
                    else:
                        return get_passenger_info(pnr, context)
            if len(context) == 0:
                pnr = pnr_passengers.first()
                return get_passenger_info(pnr, context)
    else:
        return None

@register.filter(name='customer_in_passenger_invoice')
def get_customer_in_passenger_invoice(pnr_id):
    """_summary_
    Returns:
        PNR issued : get all customers in passenger_invoice filtered by pnr_id
        PNR not issued : get customer directly on PNR (customer_id)
    """
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.invoice.Clients import Client
    
    if pnr_id != '' and pnr_id != None:                
        passenger_invoice_obj = PassengerInvoice.objects.filter(pnr_id=pnr_id)
        if passenger_invoice_obj.exists():            
            for passenger_invoice in passenger_invoice_obj:
                client_obj = Client.objects.filter(id=passenger_invoice.client_id)
                    
            if client_obj.exists():
                for client in client_obj:
                    return client
        else:
            return None
    return None

@register.filter(name='reference_from_passenger_invoice')
def get_reference_from_passenger_invoice(pnr_id):
    """_summary_
    Args:
        pnr_id (_type_): ID of current PNR

    Returns:
        list_reference: Return lists of all reference in passenger invoice filtered by pnr_id
    """
    
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    
    list_reference = []
    
    if pnr_id != '' and pnr_id != None:                
        passenger_invoice_obj = PassengerInvoice.objects.all().filter(pnr_id=pnr_id, status="sale")
        if passenger_invoice_obj.exists():  
            for passenger in passenger_invoice_obj:
                if passenger.reference not in list_reference:
                    list_reference.append(passenger.reference)
                    
            return list_reference[0]
        else:
            return None
    return None

@register.filter(name='ticket_not_ordered')
def get_ticket_not_ordered(ticket):
    """
        Use of disabling or not the checkbox on the line of ticket to make the creation of order for the ticket possible
        Args: 
            ticket (_type_): ticket Object
        Returns:
            ticket_not_ordered: list of ticket that is not is_invoiced (haven't any order create for the ticket)
    """
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    ticket_not_ordered = PassengerInvoice.objects.filter(ticket=ticket.id)
    if ticket_not_ordered.exists():
        return ticket_not_ordered.first()
    else:
        return None


@register.filter(name='fee_not_ordered')
def get_fee_not_ordered(fee):
    """
        Use of disabling or not the checkbox on the line of fee to make the creation of order for the fee possible
        Args: 
            fee (_type_): fee Object
        Returns:
            fee_not_ordered: list of fee that is not is_invoiced (haven't any order create for the fee)
    """
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    fee_not_ordered = PassengerInvoice.objects.filter(fee=fee.id)
    if fee_not_ordered.exists():
        return fee_not_ordered.first()
    else:
        return None
    

##############################################
# CHECK IF ONE OR MANY PASSENGER IS INVOICED #
##############################################
@register.filter(name='check_if_one_or_many_passenger_is_invoiced')
def get_check_if_one_or_many_passenger_is_invoiced(pnr):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    passenger_invoices = PassengerInvoice.objects.filter(pnr=pnr.id)
    check_list = []
    if passenger_invoices.exists():
        for passenger in passenger_invoices:
            check_list.append(passenger.is_invoiced)
        if True in check_list:
            return True
        else:
            return False
    else:
        return False
    

###########################################
# GET ALL CUSTOMERS WHO HAS NOT HAD ORDER #
###########################################
@register.filter(name='customer_has_not_had_order')
def get_customer_has_not_had_order(pnr_id):
    """
        Use to get customer who has not yet had an order
        Args: 
            pnr (_type_): pnr Object
        Returns:
            client: list of customers that isreturn passenger_invoice_obj.first() not had an order
    """
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.invoice.Clients import Client
    
    list_clients = []
    
    if pnr_id is not None:
        passenger_invoice_obj = PassengerInvoice.objects.filter(pnr_id=pnr_id, status="sale", is_invoiced=True)
        if passenger_invoice_obj.exists():
            for passenger_invoice in passenger_invoice_obj:
                client_obj = Client.objects.filter(id=passenger_invoice.client_id)
                for client in client_obj:
                    if client not in list_clients:
                        list_clients.append(client)
            return {"list": list_clients, "length": len(list_clients)}
        else:
            return None
    return None


################################################################
# GET ALL INFORMATIONS ABOUT CUSTOMER WHO HAS BEEN HAD INVOICE #
################################################################
@register.filter(name='customer_invoiced_informations')
def get_customer_invoiced_informations(pnr_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.invoice.Clients import Client
    
    list_clients = []
    
    if pnr_id is not None:
        passenger_invoice_obj = PassengerInvoice.objects.filter(pnr_id=pnr_id, status="sale", is_invoiced=True)
        if passenger_invoice_obj.exists():
            for passenger_invoice in passenger_invoice_obj:
                client_obj = Client.objects.filter(id=passenger_invoice.client_id)
                for client in client_obj:
                    context = {}
                    context['id'] = client.id
                    context['intitule'] = client.intitule
                    
                    if client.address_1 is not None:
                        context['address'] = client.address_1
                    elif client.address_1 and client.address_2 is not None:
                        context['address'] = client.address_1 + "," + client.address_2
                    else:
                        context['address'] = ""
                    
                    context['city'] = client.city
                    context['departement'] = client.departement
                    context['country'] = client.country
                    context['telephone'] = client.telephone
                    context['email'] = client.email
                    
                    if context not in list_clients:
                        list_clients.append(context)
                        
            return json.dumps(list_clients)
        else:
            return []
    return []


##########################
# GET TOTAL AMOUNT ORDER #
##########################
@register.filter(name='total_amount_order')
def get_total_amount_order(pnr_id):
    """_summary_
    Args:
        pnr_id (_type_): ID of current PNR

    Returns:
        total: Return objects that contains data about amount total for each customer
    """
    
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.invoice.Ticket import Ticket
    from AmadeusDecoder.models.invoice.Fee import Fee, OthersFee
    
    total = []
    customers = []
    
    if pnr_id is not None:                
        passenger_invoice_obj = PassengerInvoice.objects.filter(pnr_id=pnr_id) #<==is_invoiced=True
        if passenger_invoice_obj.exists():  
            for passenger in passenger_invoice_obj:
                if passenger.client_id not in customers:
                    customers.append(passenger.client_id)
                    
            if len(customers) > 0:                        
                for customer in customers:
                    passenger_invoice_per_customer_obj = PassengerInvoice.objects.filter(pnr_id=pnr_id, client_id=customer) #<==is_invoiced=True
                                        
                    ticket = {}
                    fee = {}
                    other_fee = {}
                    
                    list_ticket_total = []
                    list_fee_total = []
                    list_other_fee_total = []
                    
                    if passenger_invoice_per_customer_obj.exists():
                        for passenger in passenger_invoice_per_customer_obj:  
                            if passenger.fee_id is not None:
                                fee_obj = None
                                if passenger.fee.ticket is not None:
                                    fee_obj = Fee.objects.filter(id=passenger.fee_id, is_invoiced=False, ticket__ticket_status=1)
                                elif passenger.fee.other_fee is not None:
                                    fee_obj = Fee.objects.filter(id=passenger.fee_id, is_invoiced=False, other_fee__other_fee_status=1)
                                else:
                                    fee_obj = Fee.objects.filter(id=passenger.fee_id, is_invoiced=False, ticket=None, other_fee=None)
                                if fee_obj.exists():
                                    for f in fee_obj:
                                        list_fee_total.append(float(f.total))
                                    fee["total"] = list_fee_total
                            if passenger.ticket_id is not None:
                                ticket_obj = Ticket.objects.filter(id=passenger.ticket_id, ticket_status=1, is_invoiced=False).exclude(ticket_type='TST') # <==  is_invoiced=False
                                if ticket_obj.exists():
                                    for t in ticket_obj:
                                        list_ticket_total.append(float(t.total))
                                    ticket["total"] = list_ticket_total
                            if passenger.other_fee_id is not None:
                                other_fee_obj = OthersFee.objects.filter(id=passenger.other_fee_id, other_fee_status=1, is_invoiced=False) # <== is_invoiced=False 
                                if other_fee_obj.exists():
                                    for o in other_fee_obj:
                                        list_other_fee_total.append(float(o.total))
                                    other_fee["total"] = list_other_fee_total
                                    
                            amount_total_per_customer = {
                                "customer_id": passenger.client_id,
                                "total": float(sum(list_fee_total)) + float(sum(list_ticket_total)) + float(sum(list_other_fee_total))
                            }
                        
                        if amount_total_per_customer not in total:
                            total.append(amount_total_per_customer)
                    else:
                        return 0
                return json.dumps(total)
        else:
            return 0
    return 0

@register.filter(name='total_amount_order_for_receipt_print')
def get_total_amount_order_for_receipt_print(pnr_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.invoice.Ticket import Ticket
    from AmadeusDecoder.models.invoice.Fee import Fee, OthersFee
    
    total = []
    customers = []
    invoice_numbers = []
    
    if pnr_id is not None:                
        passenger_invoice_obj = PassengerInvoice.objects.filter(pnr_id=pnr_id, is_invoiced=True) #<==is_invoiced=True
        if passenger_invoice_obj.exists():  
            for passenger in passenger_invoice_obj:
                if passenger.invoice_number not in invoice_numbers:
                    invoice_numbers.append(passenger.invoice_number)    
                if passenger.client_id not in customers:
                    customers.append(passenger.client_id)        
                        
            if len (invoice_numbers) < 0:
                for passenger in passenger_invoice_obj:
                    passenger_invoice_per_customer_obj = PassengerInvoice.objects.filter(pnr_id=pnr_id, client_id=passenger.client_id, is_invoiced=True) #<==is_invoiced=True     
                    
                    ticket = {}
                    fee = {}
                    other_fee = {}
                    
                    list_passenger_from_ticket = []
                    list_ticket_type = []
                    list_ticket_numbers = []
                    list_ticket_issuing_date = []
                    list_ticket_tax = []
                    list_ticket_transport_cost = []
                    list_ticket_total = []
                    
                    list_fee_type = []
                    list_fee_cost = []
                    list_fee_issuing_date = []
                    list_fee_tax = []
                    list_fee_total = []
                    
                    list_other_fee_type = []
                    list_other_fee_cost = []
                    list_other_fee_issuing_date = []
                    list_other_fee_tax = []
                    list_other_fee_passenger = []
                    list_other_fee_designation = []
                    list_other_fee_total = []
                    
                    pnr_invoice_numbers = []
                    
                    if passenger_invoice_per_customer_obj.exists():
                        for passenger in passenger_invoice_per_customer_obj:  
                            if passenger.invoice_number is not None:
                                if passenger.invoice_number not in pnr_invoice_numbers:
                                    pnr_invoice_numbers.append(passenger.invoice_number)
                            if passenger.fee_id is not None:
                                fee_obj = Fee.objects.filter(id=passenger.fee_id)
                                if fee_obj.exists():
                                    for f in fee_obj:
                                        list_fee_type.append(f.type)
                                        list_fee_cost.append(float(f.cost))
                                        list_fee_tax.append(float(f.tax))
                                        list_fee_total.append(float(f.total))
                                        
                                        if f.ticket is not None:
                                            list_fee_issuing_date.append(str(f.ticket.issuing_date))
                                        elif f.other_fee is not None:
                                            list_fee_issuing_date.append(str(f.other_fee.creation_date))
                                        
                                    fee = {
                                        "type": list_fee_type,
                                        "cost": list_fee_cost,
                                        "issuing_date": list_fee_issuing_date,
                                        "tax": list_fee_tax,
                                        "total": list_fee_total,
                                        "length": len(list_fee_type),
                                        "invoice_number": passenger.invoice_number
                                    }
                            if passenger.ticket_id is not None:
                                ticket_obj = Ticket.objects.filter(id=passenger.ticket_id).exclude(ticket_type='TST') # <==  is_invoiced=True
                                if ticket_obj.exists():
                                    for t in ticket_obj:
                                        list_ticket_type.append(t.ticket_type)
                                        list_ticket_numbers.append(t.number)
                                        list_ticket_tax.append(float(t.tax))
                                        list_ticket_transport_cost.append(float(t.transport_cost))
                                        list_ticket_total.append(float(t.total))
                                        list_ticket_issuing_date.append(str(t.issuing_date))
                                        
                                        displayed_name = ''
                                        if t.passenger is not None:
                                            if t.passenger.name is not None:
                                                displayed_name  += t.passenger.name
                                            if t.passenger.surname is not None:
                                                displayed_name += ' ' + t.passenger.surname
                                            if t.passenger.designation is not None:
                                                displayed_name += ' ' + t.passenger.designation
                                        list_passenger_from_ticket.append(displayed_name)
                                        
                                    ticket = {
                                        "passenger": list_passenger_from_ticket,
                                        "type": list_ticket_type,
                                        "number": list_ticket_numbers,
                                        "issuing_date": list_ticket_issuing_date,
                                        "tax": list_ticket_tax,
                                        "transport_cost": list_ticket_transport_cost,
                                        "total": list_ticket_total,
                                        "length": len(list_ticket_numbers)
                                    }
                            if passenger.other_fee_id is not None:
                                other_fee_obj = OthersFee.objects.filter(id=passenger.other_fee_id) 
                                if other_fee_obj.exists():
                                    for o in other_fee_obj:
                                        list_other_fee_cost.append(float(o.cost))
                                        list_other_fee_tax.append(float(o.tax))
                                        list_other_fee_total.append(float(o.total))
                                        
                                        displayed_name_other_fee = ''
                                        try:
                                            temp_passenger = passenger.other_fee.related_segments.first().passenger
                                            if temp_passenger.name is not None:
                                                displayed_name_other_fee  += temp_passenger.name
                                            if temp_passenger.surname is not None:
                                                displayed_name_other_fee += ' ' + temp_passenger.surname
                                            if temp_passenger.designation is not None:
                                                displayed_name_other_fee += ' ' + temp_passenger.designation 
                                        except:
                                            temp_passenger = ""
                                            
                                        list_other_fee_passenger.append(displayed_name_other_fee)
                                        list_other_fee_designation.append(o.designation)
                                        list_other_fee_issuing_date.append(str(o.creation_date))
                                    
                                    list_other_fee_type.append("EMD")  
                                    
                                    other_fee = {
                                        "designation": list_other_fee_designation,
                                        "passenger": list_other_fee_passenger,
                                        "cost": list_other_fee_cost,
                                        "type": list_other_fee_type,
                                        "issuing_date": list_other_fee_issuing_date,
                                        "tax": list_other_fee_tax,
                                        "total": list_other_fee_total,
                                        "length": len(list_other_fee_type)
                                    }
                                    
                            amount_total_per_customer = {
                                "fee": fee or [],
                                "ticket": ticket or [],
                                "other_fee": other_fee or [],
                                "customer_id": passenger.client_id,
                                "pnr_invoice_numbers": pnr_invoice_numbers,
                                "total": float(sum(list_fee_total)) + float(sum(list_ticket_total)) + float(sum(list_other_fee_total))
                            }
                        
                        if amount_total_per_customer not in total:
                            total.append(amount_total_per_customer)
                    else:
                        return []
                return json.dumps(total)
            if len (invoice_numbers) > 0:               
                for passenger in passenger_invoice_obj:
                    passenger_invoice_per_customer_obj = PassengerInvoice.objects.filter(pnr_id=pnr_id, invoice_number=passenger.invoice_number, client_id=passenger.client_id, is_invoiced=True) #<==is_invoiced=True 
                        
                    ticket = {}
                    fee = {}
                    other_fee = {}
                    
                    list_passenger_from_ticket = []
                    list_ticket_type = []
                    list_ticket_numbers = []
                    list_ticket_issuing_date = []
                    list_ticket_tax = []
                    list_ticket_transport_cost = []
                    list_ticket_total = []
                    
                    list_fee_type = []
                    list_fee_cost = []
                    list_fee_issuing_date = []
                    list_fee_tax = []
                    list_fee_total = []
                    
                    list_other_fee_type = []
                    list_other_fee_cost = []
                    list_other_fee_issuing_date = []
                    list_other_fee_tax = []
                    list_other_fee_passenger = []
                    list_other_fee_designation = []
                    list_other_fee_total = []
                    
                    pnr_invoice_numbers = []
                    
                    if passenger_invoice_per_customer_obj.exists():
                        for passenger in passenger_invoice_per_customer_obj:  
                            if passenger.invoice_number is not None:
                                if passenger.invoice_number not in pnr_invoice_numbers:
                                    pnr_invoice_numbers.append(passenger.invoice_number)
                            if passenger.fee_id is not None:
                                fee_obj = Fee.objects.filter(id=passenger.fee_id)
                                if fee_obj.exists():
                                    for f in fee_obj:
                                        list_fee_type.append(f.type)
                                        list_fee_cost.append(float(f.cost))
                                        list_fee_tax.append(float(f.tax))
                                        list_fee_total.append(float(f.total))
                                        
                                        if f.ticket is not None:
                                            list_fee_issuing_date.append(str(f.ticket.issuing_date))
                                        elif f.other_fee is not None:
                                            list_fee_issuing_date.append(str(f.other_fee.creation_date))
                                        
                                    fee = {
                                        "type": list_fee_type,
                                        "cost": list_fee_cost,
                                        "issuing_date": list_fee_issuing_date,
                                        "tax": list_fee_tax,
                                        "total": list_fee_total,
                                        "length": len(list_fee_type),
                                        "invoice_number": passenger.invoice_number
                                    }
                            if passenger.ticket_id is not None:
                                ticket_obj = Ticket.objects.filter(id=passenger.ticket_id).exclude(ticket_type='TST')
                                if ticket_obj.exists():
                                    for t in ticket_obj:
                                        list_ticket_type.append(t.ticket_type)
                                        list_ticket_numbers.append(t.number)
                                        list_ticket_tax.append(float(t.tax))
                                        list_ticket_transport_cost.append(float(t.transport_cost))
                                        list_ticket_total.append(float(t.total))
                                        list_ticket_issuing_date.append(str(t.issuing_date))
                                        
                                        displayed_name = ''
                                        if t.passenger is not None:
                                            if t.passenger.name is not None:
                                                displayed_name  += t.passenger.name
                                            if t.passenger.surname is not None:
                                                displayed_name += ' ' + t.passenger.surname
                                            if t.passenger.designation is not None:
                                                displayed_name += ' ' + t.passenger.designation
                                        list_passenger_from_ticket.append(displayed_name)
                                        
                                    ticket = {
                                        "passenger": list_passenger_from_ticket,
                                        "type": list_ticket_type,
                                        "number": list_ticket_numbers,
                                        "issuing_date": list_ticket_issuing_date,
                                        "tax": list_ticket_tax,
                                        "transport_cost": list_ticket_transport_cost,
                                        "total": list_ticket_total,
                                        "length": len(list_ticket_numbers)
                                    }
                            if passenger.other_fee_id is not None:
                                other_fee_obj = OthersFee.objects.filter(id=passenger.other_fee_id) 
                                if other_fee_obj.exists():
                                    for o in other_fee_obj:
                                        list_other_fee_cost.append(float(o.cost))
                                        list_other_fee_tax.append(float(o.tax))
                                        list_other_fee_total.append(float(o.total))
                                        
                                        displayed_name_other_fee = ''
                                        try:
                                            temp_passenger = passenger.other_fee.related_segments.first().passenger
                                            if temp_passenger.name is not None:
                                                displayed_name_other_fee  += temp_passenger.name
                                            if temp_passenger.surname is not None:
                                                displayed_name_other_fee += ' ' + temp_passenger.surname
                                            if temp_passenger.designation is not None:
                                                displayed_name_other_fee += ' ' + temp_passenger.designation 
                                        except:
                                            temp_passenger = ""
                                            
                                        list_other_fee_passenger.append(displayed_name_other_fee)
                                        list_other_fee_designation.append(o.designation)
                                        list_other_fee_issuing_date.append(str(o.creation_date))
                                    
                                    list_other_fee_type.append("EMD")  
                                    
                                    other_fee = {
                                        "designation": list_other_fee_designation,
                                        "passenger": list_other_fee_passenger,
                                        "cost": list_other_fee_cost,
                                        "type": list_other_fee_type,
                                        "issuing_date": list_other_fee_issuing_date,
                                        "tax": list_other_fee_tax,
                                        "total": list_other_fee_total,
                                        "length": len(list_other_fee_type)
                                    }
                                    
                            amount_total_per_customer = {
                                "fee": fee or [],
                                "ticket": ticket or [],
                                "other_fee": other_fee or [],
                                "customer_id": passenger.client_id,
                                "pnr_invoice_numbers": pnr_invoice_numbers,
                                "total": float(sum(list_fee_total)) + float(sum(list_ticket_total)) + float(sum(list_other_fee_total))
                            }
                        
                        if amount_total_per_customer not in total:
                            total.append(amount_total_per_customer)
                    else:
                        return []
                return json.dumps(total)
        else:
            return []
    return []


############################
# CHECK IF FEE IS INVOICED #
############################
@register.filter(name='is_fee_invoiced')
def check_if_fee_is_invoiced(fee_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.invoice.Fee import Fee
    
    passenger_invoice_obj = PassengerInvoice.objects.filter(fee=fee_id)
    fee_obj = Fee.objects.filter(id=fee_id)
    
    fee_is_invoiced = []
    
    if passenger_invoice_obj.exists() or fee_obj.exists():
        for passenger_invoice in passenger_invoice_obj:
            fee_is_invoiced.append(passenger_invoice.is_invoiced)
        for fee in fee_obj:
            fee_is_invoiced.append(fee.is_invoiced)
        if True in fee_is_invoiced:
            return True
        else:
            return False
    else:
        return False
    
    
##################################
# CHECK IF OTHER_FEE IS INVOICED #
##################################
@register.filter(name='is_other_fee_invoiced')
def check_if_other_fee_invoiced(other_fee_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.invoice.Fee import OthersFee
    
    passenger_invoice_obj = PassengerInvoice.objects.filter(other_fee_id=other_fee_id)
    other_fee_obj = OthersFee.objects.filter(id=other_fee_id)
    
    other_fee_is_invoiced = []
    
    if passenger_invoice_obj.exists() or other_fee_obj.exists():
        for passenger_invoice in passenger_invoice_obj:
            other_fee_is_invoiced.append(passenger_invoice.is_invoiced)
        for other_fee in other_fee_obj:
            other_fee_is_invoiced.append(other_fee.is_invoiced)
        if True in other_fee_is_invoiced:
            return True
        else:
            return False
    else:
        return False
    
#############################
# GET TICKET INVOICE NUMBER #
#############################
@register.filter(name='ticket_invoice_number')
def get_ticket_invoice_number(pnr_id, ticket_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    passenger_invoices = PassengerInvoice.objects.filter(pnr_id=pnr_id, ticket_id=ticket_id, is_invoiced=True)
    if passenger_invoices.exists():
        for passenger in passenger_invoices:
            return passenger.invoice_number
        
##########################
# GET FEE INVOICE NUMBER #
##########################
@register.filter(name='fee_invoice_number')
def get_fee_invoice_number(pnr_id, fee_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    passenger_invoices = PassengerInvoice.objects.filter(pnr_id=pnr_id, fee_id=fee_id, is_invoiced=True)
    if passenger_invoices.exists():
        for passenger in passenger_invoices:
            return passenger.invoice_number
        
###############################
# GET OTHERFEE INVOICE NUMBER #
###############################
@register.filter(name='other_fee_invoice_number')
def get_other_fee_invoice_number(pnr_id, other_fee_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    passenger_invoices = PassengerInvoice.objects.filter(pnr_id=pnr_id, other_fee_id=other_fee_id, is_invoiced=True)
    if passenger_invoices.exists():
        for passenger in passenger_invoices:
            return passenger.invoice_number



##########################################################
#### Calculate Amout total depend on line not ordered ####
##########################################################

@register.filter(name='order_amount_total')
def get_order_amout_total(pnr):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.invoice.Ticket import Ticket
    from AmadeusDecoder.models.invoice.Fee import OthersFee, Fee
    pnr = Pnr.objects.get(pk=pnr.id)
    passenger_invoices = PassengerInvoice.objects.filter(pnr_id=pnr)
    amount_total = 0
    amount_invoiced = 0
    pnr_elements_count = 0
    fee_not_invoiced_count = 0
    tickets = Ticket.objects.filter(pnr=pnr, ticket_status=1, is_invoiced=False)
    other_fees = OthersFee.objects.filter(pnr=pnr, is_invoiced=False)
    if tickets.exists() and other_fees.exists():
        for ticket in tickets:
            fees = Fee.objects.filter(ticket=ticket, is_invoiced=False)
            if fees.exists():
                fee_not_invoiced_count += 1
        for other_fee in other_fees:
            fees = Fee.objects.filter(other_fee=other_fee, is_invoiced=False)
            if fees.exists():
                fee_not_invoiced_count += 1
        pnr_elements_count = tickets.count() + other_fees.count() + fee_not_invoiced_count
    if pnr.status_value == 0:
        order_invoiced = passenger_invoices.filter(status='sale', is_invoiced=True)
        passenger_invoice = passenger_invoices.filter(status='sale', is_invoiced=False)
        if order_invoiced.exists():
            for order in order_invoiced:
                if order.ticket is not None and order.ticket.ticket_status == 1:
                    amount_invoiced += order.ticket.total
                if order.fee is not None:
                    if (order.fee.ticket is not None and order.fee.ticket.ticket_status == 1) or (order.fee.other_fee is not None and order.fee.other_fee.other_fee_status == 1):
                        amount_invoiced += order.fee.total
                if order.other_fee is not None and order.other_fee.other_fee_status == 1:
                    amount_invoiced += order.other_fee.total
            if passenger_invoice.exists() and passenger_invoice.count() == pnr_elements_count:
                for order in passenger_invoice:
                    if order.ticket is not None and order.ticket.ticket_status == 1:
                        amount_total += order.ticket.total
                    if order.fee is not None:
                        if (order.fee.ticket is not None and order.fee.ticket.ticket_status == 1) or (order.fee.other_fee is not None and order.fee.other_fee.other_fee_status == 1):
                            amount_invoiced += order.fee.total
                    if order.other_fee is not None and order.other_fee.other_fee_status == 1:
                        amount_total += order.other_fee.total
            else:
                amount_total = pnr.invoice.detail.total - amount_invoiced
        else:
            amount_total = pnr.invoice.detail.total
    elif pnr.status_value == 1:
        quotation_invoiced = passenger_invoices.filter(status='quotation', is_quotation=True)
        passenger_invoice = passenger_invoices.filter(status='quotation', is_quotation=False)
        if quotation_invoiced.exists():
            for order in quotation_invoiced:
                if order.ticket is not None and order.ticket.ticket_status == 1:
                    amount_invoiced += order.ticket.total
                if order.fee is not None:
                    if (order.fee.ticket is not None and order.fee.ticket.ticket_status == 1) or (order.fee.other_fee is not None and order.fee.other_fee.other_fee_status == 1):
                        amount_invoiced += order.fee.total
                if order.other_fee is not None and order.other_fee.other_fee_status == 1:
                    amount_invoiced += order.other_fee.total
                if order.invoice_id is not None:
                    amount_total += order.invoice_id.detail.total
            if passenger_invoice.exists() and passenger_invoice.count() == pnr_elements_count:
                for order in passenger_invoice:
                    if order.ticket is not None and order.ticket.ticket_status == 1:
                        amount_total += order.ticket.total
                    if order.fee is not None:
                        if (order.fee.ticket is not None and order.fee.ticket.ticket_status == 1) or (order.fee.other_fee is not None and order.fee.other_fee.other_fee_status == 1):
                            amount_invoiced += order.fee.total
                    if order.other_fee is not None and order.other_fee.other_fee_status == 1:
                        amount_total += order.other_fee.total
                    if order.invoice_id is not None:
                        amount_total += order.invoice_id.detail.total
        else:
            amount_total = pnr.invoice.detail.total

    return amount_total


##############################################################
#### Calculate Fee Amout total depend on line not ordered ####
##############################################################

@register.filter(name='fee_amount_total')
def get_fee_amount_total(pnr):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.pnr.Pnr import Pnr
    from AmadeusDecoder.models.invoice.Ticket import Ticket
    from AmadeusDecoder.models.invoice.Fee import OthersFee, Fee
    pnr = Pnr.objects.get(pk=pnr.id)
    passenger_invoices = PassengerInvoice.objects.filter(pnr_id=pnr)
    fee_amount_total = 0
    fee_amount_invoiced = 0
    fee_not_invoiced_count = 0
    pnr_elements_count = 0
    tickets = Ticket.objects.filter(pnr=pnr, ticket_status=1, is_invoiced=False)
    other_fees = OthersFee.objects.filter(pnr=pnr, is_invoiced=False, other_fee_status=1)
    if tickets.exists() and other_fees.exists():
        for ticket in tickets:
            fees = Fee.objects.filter(ticket=ticket, is_invoiced=False)
            if fees.exists():
                fee_not_invoiced_count += 1
        for other_fee in other_fees:
            fees = Fee.objects.filter(other_fee=other_fee, is_invoiced=False)
            if fees.exists():
                fee_not_invoiced_count += 1
        pnr_elements_count = fee_not_invoiced_count
    if pnr.status_value == 0:
        order_invoiced = passenger_invoices.filter(status='sale', is_invoiced=True).exclude(fee=None)
        passenger_invoice = passenger_invoices.filter(status='sale', is_invoiced=False).exclude(fee=None)
        if order_invoiced.exists():
            for order in order_invoiced:
                if (order.fee.ticket is not None and order.fee.ticket.ticket_status == 1) or (order.fee.other_fee is not None and order.fee.other_fee.other_fee_status == 1):
                    fee_amount_invoiced += order.fee.total
            if passenger_invoice.exists() and passenger_invoice.count() == pnr_elements_count:
                for order in passenger_invoice:
                    if (order.fee.ticket is not None and order.fee.ticket.ticket_status == 1) or (order.fee.other_fee is not None and order.fee.other_fee.other_fee_status == 1):
                        fee_amount_total += order.fee.total
            else:
                fee_amount_total = pnr.invoice.detail.total_fees - fee_amount_invoiced
        else:
            fee_amount_total = pnr.invoice.detail.total_fees
    elif pnr.status_value == 1:
        quotation_invoiced = passenger_invoices.filter(status='quotation', is_quotation=True).exclude(fee=None)
        passenger_invoice = passenger_invoices.filter(status='quotation', is_quotation=False).exclude(fee=None)
        if quotation_invoiced.exists():
            for order in quotation_invoiced:
                if order.fee.ticket.ticket_status == 1:
                    fee_amount_invoiced += order.fee.total
            if passenger_invoice.exists():
                for order in passenger_invoice and passenger_invoice.count() == pnr_elements_count:
                    if order.fee is not None and order.fee.ticket.ticket_status == 1:
                        fee_amount_total += order.fee.total
            else:
                fee_amount_total = pnr.invoice.detail.total_fees - fee_amount_invoiced
        else:
            fee_amount_total = pnr.invoice.detail.total_fees

    return fee_amount_total
        
#################################
# GET STATE OF PNR IN T_COMMENT #
#################################
@register.filter(name='pnr_comment_state')
def get_pnr_comment_state(pnr):
    from AmadeusDecoder.models.utilities.Comments import Comment
    comments = Comment.objects.filter(pnr_id_id=pnr.id)
    states = []
    if comments.exists():
        for comment in comments:
            states.append(comment.state)
        if len(states) == 0:
            return 1
        if False in states:
            return 0
        else:
            return 1
    else:
        return -1
    
###########################
# FIND FEE REDUCE REQUEST #
###########################
@register.filter(name='find_fee_reduce_request')
def get_find_fee_reduce_request(pnr, fee):
    from AmadeusDecoder.models.invoice.Fee import ReducePnrFeeRequest
    reduce_pnr_fee_requests = ReducePnrFeeRequest.objects.filter(pnr_id=pnr.id, fee_id=fee.id)
    fee_reduce_request_found = 0
    if reduce_pnr_fee_requests.exists():
        for reduce_pnr_fee_request in reduce_pnr_fee_requests:
            if reduce_pnr_fee_request.status == 0:
                fee_reduce_request_found += 1
            else:
                fee_reduce_request_found += 0
        if fee_reduce_request_found > 0:
            return True
        else:
            return False
    else:
        return False
        
# check if current ticket has been issued at airport #
@register.simple_tag
def is_issued_at_airport(ticket, other_fee):
    from AmadeusDecoder.models.invoice.Ticket import Ticket
    from AmadeusDecoder.models.invoice.Fee import OthersFee
    
    # for ticket
    if ticket is not None:
        current_ticket = Ticket.objects.filter(id=ticket.id, ticket_type='EMD').first()
        if current_ticket is not None:
            # ticket has agency name: mostly for Zenith
            if current_ticket.issuing_agency_name in AIRPORT_AGENCY_CODE:
                return True
            # ticket has agency object: mostly for Altea
            if current_ticket.issuing_agency is not None:
                if current_ticket.issuing_agency.name in AIRPORT_AGENCY_CODE or \
                    current_ticket.issuing_agency.code in AIRPORT_AGENCY_CODE:
                    return True
    # for other fee: mostly for Zenith
    elif other_fee is not None:
        current_other_fee = OthersFee.objects.filter(id=other_fee.id, fee_type='EMD').first()
        if current_other_fee is not None:
            # other fee agency name
            if current_other_fee.issuing_agency_name in AIRPORT_AGENCY_CODE:
                return True
        
    return False

# get flight cabin from segment's flight class
@register.filter(name='flight_cabin')
def get_segment_cabin(segment):
    from AmadeusDecoder.models.invoice.ServiceFees import ClassCabin
    
    flight_cabin = ''
    try:
        related_pnr = segment.pnr
        related_cabin = ClassCabin.objects.filter(sign__contains=[segment.flightclass], gdsprovider=related_pnr.type).first()
        if related_cabin is not None:
            return related_cabin.type
    except Exception as e:
        print('Getting flight cabin encountered some error (templatetags/pnr_details.py (name=flight_cabin)): ', e)
        return flight_cabin
    
@register.filter(name='manage_pnr_switch_with_button')
def get_all_pnr_to_switch(request):
    from AmadeusDecoder.models.pnr.Pnr import Pnr
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
    
    try:
        filtered_creator = request.COOKIES.get('creator_pnr_filter')
        filtered_creator_cookie = None
        if str(json.loads(filtered_creator)[0]) == "0":
            filtered_creator_cookie = None
        elif str(json.loads(filtered_creator)[0]) == 'Empty':
            filtered_creator_cookie = 'Empty'
        else:
            filtered_creator_cookie = [int(user_id) for user_id in json.loads(filtered_creator)]
            
        # print(filtered_creator_cookie)
        # print(type(filtered_creator_cookie))
    except Exception as e:
        filtered_creator_cookie = None
        # print(f"Error on filter creator ${e}")

    # Retrieve the value of the "isSortedByCreator" cookie from the request
    is_sorter_by_creator = request.COOKIES.get('isSortedByCreator')

    # Initialize the sort_creator variable to a default value
    # Set order_by username ascendant
    sort_creator = None

    # Determine the value of "sort_creator" based on the value of the cookie
    if is_sorter_by_creator is not None:
        sort_creator = is_sorter_by_creator

    # print(sort_creator)
    
    date_filter = Q(system_creation_date__range=[start_date, end_date]) if start_date and end_date else Q()
    max_system_creation_date = Q(system_creation_date__gt=maximum_timezone)
    
    agency_name_filter = request.COOKIES.get('agency_name_filter')
    
    agency_name = Q()
    if agency_name_filter and agency_name_filter != "0":
        agency_name = Q(agency_name__icontains=agency_name_filter) | Q(agency__name__icontains=agency_name_filter) if agency_name_filter else Q()
    elif agency_name_filter == "0":
        agency_name = Q(agency_name="", agent_code="", agency=None)
   

    status_value = Q(status_value=status_value_from_cookie) if status_value_from_cookie in [0, 1] else Q()

    if request.user.id in [4, 5]: #==> [Farida et Mouniati peuvent voir chacun l'ensemble de leurs pnr]
        pnr_list = []
        issuing_users = request.user.copied_documents.all()

        if is_invoiced is None:
            for issuing_user in issuing_users:
                pnr =   Pnr.objects.filter(
                            number=issuing_user.document
                        ).filter(
                            max_system_creation_date, 
                            status_value,
                            date_filter,
                            agency_name,
                        ).first()
                if pnr not in pnr_list and pnr is not None:
                    pnr_list.append(pnr)
            
            agent = Q()
            if filtered_creator_cookie == 'Empty':
                agent = Q(agent_id=None)
            elif filtered_creator_cookie is not None and filtered_creator_cookie != 'Empty':
                agent = Q(agent_id__in=filtered_creator_cookie)
            else:
                agent = Q(agent_id=4) | Q(agent_id=5)

            pnr_obj  =  Pnr.objects.filter(
                            agent
                        ).filter(
                            max_system_creation_date, 
                            status_value,
                            date_filter,
                            agency_name,
                        ).all().order_by(date_order_by + 'system_creation_date')

            for pnr in pnr_obj:
                if pnr not in pnr_list:
                    pnr_list.append(pnr)

            if date_order_by == "-" :
                pnr_list = sorted(pnr_list, key=lambda pnr: pnr.system_creation_date, reverse=True)
            else :
                pnr_list = sorted(pnr_list, key=lambda pnr: pnr.system_creation_date, reverse=False)

        else:
            for issuing_user in issuing_users:
                pnr =   Pnr.objects.filter(
                            number=issuing_user.document
                        ).filter(
                            max_system_creation_date, 
                            status_value,
                            date_filter,
                            agency_name,
                        ).filter(is_invoiced=is_invoiced).first()
                if pnr not in pnr_list and pnr is not None:
                    pnr_list.append(pnr)

            agent = Q()
            if filtered_creator_cookie == 'Empty':
                agent = Q(agent_id=None)
            elif filtered_creator_cookie is not None and filtered_creator_cookie != 'Empty':
                agent = Q(agent_id__in=filtered_creator_cookie)
            else:
                agent = Q(agent_id=4) | Q(agent_id=5)

            pnr_obj =   Pnr.objects.filter(
                            agent
                        ).filter(
                            max_system_creation_date, 
                            status_value,
                            date_filter,
                            agency_name,
                        ).filter(is_invoiced=is_invoiced).all().order_by(date_order_by + 'system_creation_date')

            for pnr in pnr_obj:
                if pnr not in pnr_list:
                    pnr_list.append(pnr)

            if date_order_by == "-" :
                pnr_list = sorted(pnr_list, key=lambda pnr: pnr.system_creation_date, reverse=True)
            else :
                pnr_list = sorted(pnr_list, key=lambda pnr: pnr.system_creation_date, reverse=False)
        list_pnr_with_position = [{'id': pnr.id, 'position': index, 'number': pnr.number} for index, pnr in enumerate(pnr_list)]
        return json.dumps(list_pnr_with_position)

    if request.user.role_id == 3:
        pnr_list = []
        issuing_users = request.user.copied_documents.all()
        if is_invoiced is not None:
            for issuing_user in issuing_users:
                pnr =   Pnr.objects.filter(
                            number=issuing_user.document
                        ).filter(
                            max_system_creation_date, 
                            date_filter,
                            status_value,
                            agency_name,
                        ).filter(is_invoiced=is_invoiced).first()
                if pnr not in pnr_list and pnr is not None:
                    pnr_list.append(pnr)

            agent = Q()
            if filtered_creator_cookie == 'Empty':
                agent = Q(agent_id=None)
            elif filtered_creator_cookie is not None and filtered_creator_cookie != 'Empty':
                agent = Q(agent_id__in=filtered_creator_cookie)
            else:
                agent = Q(agent_id=request.user.id) | Q(agent_id=None)

            pnr_obj =   Pnr.objects.filter(
                            agent
                        ).filter(
                            max_system_creation_date,
                            date_filter, 
                            status_value,
                            agency_name,
                        ).filter(is_invoiced=is_invoiced).all().order_by(date_order_by + 'system_creation_date')
            for pnr in pnr_obj:
                if pnr not in pnr_list:
                    pnr_list.append(pnr)

            if date_order_by == "-" :
                pnr_list = sorted(pnr_list, key=lambda pnr: pnr.system_creation_date, reverse=True)
            else :
                pnr_list = sorted(pnr_list, key=lambda pnr: pnr.system_creation_date, reverse=False)

        list_pnr_with_position = [{'id': pnr.id, 'position': index, 'number': pnr.number} for index, pnr in enumerate(pnr_list)]
        return json.dumps(list_pnr_with_position)

    else:
        if filtered_creator_cookie is not None and filtered_creator_cookie != 'Empty': 
            if is_invoiced == None:
                pnr_list =  Pnr.objects.filter(
                                Q(agent_id__in=filtered_creator_cookie),
                                status_value,
                                date_filter,
                                max_system_creation_date,
                                agency_name,
                            ).all().order_by(date_order_by + 'system_creation_date') # <======= IMPORTANT
            else:
                pnr_list =  Pnr.objects.filter(
                                Q(agent_id__in=filtered_creator_cookie), 
                                status_value,
                                date_filter,
                                max_system_creation_date,
                                agency_name,
                            ).all().order_by(date_order_by + 'system_creation_date').filter(is_invoiced=is_invoiced)
            print('Not all')
        elif filtered_creator_cookie is None: ##### Si 'Tout' est sélectionner dans le filtre créateur
            if is_invoiced == None:
                pnr_list =  Pnr.objects.all().order_by(date_order_by + 'system_creation_date').filter(
                                status_value,
                                date_filter,
                                max_system_creation_date,
                                agency_name,
                            ) # <======= IMPORTANT
            else:
                pnr_list =  Pnr.objects.all().order_by(date_order_by + 'system_creation_date').filter(
                                status_value,
                                date_filter,
                                max_system_creation_date,
                                agency_name,
                            ).filter(is_invoiced=is_invoiced)
            print('All')
        elif filtered_creator_cookie == 'Empty':
            if is_invoiced == None:
                pnr_list =  Pnr.objects.filter(agent_id=None).order_by(date_order_by + 'system_creation_date').filter(
                                status_value,
                                date_filter,
                                max_system_creation_date,
                                agency_name,
                            ) # <======= IMPORTANT
            else:
                pnr_list =  Pnr.objects.filter(agent_id=None).order_by(date_order_by + 'system_creation_date').filter(
                                status_value,
                                date_filter,
                                max_system_creation_date,
                                agency_name,
                            ).filter(is_invoiced=is_invoiced)
            print('All')

        list_pnr_with_position = [{'id': pnr.id, 'position': index, 'number': pnr.number} for index, pnr in enumerate(pnr_list)] # type: ignore
        print(len(list_pnr_with_position))
        return json.dumps(list_pnr_with_position)

###### Use to block checkbox when ticket or service is cancel or void immedialty after being issued so it can't be ordered ######
@register.filter(name='ticket_cancel_void_status')
def get_ticket_cancel_void_status(ticket):
    from AmadeusDecoder.models.invoice.Fee import OthersFee
    is_cancelled = False
    ticket_line_canceller = OthersFee.objects.filter(ticket_id=ticket.id).exclude(fee_type='outsourcing')
    print("ticket_line_canceller: " + str(ticket_line_canceller))

    if ticket_line_canceller.exists() and not ticket.is_subjected_to_fees and ticket.is_invoiced:
        is_cancelled = True
    else:
        is_cancelled= False
        
    return is_cancelled

@register.filter(name='other_fee_cancel_void_status')
def get_other_fee_cancel_void_status(other_fee):
    from AmadeusDecoder.models.invoice.Fee import OthersFee
    is_cancelled = False
    other_fee_line_canceller = OthersFee.objects.filter(other_fee=other_fee.id).exclude(fee_type='outsourcing') # type: ignore
    print("other_fee_line_canceller: " + str(other_fee_line_canceller))

    if other_fee_line_canceller.exists() and not other_fee.is_subjected_to_fee and other_fee.is_invoiced:
        is_cancelled = True
    else:
        is_cancelled= False

    return is_cancelled

@register.filter(name='list_agency_name')
def get_list_agency_name(_):
    """
    Retourne une liste de dictionnaires contenant les noms d'agence.

    Args:
        _ (str): Paramêtre non utilisé.

    Returns:
        list: Liste de dictionnaires.
    """
    
    _OFFICE_LIST_SKIP = ['DZAUU01A1', 'DZAUU01A3', 'DZAUU01A4']  # Liste des codes de bureau à ignorer
    _AGENCY_NAME_SKIP = ['GSA ISSOUFALI Dzaoudzi', 'GSA ISSOUFALI Jumbo Score', 'GSA ISSOUFALI Mamoudzou']  # Liste des noms d'agence à ignorer
    
    # Récupérer les noms d'agence distincts de la table Pnr
    distinct_agency_names = set(Pnr.objects.values_list('agency_name', flat=True))
    
    # Récupérer les noms de bureau distincts de la table Office
    office_list = set(Office.objects.filter(company_id=1).values_list('name', flat=True))
    
    # Ensemble pour stocker les noms d'agence
    agency_names = set()
    
    # Filtrer et ajouter les noms d'agence à l'ensemble
    agency_names = {agency.strip() for agency in distinct_agency_names if agency.strip() not in _AGENCY_NAME_SKIP}

    # Filtrer et ajouter les noms de bureau à l'ensemble
    office_names = {office.strip() for office in office_list if office.strip() not in _OFFICE_LIST_SKIP}

    # Ajouter les noms de bureau à l'ensemble des noms d'agence
    agency_names.update(office_names)
    
    altea_agency = set(['Jumbo Score', 'Dzaoudzi', 'Mamoudzou', 'Office 5'])  # Noms d'agence supplémentaires
    agency_names = sorted(agency_names.union(altea_agency))  # Fusionner les ensembles et trier les noms d'agence
    
    # Afficher les noms d'agence
    # print(f'''
    #     Liste de tous les agences \n
    #     *******************************
    #     {agency_names}
    #     *******************************
    #     {len(agency_names)}
    #     *******************************
    # ''')
    
    # Créer une liste de dictionnaires contenant les noms d'agence
    return [{'agency_name': agency} for agency in agency_names]

@register.filter(name='check_passenger_missing')
def get_check_passenger_missing(pnr_id, client_id):   
    passenger_invoices = PassengerInvoice.objects.filter(pnr=pnr_id, client=client_id)
    
    tickets = []
    for passenger_invoice in passenger_invoices:
        if passenger_invoice.ticket is not None:
            tickets.append(passenger_invoice.ticket)
                
    count_passenger_missing = 0    
    for ticket in tickets:
        if ticket.passenger is None:
            count_passenger_missing += 1
        else:
            count_passenger_missing += 0

    return count_passenger_missing