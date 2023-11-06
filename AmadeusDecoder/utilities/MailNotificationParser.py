from datetime import datetime, timezone, timedelta, time
from dateutil import tz

from django.db.models import Q

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.utilities.SendMail import Sending

class MailNotification():

    def passenger_segment_missing_notification(time_now):
        pnr_segment_missing = Pnr.objects.filter(system_creation_date = (time_now - timedelta(minutes=1))).filter(Q(state=2) | Q(state=3))
        recipients = []
        if pnr_segment_missing.exists():
            for pnr in pnr_segment_missing:
                tickets = pnr.tickets.filter(state=2).all()
                tickets_passenger_segment = []
                for ticket in tickets :
                    res = ''
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

                message = ""
                recipient = ""
                subject = "Application Gestion PNR - Tarifications billets manquantes"
                message += """
                            <!DOCTYPE html>
                            <html>
                            <head>
                                <title>Mail de tarification billet manquant</title>
                            </head>
                            <body>
                                <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                                    Bonjour,
                                </p>
                                <p>
                                    Le mail de tarification pour le PNR: {pnr} n'a pas encore été envoyé,
                                    Les billets et segments concernés: {segment},
                                    Date de création du PNR: {date}
                                </p>
                                <p> Cordialement, </p>
                            </body>
                            </html>
                        """.format(pnr=pnr.number, segment=tickets_passenger_segment, date=pnr.system_creation_date.strftime('%d-%m-%Y %H-%M-%S'))

                if pnr.agent is not None:
                    recipients = [pnr.agent.email, "nasolo@phidia.onmicrosoft.com"]

                Sending.send_email(
                        "issoufali.pnr@outlook.com",
                        recipients,
                        subject,
                        message
                    )

    def pnr_missing_notification(time_now):
        pnr_missing = Pnr.objects.filter(system_creation_date = (time_now - timedelta(minutes=1)), state = 1)
        if pnr_missing.exists():
            for pnr in pnr_missing:
                message = ""
                recipient = ''
                subject = "Application Gestion PNR - PNR manquantes"
                message += """
                            <!DOCTYPE html>
                            <html>
                            <head>
                                <title>Mail de PNR manquant</title>
                            </head>
                            <body>
                                <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                                    Bonjour,
                                </p>
                                <p>
                                    Mail de PNR manquant pour le PNR: {pnr}
                                    Date de création : {date}
                                </p>
                                <p> Cordialement, </p>
                            </body>
                            </html>
                        """.format(pnr=pnr.number, date=pnr.system_creation_date.strftime('%d-%m-%Y %H-%M-%S'))

                if pnr.agent_id is not None:
                    recipient = [pnr.agent_id.email, "nasolo@phidia.onmicrosoft.com", "tahina@phidia.onmicrosoft.com", "nasolo@phidia.onmicrosoft.com"]
                Sending.send_email(
                        "issoufali.pnr@outlook.com",
                        recipient,
                        subject,
                        message
                    )

    def pnr_upload_notification(now):
        def weekend_processing_time(minutes):
            datetime_before_minutes = now - timedelta(minutes=minutes)

            print("============================== PNR UPLOAD NOTIFICATION ==============================")
            
            # We filter pnr with creation date greater than or equal to datetime_before_minutes
            pnr_upload = Pnr.objects.filter(system_creation_date__gte=datetime_before_minutes)   
            
            # Get time from datetime python's class
            time_now = now.time() 
            start_date = time(8, 15) # => 08:15:00
            end_date = time(17, 15)  # => 17:15:00
            
            date = datetime_before_minutes.strftime('%d-%m-%Y')
            hours = datetime_before_minutes.strftime('%H:%M:%S')

            print(f"NOW: {time_now}, START_DATE: {start_date}, END_DATE: {end_date}, DATE: {date}, HOURS: {hours}")
            
            if start_date <= time_now <= end_date:
                if not pnr_upload.exists():
                    message = ""
                    subject = f"PNR non remontés dans l'application le {date}"
                    message += f"""
                                <!DOCTYPE html>
                                <html>
                                <head>
                                    <title>Mail pour les PNR non remontés</title>
                                </head>
                                <body>
                                    <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                                        Bonjour,
                                    </p>
                                    <p>
                                        Aucun PNR n'a été remonté dans l'application entre {hours} et {time_now}.
                                    </p>
                                    <p>
                                        <strong>
                                            <u>Date d'envoi</u>:
                                        </strong>
                                        {date}
                                    </p>
                                    <p> Cordialement, </p>
                                </body>
                                </html>
                            """

                    try:
                        Sending.send_email(
                            "issoufali.pnr@outlook.com",
                            [
                                "pp@phidia.onmicrosoft.com",
                                "tahina@phidia.onmicrosoft.com",
                                "alain@phidia.onmicrosoft.com",
                                "nasolo@phidia.onmicrosoft.com",
                                "famenontsoa@outlook.com",
                            ],
                            subject,
                            message
                        )
                    except Exception as e:
                        print(f"Error sending pnr not sent to GP : {e}")
                        raise e
                else:
                    print(f"📢 Pnr is already up to date on {date}, {time_now}")
            else:
                print('📢 The time is outside of working hours')
        
        try:
            if now.weekday() in [0, 1, 2, 3, 4]: # [Lundi, Mardi, Mercredi, Jeudi, Vendredi]
                print("Not weekend day")
                weekend_processing_time(10)
            if now.weekday() in [5]: # [Samedi]
                print("Saturday day")
                weekend_processing_time(60)
            if now.weekday() in [6]: # [Dimanche]
                print("Sunday day")
                weekend_processing_time(180)
        except Exception as e:
            try:
                Sending.send_email_pnr_parsing("Aucun PNR non remonté")
            except Exception as e:
                print(f"Error sending pnr not sent to GP : {e}")
                raise e
        
    def pnr_not_sent_to_odoo(now):
        dt_now = now
        day = dt_now.day
        month = dt_now.month
        year = dt_now.year
        time_now = dt_now.time()
        time_before_afternoon = time(12, 0, 0)
        time_after_afternoon = time(15, 0, 0)
        
        dt_to_start_sending_to_odoo = datetime(
                                        day=day, 
                                        month=month, 
                                        year=year, 
                                        hour=8, 
                                        minute=0, 
                                        second=0,
                                        tzinfo=timezone.utc
                                    )     
        dt_sending_before_afternoon = datetime(
                                        day=day, 
                                        month=month, 
                                        year=year, 
                                        hour=12, 
                                        minute=0, 
                                        second=0,
                                        tzinfo=timezone.utc
                                    )
        dt_sending_after_afternoon = datetime(
                                        day=day, 
                                        month=month, 
                                        year=year, 
                                        hour=15, 
                                        minute=0, 
                                        second=0,
                                        tzinfo=timezone.utc
                                    )

        # Liste des pnrs non envoyées entre 08h à 12h
        pnr_not_sent_to_odoo_before_afternoon = Pnr.objects.filter(
                                                    Q(system_creation_date__gte=dt_to_start_sending_to_odoo) & 
                                                    Q(system_creation_date__lte=dt_sending_before_afternoon)
                                                ).filter(is_invoiced=False, state=0, status="Emis").all()
        
        # Liste des pnrs non envoyées entre 08h à 15h
        pnr_not_sent_to_odoo_after_afternoon = Pnr.objects.filter(
                                                    Q(system_creation_date__gte=dt_to_start_sending_to_odoo) & 
                                                    Q(system_creation_date__lte=dt_sending_after_afternoon)
                                                ).filter(is_invoiced=False, state=0, status="Emis").all()
        
        from AmadeusDecoder.models.utilities.Comments import Comment
        
        # Liste des PNRs ayant des anomalies
        anomaly_pnr_ids = []

        # Liste des PNRs sans anomalie
        no_anomaly_pnr_ids_before_afternoon = []
        no_anomaly_pnr_ids_after_afternoon = []

        # Parcourir chaque PNR qui n'a pas été envoyé à Odoo avant midi
        for pnr in pnr_not_sent_to_odoo_before_afternoon:
            comments = Comment.objects.filter(pnr_id_id=pnr.id)
            
            # Vérifier si un commentaire a l'état False
            if any(comment.state is False for comment in comments):
                anomaly_pnr_ids.append(pnr.number)
            else:
                no_anomaly_pnr_ids_before_afternoon.append(pnr.id)
                
        # Parcourir chaque PNR qui a été envoyé à Odoo après midi
        for pnr in pnr_not_sent_to_odoo_after_afternoon:
            comments = Comment.objects.filter(pnr_id_id=pnr.id)
            
            # Vérifier si un commentaire a l'état False
            if any(comment.state is False for comment in comments):
                anomaly_pnr_ids.append(pnr.number)
            else:
                no_anomaly_pnr_ids_after_afternoon.append(pnr.id)

        # Imprimer les PNRs ayant des anomalies
        """if len(anomaly_pnr_ids) > 0:
            print(f"*********** Les PNRs suivants ont des anomalies : {anomaly_pnr_ids} ***********")
            print("\n")
        else:
            print("Aucune anomalie détectée")
            print("\n")"""

        # Récupérer les objets PNRs sans anomalie avant midi
        no_anomaly_pnrs_before_afternoon = []
        for pnr_id in no_anomaly_pnr_ids_before_afternoon:
            no_anomaly_pnrs_before_afternoon.append(Pnr.objects.get(id=pnr_id))
            
        # Récupérer les objets PNRs sans anomalie après midi
        no_anomaly_pnrs_after_afternoon = []
        for pnr_id in no_anomaly_pnr_ids_after_afternoon:
            no_anomaly_pnrs_after_afternoon.append(Pnr.objects.get(id=pnr_id))
            
            
        administrator_username = ['Anissa', 'Asma', 'Lamia', 'Moïse ISSOUFALI']
        
        no_anomaly_pnrs_before_afternoon_for_administrator = []
        no_anomaly_pnrs_after_afternoon_for_administrator = []
        
        no_anomaly_pnrs_before_afternoon_after_processing = []
        no_anomaly_pnrs_after_afternoon_after_processing = []
        
        for pnr in no_anomaly_pnrs_before_afternoon:
            if not str(pnr.get_emit_agent()) in administrator_username:
                no_anomaly_pnrs_before_afternoon_after_processing.append(pnr)
            else:
                no_anomaly_pnrs_before_afternoon_for_administrator.append(pnr)
        
        for pnr in no_anomaly_pnrs_after_afternoon:
            if not str(pnr.get_emit_agent()) in administrator_username:
                no_anomaly_pnrs_after_afternoon_after_processing.append(pnr)
            else:
                no_anomaly_pnrs_after_afternoon_for_administrator.append(pnr)
        
        
        ISSOUFALI_URL = 'https://pnr.issoufali.phidia.fr'
        
        # Parcourir les pnrs non envoyés avant-midi dans Odoo pour les administrateurs
        def pnr_line_data_for_pnr_not_sent_to_odoo_before_afternoon_for_administrator():
            new_line = "\n"
            return(
                f"""
                    {
                        new_line.join(
                            f'''
                                <tr>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        <a href='{ISSOUFALI_URL}/home/pnr/{pnr.id}' title="Ouvrir le pnr {pnr.id}" target="_blank">
                                        {pnr.number}
                                        </a>
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.system_creation_date}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.get_max_issuing_date() if pnr.get_max_issuing_date() is not None else ""}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.get_emit_agent() if pnr.get_emit_agent() is not None else pnr.agent if pnr.agent is not None else ""}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.status}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.type}
                                    </td>
                                </tr>
                            ''' for pnr in no_anomaly_pnrs_before_afternoon_for_administrator
                        )
                    }
                """
            )
            
        # Parcourir les pnrs non envoyés après-midi dans Odoo pour les administrateurs
        def pnr_line_data_for_pnr_not_sent_to_odoo_after_afternoon_for_administrator():
            new_line = "\n"
            return(
                f"""
                    {
                        new_line.join(
                            f'''
                                <tr>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        <a href='{ISSOUFALI_URL}/home/pnr/{pnr.id}' title="Ouvrir le pnr {pnr.id}" target="_blank">
                                        {pnr.number}
                                        </a>
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.system_creation_date}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.get_max_issuing_date() if pnr.get_max_issuing_date() is not None else ""}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.get_emit_agent() if pnr.get_emit_agent() is not None else pnr.agent if pnr.agent is not None else ""}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.status}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.type}
                                    </td>
                                </tr>
                            ''' for pnr in no_anomaly_pnrs_after_afternoon_for_administrator
                        )
                    }
                """
            )
        
        def pnr_line_data_for_pnr_not_sent_to_odoo_before_afternoon():
            new_line = "\n"
            return(
                f"""
                    {
                        new_line.join(
                            f'''
                                <tr>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        <a href='{ISSOUFALI_URL}/home/pnr/{pnr.id}' title="Ouvrir le pnr {pnr.id}" target="_blank">
                                        {pnr.number}
                                        </a>
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.system_creation_date}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.get_max_issuing_date() if pnr.get_max_issuing_date() is not None else ""}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.get_emit_agent() if pnr.get_emit_agent() is not None else pnr.agent if pnr.agent is not None else ""}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.status}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.type}
                                    </td>
                                </tr>
                            ''' for pnr in no_anomaly_pnrs_before_afternoon_after_processing
                        )
                    }
                """
            )
            
        def pnr_line_data_for_pnr_not_sent_to_odoo_after_afternoon():
            new_line = "\n"
            return(
                f"""
                    {
                        new_line.join(
                            f'''
                                <tr>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        <a href='{ISSOUFALI_URL}/home/pnr/{pnr.id}' title="Ouvrir le pnr {pnr.id}" target="_blank" style="text-decoration">
                                            {pnr.number}
                                        </a>
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.system_creation_date}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.get_max_issuing_date() if pnr.get_max_issuing_date() is not None else ""}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.get_emit_agent() if pnr.get_emit_agent() is not None else pnr.agent if pnr.agent is not None else ""}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.status}
                                    </td>
                                    <td style="border:1px solid #ddd;padding:8px;">
                                        {pnr.type}
                                    </td>
                                </tr>
                            ''' for pnr in no_anomaly_pnrs_after_afternoon_after_processing
                        )
                    }
                """
            )
                    
        administrator_users_mail = [
            "lamia@agences-issoufali.com",
            "asmakalfane@agences-issoufali.com",
            "missoufali@agences-issoufali.com",
            "issoufali.a@gmail.com",
        ]
        
        mgbi_users_mail = [
            "phpr974@gmail.com",
            "pp@phidia.onmicrosoft.com",
            "nasolo@phidia.onmicrosoft.com",
            "tahina@phidia.onmicrosoft.com",
            "famenontsoa@outlook.com",
            "alain@phidia.onmicrosoft.com",
        ]
        
        other_users_mail = [
            "stephanie@agences-issoufali.com",
            "fahar@agences-issoufali.com",
            "samir@agences-issoufali.com",
            "oulfate@agences-issoufali.com",
            "mraati@agences-issoufali.com",
            "fouadi@agences-issoufali.com",
            "roihamina@agences-issoufali.com",
            "mouniati@agences-issoufali.com",
            "sylvia@agences-issoufali.com",
            "anziza@agences-issoufali.com",
            "sejours@agences-issoufali.com",
            "sarmada@agences-issoufali.com",
            "lola@agences-issoufali.com",
            "farida@agences-issoufali.com",
            "goula@agences-issoufali.com",
            "saouda@agences-issoufali.com",
            "riziki@agences-issoufali.com",
            "karim@agences-issoufali.com",
            "josianenovou@agences-issoufali.com",
            "anaissa@agences-issoufali.com",
            "hassanati@agences-issoufali.com",
            "saidmaoulida@agences-issoufali.com",
            "madjid@agences-issoufali.com",
            "sity@agences-issoufali.com",
            "koro@agences-issoufali.com",
            "issoufali.pnr@outlook.com",
            "danielbehava2@agences-issoufali.com",
            "david.domitin@agences-issoufali.com",
            "eric@agences-issoufali.com",
            "taanli@agences-issoufali.com",
            "shoulaya@agences-issoufali.com",
        ]
        
        if time_now == time_before_afternoon: # 12h00
            print("==================== PNR not sent to Odoo checking between 08h - 12h ====================")
            
            print("|========= Les pnrs avant 12 heures sans anomalies non envoyées dans Odoo =========|")
            print(f"Les PNRs pour les agents de comptoir: {no_anomaly_pnrs_before_afternoon_after_processing}")
            print(f"Les PNRs pour les administrateurs: {no_anomaly_pnrs_before_afternoon_for_administrator}")
            print("\n")
            
            if len(no_anomaly_pnrs_before_afternoon_after_processing) > 0:
                subject = f"PNR non envoyé dans Odoo entre 08h et 12h, ce {dt_now.strftime('%d-%m-%Y')}"                    
                message = f"""        
                    <!DOCTYPE html>
                    <html>
                    <body>
                        <p> Bonjour, </p>
                        <p> Vous trouverez ci-après la liste des pnrs sans anomalies qui ne sont pas envoyés dans Odoo le {dt_now.strftime('%d-%m-%Y')} entre 08h00 et 12h00. </p>
                        <p> Bonne récéption. </p>
                        <p> Cordialement. </p>
                        <table id="customers" style="border-collapse: collapse;width: 100%;">
                            <thead>
                                <tr>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Numéro PNR</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Date de création</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Date d'émission</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Suivi par</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Status</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Type</th>
                                </tr>
                            </thead>
                            <tbody>
                                {pnr_line_data_for_pnr_not_sent_to_odoo_before_afternoon()}
                            </tbody>
                        </table>
                    </body>
                    </html>
                """
                
                # Envoyer le mail pour toutes les utilisateurs d'Isssoufali 
                Sending.send_email(
                    "issoufali.pnr@outlook.com", 
                    administrator_users_mail + other_users_mail + mgbi_users_mail,  
                    subject, 
                    message
                )
            
            if len(no_anomaly_pnrs_before_afternoon_for_administrator) > 0:
                subject = f"PNR non envoyé dans Odoo pour les directions entre 08h et 12h, ce {dt_now.strftime('%d-%m-%Y')}"                    
                message = f"""        
                    <!DOCTYPE html>
                    <html>
                    <body>
                        <p> Bonjour, </p>
                        <p> Vous trouverez ci-après la liste des pnrs sans anomalies qui ne sont pas envoyés dans Odoo le {dt_now.strftime('%d-%m-%Y')} entre 08h00 et 12h00. </p>
                        <p> Bonne récéption. </p>
                        <p> Cordialement. </p>
                        <table id="customers" style="border-collapse: collapse;width: 100%;">
                            <thead>
                                <tr>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Numéro PNR</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Date de création</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Date d'émission</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Suivi par</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Status</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Type</th>
                                </tr>
                            </thead>
                            <tbody>
                                {pnr_line_data_for_pnr_not_sent_to_odoo_before_afternoon_for_administrator()}
                            </tbody>
                        </table>
                    </body>
                    </html>
                """
                
                # Envoyer le mail pour les administrateurs d'Isssoufali 
                Sending.send_email(
                    "alain@phidia.onmicrosoft.com", 
                    # administrator_users_mail + mgbi_users_mail,  
                    subject, 
                    message
                )
                                
            if len(no_anomaly_pnrs_before_afternoon_for_administrator) < 1 and len(no_anomaly_pnrs_before_afternoon_after_processing) < 1:
                print("Aucun PNR non envoyé dans cette intervalle [08:00 - 12:00]")
                
        if time_now == time_after_afternoon: # 15h00
            print("==================== PNR not sent to Odoo checking between 08h - 15h ====================")
            
            print("|========== Les pnrs après 12 heures sans anomalies non envoyées dans Odoo ========|")
            print(f"Les PNRs pour les agents de comptoir: {no_anomaly_pnrs_after_afternoon_after_processing}")
            print(f"Les PNRs pour les administrateurs: {no_anomaly_pnrs_after_afternoon_for_administrator}")
            print("\n")
            
            if len(no_anomaly_pnrs_after_afternoon_after_processing) > 0:
                subject = f"PNR non envoyé dans Odoo entre 08h et 15h, ce {dt_now.strftime('%d-%m-%Y')}"                
                message = f"""        
                    <!DOCTYPE html>
                    <html>
                    <body>
                        <p> Bonjour, </p>
                        <p> Vous trouverez ci-après la liste des pnrs sans anomalies et qui ne sont pas envoyés dans Odoo le  {dt_now.strftime('%d-%m-%Y')} entre 08h00 et 15h00. </p>
                        <p> Bonne récéption. </p>
                        <p> Cordialement. </p>
                        <table id="customers" style="border-collapse: collapse;width: 100%;">
                            <thead>
                                <tr>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Numéro PNR</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Date de création</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Date d'émission</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Suivi par</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Status</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Type</th>
                                </tr>
                            </thead>
                            <tbody>
                                {pnr_line_data_for_pnr_not_sent_to_odoo_after_afternoon()}
                            </tbody>
                        </table>
                    </body>
                    </html>
                """           
                    
                # Envoyer le mail pour toutes les utilisateurs d'Isssoufali 
                Sending.send_email(
                    "issoufali.pnr@outlook.com", 
                    administrator_users_mail + other_users_mail + mgbi_users_mail,
                    subject, 
                    message
                )
                
            if len(no_anomaly_pnrs_after_afternoon_for_administrator) > 0:
                subject = f"PNR non envoyé dans Odoo pour les directions entre 08h et 15h, ce {dt_now.strftime('%d-%m-%Y')}"                
                message = f"""        
                    <!DOCTYPE html>
                    <html>
                    <body>
                        <p> Bonjour, </p>
                        <p> Vous trouverez ci-après la liste des pnrs sans anomalies qui ne sont pas envoyés dans Odoo le  {dt_now.strftime('%d-%m-%Y')} entre 08h00 et 15h00. </p>
                        <p> Bonne récéption. </p>
                        <p> Cordialement. </p>
                        <table id="customers" style="border-collapse: collapse;width: 100%;">
                            <thead>
                                <tr>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Numéro PNR</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Date de création</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Date d'émission</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Suivi par</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Status</th>
                                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Type</th>
                                </tr>
                            </thead>
                            <tbody>
                                {pnr_line_data_for_pnr_not_sent_to_odoo_after_afternoon_for_administrator()}
                            </tbody>
                        </table>
                    </body>
                    </html>
                """        
                    
                # Envoyer le mail pour les administrateurs d'Isssoufali 
                Sending.send_email(
                    "alain@phidia.onmicrosoft.com", 
                    # administrator_users_mail + mgbi_users_mail,  
                    subject, 
                    message
                )

            if len(no_anomaly_pnrs_after_afternoon_for_administrator) < 1 and len(no_anomaly_pnrs_after_afternoon_after_processing) < 1:
                print("Aucun PNR non envoyé dans cette intervalle [08:00 - 15:00]")
