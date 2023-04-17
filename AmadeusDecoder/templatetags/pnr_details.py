'''
Created on 29 Sep 2022

@author: Famenontsoa
'''

from django import template
from django.db.models import Q
import json
import traceback

register = template.Library()

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
    
@register.filter(name='pnr_creator')
def get_pnr_creator(pnr):
    try:
        return pnr.get_creator_agent()
    except:
        return None
    
@register.filter(name='company_currency')
def get_company_currency(company_name):
    from AmadeusDecoder.models.company_info.CompanyInfo import CompanyInfo
    try:
        return CompanyInfo.objects.filter(company_name=company_name).first().company_currency
    except:
        return ''

@register.filter(name='pnr_count')
def get_all_pnr(request):
    # Add max timezone 
    maximum_timezone = "2023-01-01 01:00:00.000000+03:00"
    
    if request is not None:
        filtered_creator = request.COOKIES.get('creator_pnr_filter')
        if filtered_creator is None :
            filtered_creator = '0'

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
    
    from AmadeusDecoder.models.pnr.Pnr import Pnr
    try:
        if is_invoiced is None:
            if request.user.id in [30, 16] or request.user.role_id in [1, 2]: #==> [Admin Dev, Philippe P. et Direction]
                if filtered_creator != '0' and filtered_creator is not None:
                    pnr_count = Pnr.objects.filter(Q(system_creation_date__gt=maximum_timezone), Q(agent_id=filtered_creator)).count()
                elif filtered_creator == '0' or filtered_creator is None:
                    pnr_count = Pnr.objects.filter(Q(system_creation_date__gt=maximum_timezone)).all().count()
            else:
                if request.user.id in [4, 5]: #==> [Farida et Mouniati peuvent voir chacun l'ensemble de leurs pnr]
                    pnr_list = []
                    pnr_count = 0
                    issuing_users = request.user.copied_documents.all()
                    for issuing_user in issuing_users:
                        pnr = Pnr.objects.filter(number=issuing_user.document).filter(Q(system_creation_date__gt=maximum_timezone)).first()
                        if pnr not in pnr_list and pnr is not None:
                            pnr_list.append(pnr)
                
                    pnr_obj = Pnr.objects.filter(Q(agent_id=filtered_creator)).filter(Q(system_creation_date__gt=maximum_timezone)).all()
                    
                    for pnr in pnr_obj:
                        if pnr not in pnr_list:
                            pnr_list.append(pnr)
                
                    pnr_count = len(pnr_list)
                else:
                    pnr_count = Pnr.objects.filter(Q(agent_id=filtered_creator)).filter(Q(system_creation_date__gt=maximum_timezone)).count()
        if is_invoiced is not None:
            if request.user.id in [30, 16] or request.user.role_id in [1, 2]: #==> [Admin Dev, Philippe P. et Direction]
                if filtered_creator != '0' and filtered_creator is not None:
                    pnr_count = Pnr.objects.filter(Q(system_creation_date__gt=maximum_timezone), Q(agent_id=filtered_creator)).filter(is_invoiced=is_invoiced).count()
                elif filtered_creator == '0' or filtered_creator is None:
                    pnr_count = Pnr.objects.filter(Q(system_creation_date__gt=maximum_timezone)).filter(is_invoiced=is_invoiced).all().count()
            else:
                if request.user.id in [4, 5]: #==> [Farida et Mouniati peuvent voir chacun l'ensemble de leurs pnr]
                    pnr_list = []
                    pnr_count = 0
                    issuing_users = request.user.copied_documents.all()
                    for issuing_user in issuing_users:
                        pnr = Pnr.objects.filter(number=issuing_user.document).filter(Q(system_creation_date__gt=maximum_timezone)).filter(is_invoiced=is_invoiced).first()
                        if pnr not in pnr_list and pnr is not None:
                            pnr_list.append(pnr)
                
                    pnr_obj = Pnr.objects.filter(Q(agent_id=filtered_creator)).filter(Q(system_creation_date__gt=maximum_timezone)).filter(is_invoiced=is_invoiced)
                    
                    for pnr in pnr_obj:
                        if pnr not in pnr_list:
                            pnr_list.append(pnr)
                            
                    pnr_count = len(pnr_list)
                else:
                    pnr_list = []
                    pnr_count = 0
                    issuing_users = request.user.copied_documents.all()
                    
                    if is_invoiced is not None:
                        for issuing_user in issuing_users:
                            pnr = Pnr.objects.filter(number=issuing_user.document).filter(Q(system_creation_date__gt=maximum_timezone)).filter(is_invoiced=is_invoiced).first()
                            if pnr not in pnr_list and pnr is not None:
                                pnr_list.append(pnr)
                                
                        pnr_obj = Pnr.objects.filter(Q(agent_id=filtered_creator) | Q(agent_id=None)).filter(Q(system_creation_date__gt=maximum_timezone)).filter(is_invoiced=is_invoiced).all()
                        for pnr in pnr_obj:
                            if pnr not in pnr_list:
                                pnr_list.append(pnr)
                        
                        pnr_count = len(pnr_list)
        
        # Filter PNR with datetime greater than maximum_timezone
        return pnr_count
    except:
        return 0
    
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
    passenger_invoices = PassengerInvoice.objects.filter(pnr=pnr.id, client=customer_id).exclude(Q(ticket=None) | Q(other_fee=None)).exclude(status='quotation')

    is_invoice = []

    if passenger_invoices.exists():
        for passenger in passenger_invoices:
            is_invoice.append(passenger.is_invoiced)
        if False in is_invoice:
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
                    list_ticket_tax = []
                    list_ticket_transport_cost = []
                    list_ticket_total = []
                    
                    list_fee_type = []
                    list_fee_cost = []
                    list_fee_tax = []
                    list_fee_total = []
                    
                    list_other_fee_type = []
                    list_other_fee_cost = []
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
                                        
                                    fee = {
                                        "type": list_fee_type,
                                        "cost": list_fee_cost,
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
                                    
                                    list_other_fee_type.append("EMD")  
                                    
                                    other_fee = {
                                        "designation": list_other_fee_designation,
                                        "passenger": list_other_fee_passenger,
                                        "cost": list_other_fee_cost,
                                        "type": list_other_fee_type,
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
                    list_ticket_tax = []
                    list_ticket_transport_cost = []
                    list_ticket_total = []
                    
                    list_fee_type = []
                    list_fee_cost = []
                    list_fee_tax = []
                    list_fee_total = []
                    
                    list_other_fee_type = []
                    list_other_fee_cost = []
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
                                        
                                    fee = {
                                        "type": list_fee_type,
                                        "cost": list_fee_cost,
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
                                    
                                    list_other_fee_type.append("EMD")  
                                    
                                    other_fee = {
                                        "designation": list_other_fee_designation,
                                        "passenger": list_other_fee_passenger,
                                        "cost": list_other_fee_cost,
                                        "type": list_other_fee_type,
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
    from AmadeusDecoder.models.pnr.Pnr import Pnr
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
    if reduce_pnr_fee_requests.exists():
        for reduce_pnr_fee_request in reduce_pnr_fee_requests:
            if reduce_pnr_fee_request.status == 0:
                return True
            else:
                False
    else:
        return False
        
