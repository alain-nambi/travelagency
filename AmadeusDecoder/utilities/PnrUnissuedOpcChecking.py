'''

'''
import os

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.TicketPassengerSegment import TicketPassengerSegment
from AmadeusDecoder.models.invoice.TicketSSR import TicketSSR
from AmadeusDecoder.models.pnrelements.ConfirmationDeadline import ConfirmationDeadline
from AmadeusDecoder.utilities.SendMail import Sending


def get_opc_as_datetime():
    opcs = ConfirmationDeadline.objects.all().filter(type='OPC').order_by('-doc_date')

    return opcs

def notify_user(opc) :
    pnr = opc.segment.pnr if opc.segment else opc.ssr.pnr
    passengers = pnr.passengers.all().order_by('id')
    passengers_name = ", ".join( [ '%s %s' % (passenger.passenger.name, passenger.passenger.surname) for passenger in passengers ] )
    doc_type = 'vol' if opc.segment else 'SSR'
    doc_value = '%s %s %s - %s (%s)' % ( opc.segment.servicecarrier.iata, opc.segment.flightno,  opc.segment.codeorg.iata_code,  opc.segment.codedest.iata_code, opc.segment.segmentorder) if opc.segment else ''
    doc_value = opc.ssr.ssr.code if opc.ssr else doc_value
    username = pnr.agent.username if pnr.agent else pnr.agent_code
    date_limite = opc.doc_date.strftime('%Y-%m-%d %H:%M')
    contacts = pnr.contacts.all()
    contact_value = ''
    for contact in contacts :
        contact_value += """</span>{}</span></br>""".format(contact.value)
    
    											
											

    # Send mail
    subject = "Notification OPC: " + pnr.number

    message = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Notification OPC</title>
                
                </head>
                <body>
                    <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                        Bonjour,<br /><br />
                        La réservation de(s) passager(s)  {passengers} pour le {doc_type} {doc_value} rattaché au PNR {pnr} arrive à expiration dans 24h. 
                    </p>
                    <p>
                        <strong>PNR : </strong> {pnr} </br>
                        <strong>Passager(s) : </strong> {passengers} </br>
                        <strong>{doc_type} : </strong> {doc_value} </br>
                        <strong>Date limite : </strong> {date_limite} </br>
                        <strong>Agent : </strong> {username} </br>
                        <strong>Contact : </strong>
<pre>{contact_value}</pre>
                    </p>
                    
                </body>
                </html>
            """.format(passengers=passengers_name,doc_type=doc_type,doc_value=doc_value, pnr=pnr.number, date_limite=date_limite,username=username,contact_value=contact_value)

    user_mail = pnr.agent.email if pnr.agent else ''
    Sending.send_email(
        "issoufali.pnr@outlook.com",
        [
            user_mail,
            "tahina@phidia.onmicrosoft.com",
            "pp@phidia.onmicrosoft.com",
            "maphiesarobidy@outlook.fr",
        ],
        subject,
        message
    )
        

    