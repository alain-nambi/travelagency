import ast
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse


from django.contrib.auth.decorators import login_required
from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
from AmadeusDecoder.models.invoice.TicketPassengerSegment import TicketPassengerSegment
from AmadeusDecoder.models.pnr.Passenger import Passenger

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.pnrelements.Airline import Airline
from AmadeusDecoder.models.pnrelements.PnrAirSegments import PnrAirSegments 
from AmadeusDecoder.models.utilities.Comments import Anomalie, Comment, Response, NotFetched
from AmadeusDecoder.models.user.Users import User, UserCopying
from AmadeusDecoder.utilities.SendMail import Sending
from AmadeusDecoder.models.invoice.Ticket import Ticket

from datetime import date, timedelta
from django.utils import timezone

from django.db.models import Q
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

@login_required(login_url='index')
def comment(request):
    if request.method == 'POST':
        comment_value = request.POST.get('comment')
        pnr_id = request.POST.get('pnr_id')
        pnr_element = Pnr.objects.get(pk=int(pnr_id))
        user_element = User.objects.get(pk=int(request.user.id))
        comment = Comment(pnr_id=pnr_element, user_id=user_element, comment=comment_value)
        comment.save()

        today = date.today()

        subject = "Anomalies sur la récupération des PNR reportées le " + str(today)

        message = """
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Anomalies des PNR</title>
                    </head>
                    <body>
                        <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                            Bonjour,
                        </p>
                        <p>
                            Anomalie : {} </br>
                            PNR concerné : {} </br>
                            Reporté par {} </br>
                        </p>
                        <p> Cordialement, </p>
                    </body>
                    </html>
                """.format(comment_value, pnr_element.number, user_element.username)

    Sending.send_email(
        "anomalie.issoufali.pnr@gmail.com",
        [
            "pp@phidia.onmicrosoft.com",
            "tahina@phidia.onmicrosoft.com",
            "alain@phidia.onmicrosoft.com",
            "maphiesarobidy@outlook.fr",
            "naval@phidia.onmicrosoft.com",
            "olyviahasina.razakamanantsoa@outlook.fr",
            "haryzoely@phidia.onmicrosoft.com"
        ],
         subject,
         message
    )

    return JsonResponse({'comment': 'Data successfully sent to database'})

@login_required(login_url='index')
def comment_list(request):
    maximum_timezone = "2023-01-01 01:00:00.000000+03:00"
    
    context = {}
    comments = Comment.objects.filter(Q(creation_date__gt=maximum_timezone)).order_by('-creation_date')
    context['comments'] = comments
    comments_count = comments.count()
    
    object_list = context['comments']
    row_num = request.GET.get('paginate_by', 50) or 50
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, row_num)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger: 
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {'page_obj': page_obj, 'row_num': row_num, 'pnr_count' : comments_count}

    return render(request, 'comment-list.html', context)


@login_required(login_url='index')
def comment_detail(request, comment_id):
    context = {}
    comments = Comment.objects.get(pk=comment_id)
    context['comments'] = comments

    if request.method == 'POST':
        if 'comment-response' in request.POST:
            comment_response = request.POST.get('comment-response')
            user_id = User.objects.get(pk=int(request.user.id))
            pnr_id = Pnr.objects.get(pk=int(comments.pnr_id.id))
            response = Response(pnr_id=pnr_id, user_id=user_id, response=comment_response)
            response.save()

            subject = "Réponse sur l'anomalie du PNR: " + pnr_id.number

            message = """
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Anomalies des PNR</title>
                        </head>
                        <body>
                            <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                                Bonjour,
                            </p>
                            <p>
                                Anomalie : {} </br>
                                PNR concerné : {} </br>
                                Reporté par {} </br>
                                Réponse : {} 
                            </p>
                            <p> Cordialement, </p>
                        </body>
                        </html>
                    """.format(comments.comment, comments.pnr_id.number, comments.user_id.username, comment_response)

            Sending.send_email(
                "anomalie.issoufali.pnr@gmail.com",
                [   
                    comments.user_id.email,
                    "maphiesarobidy@outlook.fr",
                    "naval@phidia.onmicrosoft.com",
                    "alain@phidia.onmicrosoft.com",
                    "olyviahasina.razakamanantsoa@outlook.fr",
                    "pp@phidia.onmicrosoft.com",
                    "tahina@phidia.onmicrosoft.com",
                    "haryzoely@phidia.onmicrosoft.com"
                ],
                subject,
                message
            )
            return redirect('comment-list')
    context['responses'] = Response.objects.filter(pnr_id=int(comments.pnr_id.id))

    return render(request, 'comment-detail.html', context)


@login_required(login_url='index')
def update_comment_state(request):
    context = {}
    if request.method == 'POST':
        if 'comment_id' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = Comment.objects.filter(pk=int(comment_id))
            comment.update(state=True)

    context['comment'] = list(comment.values())
    return JsonResponse(context)

@login_required(login_url='index')
def get_pnr_not_fetched(request):
    if request.method == 'POST':
        if 'pnrNumber' in request.POST:
            pnr_number = request.POST.get('pnrNumber')
            user_follower = request.user.id
            if pnr_number != '' and pnr_number != None and not NotFetched.objects.filter(pnr_number=pnr_number).exists():
                follower = User.objects.get(pk=int(user_follower))
                pnr_not_fetched = NotFetched(pnr_number=pnr_number, follower=follower)
                pnr_not_fetched.save()

                pnr = NotFetched.objects.get(pnr_number=pnr_number)
                subject = "{date}".format(date=pnr.date_creation.strftime('%d-%m-%Y'))

                message = """
                            <!DOCTYPE html>
                            <html>
                            <head>
                                <title>PNR non remonté dans Gestion PNR</title>
                            </head>
                            <body>
                                <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                                    Bonjour,
                                </p>
                                <p>
                                    Ce PNR n'est pas remonté dans Gestion PNR </br>
                                    PNR concerné : {} </br>
                                    Reporté par {} </br> 
                                </p>
                                <p> Cordialement, </p>
                            </body>
                            </html>
                        """.format(pnr.pnr_number, pnr.follower.username)

            Sending.send_email_pnr_not_fetched(
                "anomalie.issoufali.pnr@gmail.com",
                [
                    "maphiesarobidy@outlook.fr",
                    "naval@phidia.onmicrosoft.com",
                    "alain@phidia.onmicrosoft.com",
                    "olyviahasina.razakamanantsoa@outlook.fr",
                    "pp@phidia.onmicrosoft.com",
                    "tahina@phidia.onmicrosoft.com",
                    "haryzoely@phidia.onmicrosoft.com"
                ],
                subject,
                message
            )
    return JsonResponse({})

# ----------------- anomalie: réponse automatique -----------------

@login_required(login_url='index')
def get_unshowed_tickets(request):
    context = {}
    if request.method == 'POST':
        pnr_id = request.POST.get('pnr_id')
        tickets_query = Ticket.objects.filter(pnr_id= pnr_id).filter((Q(transport_cost=0) & Q(tax=0) & Q(total=0)) | Q(is_no_adc=True)).all()
        tickets= []
        for ticket in tickets_query:
            ticket_data = {
                'ticket_id' : ticket.id,
                'pnr_id' : ticket.pnr_id,
                'number' : ticket.number,
                'transport_cost' : ticket.transport_cost,
                'taxe' : ticket.tax,
                'total' : ticket.total
            }
            tickets.append(ticket_data)
        context['tickets'] = tickets
        context['status'] = 200
    return JsonResponse(context)


@login_required(login_url='index')
def verif_ticket(request):
    if request.method == 'POST':
        ticket_number = request.POST.get('ticket_number')
        pnr_id = request.POST.get('pnr_id')
        ticket = Ticket.objects.filter(number=ticket_number).first()
        
        response = {'verif': 'False'}
        
        if ticket is not None:
            if int(ticket.pnr_id) == int(pnr_id):
                if ticket.is_no_adc:
                    response['verif'] = 'is_no_adc'
                elif ticket.total > 0 and ticket.ticket_status == 1:
                    response['verif'] = 'ticket_already_exist'
                else:
                    response['verif'] = 'True'
            else:
                response['verif'] = {
                    'exist': True,
                    'pnr': ticket.pnr.number,
                }
        else:
            response['verif'] = 'False'

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid request'})

# get by pnr
@login_required(login_url='index')
def getPassengersAndSegmets(request):
    context = {}

    if request.method == 'POST':
        pnr_id = request.POST.get('pnr_id')
        pnr = Pnr.objects.get(pk=pnr_id)
        
        passengers = pnr.passengers.filter(passenger__passenger_status=1).order_by('id')
        passengers_data = []
        
        for passenger in passengers:
            passenger_data = {
                'passenger_id': passenger.passenger.id,
                'passenger_name': passenger.passenger.name,
                'passenger_surname': passenger.passenger.surname,
            }
            passengers_data.append(passenger_data)
            
        pnr = Pnr.objects.get(pk=pnr_id)
        air_segments = pnr.segments.filter(segment_type='Flight', air_segment_status=1).all().order_by('segmentorder')
        segments_data = []

        for air_segment in air_segments:
            segment_data = {
                'segment_id' : air_segment.id,
                'segment' : air_segment.segmentorder,
                'vol' : air_segment.servicecarrier.iata,
                'vol_number' : air_segment.flightno
            }
            segments_data.append(segment_data)

       

        context['passengers'] = passengers_data
        context['segments'] = segments_data
        

    return JsonResponse({'context': context})

@login_required(login_url='index')
def getPassengerAndSegmentById(request):
    if request.method == 'POST':
        passenger_id = request.POST.get('passenger_id')
        segment_id = request.POST.get('segment_id')
        
        try:
            passenger = Passenger.objects.get(pk=passenger_id)
            passenger_dict = {
                'id': passenger.id,
                'name': passenger.name,
                'surname': passenger.surname,
            }
            print(segment_id)
            segment = PnrAirSegments.objects.get(id=segment_id)
            segment_dict = {
                'segmentorder': segment.segmentorder,
                'vol': segment.servicecarrier.iata,
                'vol_number': segment.flightno,
            }
            
            return JsonResponse({'passenger': passenger_dict, 'segment': segment_dict})
        except Passenger.DoesNotExist:
            return JsonResponse({'error': 'Passenger not found'}, status=404)

# enregistrement de l'anomalie billet non remonté
@login_required(login_url='index')
def save_ticket_anomalie(request):
    if request.method == 'POST':
        if "listNewTicketAnomalyInfo" in request.POST:
            new_tickets = json.loads(request.POST.get("listNewTicketAnomalyInfo"))

            ticket_number = new_tickets[0]['ticket_number']
            
            # check number ticket length
            if len(ticket_number) > 17:
                return JsonResponse({'error':'ticket number > 17 '})
        
            # get all data
            montant_hors_taxe = new_tickets[0]['montant_hors_taxe']
            taxe = new_tickets[0]['taxe']
            pnr_id = new_tickets[0]['pnr_id']
            passenger_id = new_tickets[0]['passenger_id']
            segments = []
            ticket_type = new_tickets[0]['ticket_type']
        
            for segment in new_tickets[0]['segment']:
                segments.append(segment.get('value'))

            pnr = Pnr.objects.filter(id=pnr_id).first()
                
            user_id = new_tickets[0]['user_id']
            
            info = {"ticket_number": ticket_number, "montant": montant_hors_taxe, "taxe": taxe, "passenger_id":passenger_id, "segment": segments, "ticket_status":1, 'ticket_type':ticket_type, 'fee': str(new_tickets[0]['fee']).capitalize()} # ticket_status : 0 ticket existant , 1 ticket non existant
        
        else:
            ticket_number = request.POST.get('ticket_number')
            montant_hors_taxe = request.POST.get('montant_hors_taxe')
            taxe = request.POST.get('taxe')
            pnr_id = request.POST.get('pnr_id')
            user_id = request.POST.get('user_id')
            
            pnr = Pnr.objects.filter(id=pnr_id).first()
            
            info = {"ticket_number": ticket_number, "montant": montant_hors_taxe, "taxe": taxe, "ticket_status":0} # ticket_status : 0 ticket existant , 1 ticket non existant
            
        if montant_hors_taxe == "" or taxe == "":
            return JsonResponse(
                {
                    'error': f'Veuillez remplir toutes les champs nécessaires pour le billet [{ticket_number}]',
                    'status': 'error'
                }
            )
        
        user = User.objects.filter(id= user_id).first()

        anomalie = Anomalie(pnr=pnr, categorie='Billet non remonté', infos=info, issuing_user = user, creation_date=timezone.now())
        anomalie.save()   
        anomalie_id = anomalie.id
        response_data = {'status':'ok','anomalie_id':anomalie_id}

        # if user.role.id in [1, 2]:
        #     response_data['accept'] = True
        # else:
        #     response_data['accept'] = False
        
        # Accepter les demandes pour les billets archivés pour toutes les utilisateurs
        response_data['accept'] = True
        
        return JsonResponse(response_data,safe=False)


@login_required(login_url='index')
def get_all_anomalies(request):
    anomalies = Anomalie.objects.exclude(status=3)
    context = {}
    context['anomalies'] = anomalies
    object_list = context['anomalies']
    row_num = request.GET.get('paginate_by', 20) or 20
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, row_num)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger: 
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        
    context = {'page_obj': page_obj, 'row_num': row_num}
    
    return render(request,'anomalies-list.html',context)

@login_required(login_url='index')
def anomaly_details(request, pnr_id):
    context={}
    anomalie = Anomalie.objects.filter(pnr_id=pnr_id).exclude(status=3)
    context['anomalies'] = anomalie
    context['pnr_id'] = pnr_id
    return render(request, 'anomalie-details.html', context)

# updating or saving ticket from anomalie 'Billet non remonté'
@login_required(login_url='index')
def update_ticket(request):
    if request.method == 'POST':
        anomalie_id = request.POST.get('anomalie_id')

        anomalie = Anomalie.objects.get(pk=anomalie_id)
        issuing_user = anomalie.issuing_user
        ticket = Ticket.objects.filter(number=anomalie.infos.get('ticket_number')).first()
        pnr = Pnr.objects.get(pk=anomalie.pnr_id)
        
        if ticket is not None:
            # update the existing ticket
            ticket.transport_cost = anomalie.infos.get('montant')
            ticket.tax = anomalie.infos.get('taxe')
            ticket.total = float(anomalie.infos.get('montant')) + float(anomalie.infos.get('taxe'))
            # set is_no_adc if total = 0
            if ticket.total == 0:
                ticket.is_no_adc = True
            ticket.ticket_status = 1
            ticket.emitter = None
            ticket.issuing_date = datetime.now()
            ticket.save()
           
        else:
            # Create a new ticket
            ticket = Ticket()
            ticket.transport_cost=anomalie.infos.get('montant')
            ticket.number=anomalie.infos.get('ticket_number')
            ticket.tax=anomalie.infos.get('taxe')
            ticket.total = float(anomalie.infos.get('montant')) + float(anomalie.infos.get('taxe'))
            # set is_no_adc if total = 0
            if ticket.total == 0:
                ticket.is_no_adc = True
            ticket.ticket_status=1
            ticket.pnr_id=anomalie.pnr_id
            ticket.passenger_id=anomalie.infos.get('passenger_id')
            ticket.ticket_type=anomalie.infos.get('ticket_type')
            ticket.is_subjected_to_fees=anomalie.infos.get('fee')
            ticket.emitter=None
            ticket.issuing_date=datetime.now()
            ticket.save()
            
            # get the corresponding segment
            segment_id = ast.literal_eval(anomalie.infos.get('segment'))
            if segment_id != "":
                if isinstance(segment_id, list):
                    for element in segment_id:
                        segment = PnrAirSegments.objects.get(pk=element)
                        ticket_passenger = TicketPassengerSegment(ticket=ticket,segment=segment)
                        ticket_passenger.save()
                elif isinstance(segment_id, int):
                    segment = PnrAirSegments.objects.get(pk=segment_id)
                    ticket_passenger = TicketPassengerSegment(ticket=ticket,segment=segment)
                    ticket_passenger.save()

        last_user_copying= UserCopying.objects.filter(document=pnr.number).last()
        
        if last_user_copying is not None:
            user_copying = User.objects.get(pk=last_user_copying.user_id.id)
            new_user_copying = UserCopying(document=pnr.number,user_id=user_copying)
            new_user_copying.save()
        
        anomalie.status = 1
        anomalie.response_date = timezone.now()
        anomalie.save()
   
        return JsonResponse('ok', safe=False)

@login_required(login_url='index')        
def refuse_anomaly(request):
    if request.method == 'POST':
        anomalie_id = request.POST.get('anomalie_id')
        anomalie = Anomalie.objects.get(pk=anomalie_id)
        anomalie.status = 2
        anomalie.response_date = timezone.now()
        anomalie.admin_id = request.user
        anomalie.save()
        return JsonResponse('ok',safe=False)
            
@login_required(login_url='index')        
def drop_anomaly(request):
    if request.method == 'POST':
        anomalie_id = request.POST.get('anomalie_id')
        anomalie = Anomalie.objects.get(pk=anomalie_id)
        anomalie.status = 3
        anomalie.admin_id = request.user
        anomalie.save()
        return JsonResponse('ok',safe=False)
    
@login_required(login_url='index')
def updateAnomaly(request):
    if request.method == 'POST':
        ticket = request.POST.get('ticket')
        montant = request.POST.get('montant')
        taxe = request.POST.get('taxe')
        anomaly_id = request.POST.get('anomaly_id')
        print('-------------------ANOMALY ----------------------------')
        print(montant)
        anomaly = Anomalie.objects.get(pk=anomaly_id)
        anomaly.infos['ticket_number'] = ticket
        anomaly.infos['montant'] = montant
        anomaly.infos['taxe'] = taxe
        
        anomaly.save()
        return JsonResponse('ok',safe=False)
        