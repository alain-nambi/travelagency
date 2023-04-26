from datetime import date

from django.db.models import Q

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.utilities.SendMail import Sending

'Get all pnr create of the day'
def get_daily_pnr():
    today = date.today()
    pnrs = Pnr.objects.filter(Q(system_creation_date__day=today.strftime('%d')), Q(system_creation_date__month=today.strftime('%m'))).order_by('-system_creation_date')
    # pnrs = Pnr.objects.filter(Q(system_creation_date__day='15'), Q(system_creation_date__month=today.strftime('%m'))).order_by('-system_creation_date')
    return pnrs

'Get the list of all pnr issued of the day and group them by user id'
def count_daily_pnr_issued(pnr, user):
    number = 0
    pnr_issued = pnr.filter(status="Emis")
    for item in pnr_issued:
        if item.get_emit_agent().id == user.id:
            number += 1
    return number
    


'Get the list of all pnr unissued of the day and group them by user id'
def count_daily_pnr_unissued(pnr, user):
    dict_pnr_issued, dict_pnr_unissued = {}, {}
    number = 0
    new_user = User.objects.all()
    pnr_unissued = pnr.filter(status="Non émis")
    for item in pnr_unissued:
        if item.agent.id == user.id:
            number += 1
        elif item.agent.id is None and item.agent_code == user.gds_id:
            number += 1
        elif item.agent.id is None and item.agent_code == user.email:
            number += 1
        elif item.agent.id is None and item.agent_code is not None and new_user.filter(gds_id=item.agent_code) is None:
            number += 1
    
    return number

def unique(pnrs) :
    array_unique = []

    for pnr in pnrs :
        if pnr not in array_unique and pnr != '' :
            array_unique.append(pnr)

    return array_unique

def get_users_that_havent_create_pnr(pnrs_users_creation, others_users) :
    users = []
    directions = [20,41]

    for user in others_users :
        if user.id not in pnrs_users_creation and user.id not in directions :
            users.append(user)

    return users

def notify_direction(pnrs):
    today = date.today()
    directions = User.objects.filter(role=2)
    others_users = User.objects.filter(~Q(role=1))
    recipients = []

    pnr_daily_issued = Pnr.objects.filter(Q(system_creation_date__day=today.strftime('%d')), Q(system_creation_date__month=today.strftime('%m')), Q(status_value=0)).order_by('-system_creation_date').count()

    pnr_daily_unissued = Pnr.objects.filter(Q(system_creation_date__day=today.strftime('%d')), Q(system_creation_date__month=today.strftime('%m')), Q(status_value=1)).order_by('-system_creation_date').count()

    for user in directions:
        recipients.append(user.email)

    # Get pnrs's users creation
    pnrs_users = [ pnr.agent.id if pnr.agent is not None else pnr.agent_code for pnr in pnrs ]
    pnrs_without_user = []
    for pu in pnrs :
        if pu.agent is None and pu.agent_code == '' :
            pnrs_without_user.append(pu.number)
    print(pnrs_without_user)
    print(pnrs_users)
    pnrs_users_creation = unique(pnrs_users)
    print(pnrs_users_creation)

    # others = ['nasolo@phidia.onmicrosoft.com']
    others = [
            'missoufali@agences-issoufali.com',
            'pp@phidia.onmicrosoft.com'
            'tahina@phidia.onmicrosoft.com',
            'mihaja@phidia.onmicrosoft.com',
            'nasolo@phidia.onmicrosoft.com',
            ]

    for item in others:
        recipients.append(item)

    subject = "Rapport des PNR créés du jour"

    message = """
                <table style= "border-collapse: collapse;width: 80%; margin-left:auto; margin-right:auto;">
                    <tr>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;text-align:left;">Utilisateur</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">PNR créés</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">PNR émis</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd; width:20%;">PNR non émis</th>
                    </tr>
    """
    list_user_that_have_create = []
    list_user_that_havent_create = []
    sum_number_created = 0
    sum_number_issued =0
    sum_number_unissued =0

    for user_id in pnrs_users_creation:
        user = User.objects.get(pk=user_id)
        username = user.username if user is not None else user_id
        number_created = 0
        number_issued = 0 
        number_unissued = 0
        for pnr in pnrs:
            if pnr.status_value == 0:
                if pnr.get_emit_agent() is not None :
                    if pnr.get_emit_agent().id == user_id:
                        number_issued += 1
                else :
                    if pnr.agent is not None and pnr.agent.id == user_id:
                        number_issued += 1
                        

                if pnr.agent is not None and pnr.agent.id == user_id:
                    number_created += 1
                
            elif pnr.status_value == 1 :
                if pnr.agent.id == user_id:
                    number_unissued += 1
                    number_created += 1
            else :
                print("PNR: ",pnr.number)
        # if number_issued > 0 or number_unissued > 0 :
        list_user_that_have_create.append([username, number_created, number_issued, number_unissued])
        sum_number_created += number_created
        sum_number_issued += number_issued
        sum_number_unissued += number_unissued
        # elif number_created == 0 and number_issued == 0 and number_unissued == 0:
        #     list_user_that_havent_create.append(username)

    print("sum_number_created: ",sum_number_created)
    print("sum_number_issued: ",sum_number_issued)
    print("sum_number_unissued: ",sum_number_unissued)

    list_user_that_havent_create = get_users_that_havent_create_pnr(pnrs_users_creation, others_users)
    
    for item in list_user_that_havent_create:
        message += """
                        <tr>
                            <td style="border: 1px solid #dddddd;padding: 8px;"><strong>{username}</strong></td>
                            <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">0</td>
                            <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">0</td>
                            <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">0</td>
                        </tr>
                    """.format(username= item)

    for item in sorted(list_user_that_have_create,key=lambda l:l[1]):
        message += """
                        <tr>
                            <td style="border: 1px solid #dddddd;padding: 8px;"><strong>{username}</strong></td>
                            <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{number_created}</td>
                            <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{number_issued}</td>
                            <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{number_unissued}</td>
                        </tr>
                    """.format(username= item[0], number_created=item[1], number_issued=item[2], number_unissued=item[3])
    # Total
    message += """
                        <tr>
                            <td style="background-color: #dddddd;"><strong>Total</strong></td>
                            <td style="padding: 8px;text-align:center;background-color: #dddddd;">{total_created}</td>
                            <td style="padding: 8px;text-align:center;background-color: #dddddd;">{total_issued}</td>
                            <td style="padding: 8px;text-align:center;background-color: #dddddd;">{total_unissued}</td>
                        </tr>
                    """.format(total_created= pnrs.count(), total_issued=pnr_daily_issued, total_unissued=pnr_daily_unissued)

    message += "</table>"

    body = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Notification OPC</title>
                
                </head>
                <body>
                    <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                        Bonjour,<br /><br />
                        Vous trouverez ci-dessous la liste des PNR créés en date du {}. 
                    </p> </br>
                    <p>
                        {}
                    </p>
                    
                    <p>
                        PNR qui n'ont pas de créateur: {}
                    </p>
                    <p>
                        Bien cordialement,
                    </p>
                    <p>
                        <strong>Ceci est un email automatique, merci de ne pas répondre.</strong></br>
                        Services supports : mihaja@phidia.onmicrosoft.com et  tahina@phidia.onmicrosoft.com
                    </p> 
                </body>
                </html>
            """.format(today.strftime('%d-%m-%Y'), message, ', '.join(pnrs_without_user))

    Sending.send_email(
        "issoufali.pnr@outlook.com",
        recipients,
        subject,
        body
    )


