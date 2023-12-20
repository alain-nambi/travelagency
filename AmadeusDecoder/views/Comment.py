from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
from AmadeusDecoder.models.pnr.Passenger import Passenger

from AmadeusDecoder.models.pnr.Pnr import Pnr 
from AmadeusDecoder.models.utilities.Comments import Anomalie, Comment, Response, NotFetched
from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.utilities.SendMail import Sending
from AmadeusDecoder.models.invoice.Ticket import Ticket

from datetime import date, timedelta
from django.utils import timezone

from django.db.models import Q
from django.core.serializers import serialize
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
         ["nasolo@phidia.onmicrosoft.com",
         "famenontsoa@outlook.com",
         "pp@phidia.onmicrosoft.com",
         "tahina@phidia.onmicrosoft.com",
         "alain@phidia.onmicrosoft.com"],
         subject,
         message
    )

    return JsonResponse({'comment': 'Data successfully sent to database'})

@login_required(login_url='index')
def comment_list(request):
    maximum_timezone = "2023-01-01 01:00:00.000000+03:00"
    date_before_30_days = str(date.today() - timedelta(days=60)) + " " + "01:00:00.000000+03:00"
    
    context = {}
    comments = Comment.objects.filter(Q(creation_date__gt=maximum_timezone) & Q(creation_date__gt=date_before_30_days)).order_by('-creation_date')
    context['comments'] = comments

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
                [comments.user_id.email,
                    "nasolo@phidia.onmicrosoft.com",
                    "alain@phidia.onmicrosoft.com",
                    "famenontsoa@outlook.com",
                    "pp@phidia.onmicrosoft.com",
                    "tahina@phidia.onmicrosoft.com"
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
                ["nasolo@phidia.onmicrosoft.com",
                "alain@phidia.onmicrosoft.com",
                "famenontsoa@outlook.com",
                "pp@phidia.onmicrosoft.com",
                "tahina@phidia.onmicrosoft.com"],
                subject,
                message
            )
    return JsonResponse({})

# ----------------- anomalie: réponse automatique -----------------
@login_required(login_url='index')
def verif_ticket(request):
    if request.method == 'POST':
        ticket_number = request.POST.get('ticket_number')
        ticket = Ticket.objects.filter(number=ticket_number)
        
        if ticket.exists():
            return JsonResponse({'verif': True})
    return JsonResponse({'verif': False})

@login_required(login_url='index')
def get_passengers_by_pnr(request):
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

        context['passengers'] = passengers_data

    return JsonResponse({'context': context})

@login_required(login_url='index')
def getPassengerById(request):
    if request.method == 'POST':
        passenger_id = request.POST.get('passenger_id')
        try:
            passenger = Passenger.objects.get(pk=passenger_id)
            passenger_dict = {
                'id': passenger.id,
                'name': passenger.name,
                'surname': passenger.surname,
            }

            return JsonResponse({'passenger': passenger_dict})
        except Passenger.DoesNotExist:
            return JsonResponse({'error': 'Passenger not found'}, status=404)

@login_required(login_url='index')
def save_ticket_anomalie(request):
    if request.method == 'POST':
        ticket_number = request.POST.get('ticket_number')
        montant_hors_taxe = request.POST.get('montant_hors_taxe')
        taxe = request.POST.get('taxe')
        pnr_id = request.POST.get('pnr_id')
        passenger_id = request.POST.get('passenger_id')
        segment = request.POST.get('segment')
        
        pnr = Pnr.objects.filter(id=pnr_id).first()
            
        user_id = request.POST.get('user_id')
        user = User.objects.filter(id= user_id).first()
        
        if passenger_id is None and segment is None:
            info = {"ticket_number": ticket_number, "montant": montant_hors_taxe, "taxe": taxe, "ticket_status":0} # ticket_status : 0 ticket existant , 1 ticket non existant
            
        else:
            info = {"ticket_number": ticket_number, "montant": montant_hors_taxe, "taxe": taxe, "passenger_id":passenger_id, "segment": segment, "ticket_status":1} # ticket_status : 0 ticket existant , 1 ticket non existant
            
        anomalie = Anomalie(pnr=pnr, categorie='Billet non remonté', infos=info, issuing_user = user)
        anomalie.save()   
        return JsonResponse('ok',safe=False)
    

@login_required(login_url='index')
def get_all_anomalies(request):
    anomalies = Anomalie.objects.all()
    context = {'anomalies': anomalies}
    return render(request,'anomalies-list.html',context)
    
@login_required(login_url='index')
def update_ticket(request):
    if request.method == 'POST':
        ticket_number = request.POST.get('ticket_number')
        montant = request.POST.get('montant')
        taxe = request.POST.get('taxe')
        anomalie_id = request.POST.get('anomalie_id')
        pnr_id = request.POST.get('pnr_id')
        
        ticket = Ticket.objects.filter(number=ticket_number).first()
        if ticket is not None:
            ticket.transport_cost = montant
            ticket.tax = taxe
            ticket.total = float(montant) + float(taxe)
            ticket.ticket_status = 1
            ticket.save()
            
            anomalie = Anomalie.objects.filter(id=anomalie_id).first()
            anomalie.status = 1
            anomalie.save()
            return JsonResponse('ok', safe=False)
        else:
            passenger_id = request.POST.get('passenger_id')
            segment = request.POST.get('segment')
            ticket = Ticket(number=ticket_number, transport_cost=montant, tax=taxe, total = float(montant) + float(taxe), ticket_status=1, pnr_id=pnr_id, passenger_id=passenger_id, segment= segment)
        return JsonResponse('not ok', safe=False)
            
            
            # ,ticket_gp_status=,exch_val=,rfnd_val=,passenger_type=,fare_type=,is_prime=, is_regional=,is_no_adc=,is_subjected_to_fees=,is_invoiced=,is_refund=,is_deposit=,is_issued_outside=,