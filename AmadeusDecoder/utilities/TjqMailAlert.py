'''

'''
import os
import pytz

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.pnr.Passenger import Passenger
from AmadeusDecoder.utilities.SendMail import Sending
from AmadeusDecoder.models.pnrelements.Tjq import Tjq
from django.db.models import Q
from datetime import datetime
from AmadeusDecoder.models.user.Users import User,Office
from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
from AmadeusDecoder.models.invoice.Ticket import Ticket


def alert_tjq() :
    print("Tjq mail alert running...")
    utc=pytz.UTC
    ndate = datetime.now()
    today = datetime(ndate.year, ndate.month, ndate.day, 0, 0, 0)
    ndate = ndate.strftime('%Y-%m-%d')
    now_timezone = ndate+" 00:00:00.000000+03:00"
    now_date = ndate+" 00:00"
    # now_timezone = "2023-01-05 01:00:00.000000+03:00"

    
    
    tjqs = Tjq.objects.all().filter(system_creation_date__gt=now_timezone)
    
    tickets = Ticket.objects.all()
    ticket_numbers = []
    # print(utc.localize(today))

    for t in tickets :
        pnr_obj = Pnr.objects.all().filter(system_creation_date__gt=now_timezone).filter(pk=int(t.pnr.id))
        if pnr_obj.exists() :
            # print("IN ", t.number, t.pnr.system_creation_date)
            ticket_numbers.append(t.number)

            
    is_invoiced = ""
    tjq_pnr_numbers = [t.pnr_number for t in tjqs]
    # print(pnrs_numbers)
    subject = "Rapport TJQ Altea"

    message_head = """
                
                    <tr>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;text-align:left;">PNR</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Ticket</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Total Tjq</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Total Gestion PNR</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Taxe</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Passager</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Vendeur</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Type</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Agence</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Envoyé dans Gestion PNR</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Transféré en commande</th>
                    </tr>
    """


    # PNR non envoyé dans Gestion PNR
    total_pnr_not_sent = 0
    total_pnr_sent = 0
    all_pnrs = []
    message_body = ""
    total_gestion_pnr = 0
    total_total_tjq = 0
    total_taxe = 0
    total_is_invoiced = 0
    for tjq in tjqs :
        if tjq.pnr_number not in all_pnrs :
            all_pnrs.append(tjq.pnr_number)

        if tjq.ticket_number in ticket_numbers :
            is_invoiced = ""
            customer_name = ""
            passenger = ""
            total_pnr_sent += 1
            pnr = Pnr.objects.filter(number=tjq.pnr_number).first()
            ticket = Ticket.objects.filter(number=tjq.ticket_number).first()

            if ticket is None :
                print(tjq.ticket_number)
            ticket_invoice = PassengerInvoice.objects.filter(ticket=ticket.id, is_invoiced=True)
            if ticket.passenger_id is not None :
                passenger = Passenger.objects.filter(pk=int(ticket.passenger_id)).first()

            user = User.objects.get(pk=int(tjq.agent_id)).username if tjq.agent_id is not None else ''
            office = Office.objects.filter(pk=pnr.agency.id).first() if pnr.agency is not None else pnr.agency_name

            if ticket_invoice.exists():
                total_is_invoiced += 1
                is_invoiced = "x"
                customer_name = ticket_invoice.first().client.intitule

            total_gestion_pnr += float(ticket.total)
            total_total_tjq += float(tjq.total)
            total_taxe += float(ticket.tax)

            message_body += """
                    <tr>
                        <td style="border: 1px solid #dddddd;padding: 8px;"><strong>{pnr}</strong></td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{ticket}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{total_tjq}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{total_gestion_pnr}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{taxe}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{passenger}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{agent}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{type}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{agence}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{gp_sent}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{is_invoiced}</td>
                    </tr>
                """.format(pnr=tjq.pnr_number, ticket=tjq.ticket_number,total_tjq=tjq.total, total_gestion_pnr=round(ticket.total, 2), taxe=round(ticket.tax, 2), passenger=passenger, agent=user, type=ticket.ticket_type, agence=office,gp_sent="x",is_invoiced=is_invoiced )

        else :
            total_pnr_not_sent += 1
            user = User.objects.get(pk=int(tjq.agent_id)).username if tjq.agent_id is not None else ''
            total_total_tjq += float(tjq.total)
            total_taxe += float(tjq.tax)
            message_body += """
                    <tr>
                        <td style="border: 1px solid #dddddd;padding: 8px;"><strong>{pnr}</strong></td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{ticket}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{total_tjq}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{total_gestion_pnr}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{taxe}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{passenger}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{agent}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{type}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{agence}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{gp_sent}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{is_invoiced}</td>
                    </tr>
                """.format(pnr=tjq.pnr_number, ticket=tjq.ticket_number, total_tjq=tjq.total, total_gestion_pnr="", taxe=tjq.tax, passenger=tjq.passenger, agent=user, type=tjq.type, agence=tjq.agency_name,gp_sent="",is_invoiced="" )


            # print(tjq)
    # message_body += """<tr>
    #     <td colspan="7" style="border: 1px solid #dddddd;padding: 8px;"><strong>Total</strong></td>
    #     <td style="border: 1px solid #dddddd;padding: 8px;"><strong>{total}</strong></td>
    # </tr>""".format(total=total_pnr_not_sent)

    message_total = """
                    <tr>
                        <td style="border: 1px solid #dddddd;padding: 8px;"><strong>{total_pnr}</strong></td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{total_ticket}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{total_total_tjq}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{total_total_gestion_pnr}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{total_taxe}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{total_passenger}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{total_agent}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{total_type}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{total_agence}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{total_gp_sent}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{total_is_invoiced}</td>
                    </tr>
    """.format(total_pnr=len(all_pnrs), total_ticket=round(total_pnr_not_sent+total_pnr_sent,2),total_total_tjq=round(total_total_tjq, 2), total_total_gestion_pnr=round(total_gestion_pnr, 2), total_taxe=round(total_taxe,2), total_passenger="", total_agent="", total_type="", total_agence="",total_gp_sent="%s/%s" % (total_pnr_sent,total_pnr_not_sent+total_pnr_sent),total_is_invoiced="%s/%s" % (total_is_invoiced,total_pnr_not_sent+total_pnr_sent ))


   

    body = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Rapport TJQ</title>
                
                </head>
                <body>
                    <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                        Bonjour,<br /><br />
                        <strong>PNR/Ticket créés du {ndate} :</strong> 
                    </p> </br>
                    <p>
                        <table style= "border-collapse: collapse;width: 80%; margin-left:auto; margin-right:auto;">
                        {message_total}
                        {message_head}
                        {message_body}
                        </table>
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
            """.format(ndate=ndate,message_total=message_total,message_head= message_head,message_body=message_body)
    											
    recipients = [
        "pissoufali@agences-issoufali.com",
        "missoufali@agences-issoufali.com",
        "lamia@agences-issoufali.com",
        "stephanie@agences-issoufali.com",
        "asmakalfane@agences-issoufali.com",
        "david.domitin@agences-issoufali.com",
        "pp@phidia.onmicrosoft.com",
        "mihaja@phidia.onmicrosoft.com",
        "tahina@phidia.onmicrosoft.com"
    ]	
    							

    Sending.send_email(
        "tjq.issoufali.pnr@outlook.com",
        recipients,
        subject,
        body
    )
        

    