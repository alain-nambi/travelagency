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
    user_obj = User.objects.only('id', 'username')
    return json.dumps([{"id": user.id, "username": user.username} for user in user_obj])

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

@register.filter(name='passenger_is_invoiced_in_passenger_invoice')
def get_passenger_is_invoiced_in_passenger_invoice(pnr_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    passenger_invoices = PassengerInvoice.objects.filter(pnr_id=pnr_id).exclude(status="quotation")
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
    
@register.filter(name='passenger_segment_mail_missing')
def get_passenger_segment_missing(pnr):
    # from AmadeusDecoder.models.invoice.Ticket import Ticket
    tickets = pnr.tickets.filter(state=2).all()
    tickets_passenger_segment = []
    for ticket in tickets :
        res = ''
        try:
            if ticket.passenger and ticket.passenger.order is not None :
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

@register.filter(name='pnr_comment_state')
def get_pnr_comment_state(pnr_id):
    from AmadeusDecoder.models.utilities.Comments import Comment
    comments = Comment.objects.filter(pnr_id_id=pnr_id)
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

@register.filter(name='ticket_issuing_date')
def get_issuing_date(pnr):
    try:
        return pnr.get_max_issuing_date()
    except:
        return None
    
@register.filter(name='order_amount_total')
def get_order_amout_total(pnr_id):
    from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
    from AmadeusDecoder.models.invoice.Ticket import Ticket
    from AmadeusDecoder.models.invoice.Fee import OthersFee, Fee
    pnr = Pnr.objects.get(pk=pnr_id)
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

@register.filter(name='opc')
def get_min_opc(pnr):
    try:
        return pnr.get_min_opc()
    except:
        return ''

@register.filter(name='min_opc')
def get_min_opc(pnr_id):
    try:
        pnr = Pnr.objects.get(pk=pnr_id)
        if pnr:
            return pnr.get_min_opc()
    except:
        return ''
    
@register.filter(name='pnr_creator')
def get_pnr_creator(pnr):
    try:
        return pnr.get_creator_agent()
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
    
@register.filter(name='uniformised_pnr_agency')
def uniformed_pnr_agency_processing(agency):
    # Define the uniformized agency names
    agence_name_uniformised = {'GSA ISSOUFALI Dzaoudzi', 'GSA ISSOUFALI Jumbo Score', 'GSA ISSOUFALI Mamoudzou'}
    
    try:
        agency = str(agency).strip()
        if agency in agence_name_uniformised:
            return agency.replace("GSA ISSOUFALI", "").strip()
        return agency
    except Exception:
        pass
    return None
