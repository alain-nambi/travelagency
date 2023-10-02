from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from AmadeusDecoder.models.pnr.Pnr import Pnr 
from AmadeusDecoder.models.utilities.Comments import Comment, Response, NotFetched
from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.utilities.SendMail import Sending
from datetime import date, timedelta
from django.utils import timezone

from django.db.models import Q


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
