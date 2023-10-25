'''
Created on 11 Jan 2023

@author: Mihaja
'''

import psycopg2
from datetime import datetime
import os
import requests
import json

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.InvoicePassenger import PassengerInvoice
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.user.Users import User,Office
from AmadeusDecoder.utilities.SendMail import Sending
from django.db.models import Q


def control_data_gp_odoo() :
    date_now = datetime.now()
    maximum_timezone = "2022-10-25 01:00:00.000000+03:00"

    tickets_invoiced = PassengerInvoice.objects.all().filter(Q(date_creation__gt=maximum_timezone)).filter(is_invoiced=True).filter(control=0)
    rows_not_found = []

    # Table head
    message_head_pnr_not_found = """
                
                    <tr>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;text-align:left;">ID</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">PNR</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Client</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Type</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Transport</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Taxe</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Sous total</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Total Gestion PNR</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Date</th>
                         <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Erreur</th>
                    </tr>
    """

    message_head = """
                
                    <tr>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;text-align:left;">ID</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">PNR</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Client</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Type</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Transport</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Taxe</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Sous total</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Total Gestion PNR</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Total Odoo</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Date</th>
                        <th style="border: 1px solid #dddddd;padding: 8px;background-color: #dddddd;">Erreur</th>
                    </tr>
    """

    message_body = ""
    for ticket_invoice in tickets_invoiced :
        print("Processing row ID %s" % ticket_invoice.id)
        # Get ticket row in odoo
        odoo_rows = get_ticket_from_odoo(ticket_invoice)

        # Total rows gp
        gptotal = get_rows_total(ticket_invoice)
        agent = ticket_invoice.pnr.agent

        transport = ticket_invoice.ticket.transport_cost if ticket_invoice.ticket is not None else ticket_invoice.fee.cost if ticket_invoice.fee is not None else ticket_invoice.other_fee.cost
        taxe = ticket_invoice.ticket.tax if ticket_invoice.ticket is not None else ticket_invoice.fee.tax if ticket_invoice.fee is not None else ticket_invoice.other_fee.tax
        sousTotal = ticket_invoice.ticket.total if ticket_invoice.ticket is not None else ticket_invoice.fee.total if ticket_invoice.fee is not None else ticket_invoice.other_fee.total
        if not odoo_rows :
            rows_not_found.append(ticket_invoice)
            print("ERREUR: Ligne {} {} non présent dans Odoo détécté.".format(ticket_invoice.type, ticket_invoice.id))
        
        else :
            error_state,results = process_row_comparaison(ticket_invoice, odoo_rows, gptotal)

            if error_state :
                message_body += """
                    <tr>
                        <td style="border: 1px solid #dddddd;padding: 8px;"><strong>{id}</strong></td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{pnr}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{client}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{type}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{transport}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{taxe}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{sousTotal}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{total}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{total_odoo}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{date}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{error}</td>
                    </tr>
                """.format(id=ticket_invoice.id,pnr=ticket_invoice.pnr, client=ticket_invoice.client, type= ticket_invoice.type, transport=transport, taxe=taxe, sousTotal=sousTotal, total=gptotal, total_odoo=odoo_rows['order']['amount_total'], date=ticket_invoice.date_creation, error=", ".join(results))

    message_for_not_found = ""
    for _row in rows_not_found :
        # Total rows gp
        gptotal = get_rows_total(_row)
        agent = _row.pnr.agent
        transport = _row.ticket.transport_cost if _row.ticket is not None else _row.fee.cost if _row.fee is not None else _row.other_fee.cost
        taxe = _row.ticket.tax if _row.ticket is not None else _row.fee.tax if _row.fee is not None else _row.other_fee.tax
        sousTotal = _row.ticket.total if _row.ticket is not None else _row.fee.total if _row.fee is not None else _row.other_fee.total

        message_for_not_found += """
                    <tr>
                        <td style="border: 1px solid #dddddd;padding: 8px;"><strong>{id}</strong></td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{pnr}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{client}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{type}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{transport}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;" align="right">{taxe}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{sousTotal}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{total}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{date}</td>
                        <td style="border: 1px solid #dddddd;padding: 8px;text-align:center;">{error}</td>
                    </tr>
                """.format(id=_row.id,pnr=_row.pnr, client=_row.client, type= _row.type, transport=transport, taxe=taxe, sousTotal=sousTotal, total=gptotal,date=_row.date_creation, error=", ".join(results))

                
    body = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Rapport TJQ</title>
                
                </head>
                <body>
                    <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                        Bonjour,<br /><br />
                        <strong>PNR/Ticket créés qui ne sont pas envoyés dans Gestion PNR :</strong> 
                    </p> </br>
                    <p>
                        <h3>PNR créé commande dans gestion PNR non présent dans Odoo</h3>
                        <table style= "border-collapse: collapse;width: 80%; margin-left:auto; margin-right:auto;">
                        {message_head_pnr_not_found}
                        {message_for_not_found}
                        </table>
                    </p>
                    <p>
                        <h3>PNR créé commande avec montant Gestion PNR - Odoo différent </h3>
                        <table style= "border-collapse: collapse;width: 80%; margin-left:auto; margin-right:auto;">
                        {message_head}
                        {message_body}
                        </table>
                    </p>
                   
                    <p>
                        Bien cordialement,
                    </p>
                    <p>
                        <strong>Ceci est un email automatique, merci de ne pas répondre.</strong></br>
                        Services supports : tahina@phidia.onmicrosoft.com
                    </p> 
                </body>
                </html>
            """.format(message_head_pnr_not_found=message_head_pnr_not_found, message_for_not_found=message_for_not_found, message_head= message_head,message_body=message_body)
    											
    recipients = [
        "nasolo@phidia.onmicrosoft.com",
        "famenontsoa@outlook.com",
        "alain@phidia.onmicrosoft.com",
        "tahina@phidia.onmicrosoft.com"
    ]		
    subject = "Contrôle des données Gestion PNR - Odoo"						

    Sending.send_email(
        "issoufali.pnr@outlook.com",
        recipients,
        subject,
        body
    )
            


        

    # gp_tickets_invoiced = PassengerInvoice.objects.all().filter(control=0)

    # for ticket in gp_tickets_invoiced :

def process_row_comparaison(ticket_invoice, odoo_rows, total) :
    date_now = datetime.now()
    error_msg = []
    state = False 

    try : 

        if int(ticket_invoice.client.id) != int(odoo_rows['order']['client_id']) :
            error = "Erreur client différent détécté."
            print(error)
            error_msg.append(error) 
            state = True
        if ticket_invoice.ticket is not None and float(ticket_invoice.ticket.total) !=  odoo_rows['price_total']:
            error = "Erreur montant transport différent détécté."
            error_msg.append(error) 
            print(error)
            state = True
        if ticket_invoice.other_fee is not None and float(ticket_invoice.other_fee.total) !=  odoo_rows['price_total']:
            error = "Erreur montant transport différent détécté."
            error_msg.append(error) 
            print(error)
            state = True
        if ticket_invoice.fee is not None and float(ticket_invoice.fee.total) !=  odoo_rows['price_total']:
            error = "Erreur montant frais de service différent détécté."
            error_msg.append(error) 
            print(error)
            state = True
        if total != odoo_rows['order']['amount_total'] :
            error = "Erreur montant total différent détécté."
            error_msg.append(error) 
            print(error)
            state = True
        
    except Exception as e :
        error_msg.append(e)
        print(e)
        # subject = "ERREUR Récupération des données Gestion PNR dans Odoo."
        # body = """
        #                 <!DOCTYPE html>
        #                 <html>
        #                 <head>
        #                     <title>Erreur de contrôle des données</title>
        #                 </head>
        #                 <body>
        #                     <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
        #                         Bonjour, <br>
        #                         une érreur s'est produite lors de la contrôle des données.
        #                     </p>
        #                     <p>
        #                         {date} ERREUR: Impossible de vérifier la ligne {doc} {id}.<br>
        #                         {date} ERREUR: {error}. 
        #                     </p>
        #                     <p> Cordialement, </p>
        #                 </body>
        #                 </html>
        #             """.format(date=date_now,error=e, id=ticket_invoice.id, doc=ticket_invoice.type)
        # recipients = [
        # "mihaja@phidia.onmicrosoft.com"
        # ]								

        # Sending.send_email_error(
        #     "error.issoufali.pnr@outlook.com",
        #     recipients,
        #     subject,
        #     body
        # )

    return state,error_msg

    

def get_rows_total(ticket_invoice) :
    rows_invoice = PassengerInvoice.objects.all().filter(client=ticket_invoice.client).filter(pnr=ticket_invoice.pnr)
    total = 0.0

    for row in rows_invoice :
        if row.fee is not None :
            total += float(row.fee.total)
        elif row.ticket is not None :
            total += float(row.ticket.total)

    return total

def get_ticket_from_odoo(ticket) :
    date_now = datetime.now()
    #url = 'http://5.135.136.201:8075/get/orderline/%s' % ticket.id
    # url = 'http://5.135.136.201:8075/get/orderline/1174'
    response = None

    try :
        response = requests.post(url)
        response = response.content.decode('utf-8')
        response = json.loads(response)
    except Exception as e :
        print("ERREUR: Ligne %s du PNR %s, Impossible de se trouver les données dans Odoo.")
        print(e)
        # Send the error with mail 
        subject = "ERREUR Récupération des données Gestion PNR dans Odoo."
        body = """
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Erreur de contrôle des données</title>
                        </head>
                        <body>
                            <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                                Bonjour, <br>
                                une érreur s'est produite lors de la contrôle des données.
                            </p>
                            <p>
                                {date} ERREUR: Impossible de trouver la ligne {doc} {id} dans Odoo.<br>
                                {date} ERREUR: {error}. 
                            </p>
                            <p> Cordialement, </p>
                        </body>
                        </html>
                    """.format(date=date_now,error=e, id=ticket.id, doc=ticket.type)
        recipients = [
        # "mihaja@phidia.onmicrosoft.com"
        ]								

        # Sending.send_email_error(
        #     "error.issoufali.pnr@outlook.com",
        #     recipients,
        #     subject,
        #     body
        # )

    return response
    


def connect_odoo_db(host, port, database, user, pwd) :
    date_now = datetime.now()
    connexion_state = False
    try :
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=pwd)

        return conn
    except Exception as e:
        
        print("Impossible de se connecter à la base de données Odoo.")
        print(e)
        # Send the error with mail 
        subject = "ERREUR ACCES BASE DE DONNEES ODOO."
        body = """
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Erreur de contrôle des données</title>
                        </head>
                        <body>
                            <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                                Bonjour, <br>
                                une érreur s'est produite lors de la contrôle des données.
                            </p>
                            <p>
                                {date} ERREUR: Impossible de se connecter à la base de données Odoo.<br>
                                {date} ERREUR: {error}. 
                            </p>
                            <p> Cordialement, </p>
                        </body>
                        </html>
                    """.format(date=date_now,error=e)
        recipients = [
            "nasolo@phidia.onmicrosoft.com"
        ]								

        Sending.send_email_error(
            "error.issoufali.pnr@outlook.com",
            recipients,
            subject,
            body
        )

    return connexion_state
