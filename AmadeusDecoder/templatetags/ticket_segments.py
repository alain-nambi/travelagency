'''
Created on 12 Sep 2022

@author: Famenontsoa
'''

from django import template

from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.TicketPassengerTST import TicketPassengerTST
from AmadeusDecoder.models.invoice.Fee import OthersFee

register = template.Library()

@register.filter(name='segment')
def get_segment_by_ticket(ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    segments = ''
    for passengerSegment in ticket.ticket_parts.all().order_by('segment__id'):
        segments += passengerSegment.segment.segmentorder + '-'
    for ssrs in  ticket.ticket_ssrs.all():
        segments += ssrs.ssr.order_line + '-'
    return segments[:-1]

@register.filter(name='route')
def get_route_by_ticket(ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    route = ''
    for passengerSegment in ticket.ticket_parts.all().order_by('segment__id'):
        if passengerSegment.segment.segment_type == 'SVC':
            route = 'SVC'
        else:
            if passengerSegment.segment.codeorg is not None:
                route += passengerSegment.segment.codeorg.iata_code + '/' + passengerSegment.segment.codedest.iata_code
            route += '//'
    if route.endswith('//'):
        route = route.removesuffix('//')
    return route

@register.filter(name='tst_passenger')
def get_tst_passengers(tst_id):
    tst = Ticket.objects.filter(id=tst_id).first()
    passengers = ''
    for ticket_passenger_tst in tst.ticket_tst_parts.all():
        passengers += ticket_passenger_tst.passenger.order + '-'
    return passengers[:-1]

@register.filter(name='fee')
def get_ticket_fees(ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    if len(ticket.fees.all()) > 0:
        return ticket.fees.all()[0]
    else:
        return None

# other fee related to a ticket
@register.filter(name='ticket_other_fee')
def get_ticket_other_fees(ticket):
    temp_other_fee = OthersFee.objects.filter(ticket=ticket).first()
    if temp_other_fee is not None:
        return temp_other_fee
    else:
        return None

@register.filter(name='other_fee_fee')
def get_other_fee_fees(other_fee_id):
    other_fee = OthersFee.objects.filter(id=other_fee_id).first()
    if len(other_fee.fees.all()) > 0:
        return other_fee.fees.all()[0]
    else:
        return None
    
@register.filter(name='tickets')
def get_ticket_tickets(pnr):
    tickets = pnr.tickets.all()
    ticket_number = []
    for ticket in tickets:
        ticket_number.append(ticket.number)
    return ticket_number