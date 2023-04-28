'''
Created on 16 Dec 2022

@author: Famenontsoa
'''
import traceback
import secrets
from datetime import datetime
from AmadeusDecoder.utilities.SendMail import Sending
from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.Fee import Fee
from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.models.invoice.Fee import ReducePnrFeeRequest

class ServiceFeesDecreaseRequest():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    # inquiry data
    def inquiry_data(self, request, feeId, pnrId, feeOriginAmount, feeAmount, motif):
        # data
        fee_object = Fee.objects.get(pk=int(feeId))
        pnr_object = Pnr.objects.get(pk=int(pnrId))
        ticket_total_cost = 0
        pnr_total_cost = 0
        customers = ''
        first_passenger = None
        try:
            ticket_obj = fee_object.ticket
            ticket_total_cost = ticket_obj.total if ticket_obj is not None else 0
            first_passenger = pnr_object.passengers.first().passenger
            pnr_customer = pnr_object.passenger_invoice.all().distinct()
            for temp_pnr_customer in pnr_customer:
                customers += str(temp_pnr_customer.client) + " -"
            customers.removesuffix('-')
            pnr_total_cost = fee_object.pnr.invoice.detail.total
        except:
            traceback.print_exc()
            pass
        
        user = User.objects.get(pk=int(request.user.id))
        token = secrets.token_hex(32)


        request_reduce_pnr_fee = ReducePnrFeeRequest(
            pnr=pnr_object, 
            fee=fee_object, 
            user=user, 
            origin_amount=float(feeOriginAmount),
            amount=float(feeAmount),
            status=0,
            system_creation_date=datetime.now(),
            token=token,
            motif=motif
            )
        request_reduce_pnr_fee.save()
        
        return request_reduce_pnr_fee, ticket_obj, ticket_total_cost, first_passenger, customers.removesuffix(';'), pnr_total_cost
    
    # request response url
    def request_response_url(self, response_type, choiceType, token, pnr_object, customers, first_passenger, feeOriginAmount, feeAmount, ticket_total_cost, ticket_total_all):
        # when modifying requested fees
        mail_recipient = "issoufali.pnr@gmail.com"
        subject = "FEE%20MODIFY%20REQUEST"
        mail_body = ""
        ticket_concerned = ""
        record_locator = "FEE%20MODIFY%20REQUEST;%0D%0A1.RECORD%20LOCATOR%20{pnr_number};%0D%0A".format(pnr_number=pnr_object.number)
        token = "3.UNIQUE%20ONE%20USE%20KEY%20{token};%0D%0A".format(token=token)
        customers = "4.CUSTOMER%20{customers};%0D%0A".format(customers=customers)
        first_passenger_in_list = "5.FIRST%20PASSENGER%20IN%20LIST%20{first_passenger};%0D%0A".format(first_passenger=first_passenger)
        original_fee_cost  = "7.ORIGINAL%20FEE%20{initial_fee}(EUR);%0D%0A".format(initial_fee=feeOriginAmount)
        requested_fee = "8.REQUESTED%20FEE%20{requested_fee}(EUR);%0D%0A".format(requested_fee=feeAmount)
        status_list = {'accepted':'ACCEPTED', 'rejected':'REJECTED', 'modify':'ACCEPTED/MODIFIED'}
        status = "9.STATUS%20{status};%0D%0A".format(status=status_list[response_type])
        to_be_applied_fees = {'accepted':str(feeAmount)+'EUR', 'rejected':'CURRENT%20FARE', 'modify':''}
        to_be_applied_fee = "10.TO%20BE%20APPLIED%3A{to_be_aaplied_fee}".format(to_be_aaplied_fee=to_be_applied_fees[response_type])
        if choiceType == "one":
            ticket_concerned = "2.ONLY%20ONE%20TICKET%20CONCERNED;%0D%0A"
            ticket_total = "6.TOTAL%20{ticket_total}(EUR);%0D%0A".format(ticket_total=round(ticket_total_cost, 2))
        elif choiceType == "all":
            ticket_concerned = "2.ALL%20TICKET%20CONCERNED;%0D%0A"
            ticket_total = "6.TOTAL%20{ticket_total}(EUR);%0D%0A".format(ticket_total=round(ticket_total_all, 2))
        
        mail_body += record_locator + ticket_concerned + token + customers + first_passenger_in_list \
            + ticket_total + original_fee_cost + requested_fee + status + to_be_applied_fee
        
        button_texts = {'accepted':'Accepter', 'rejected':'Refuser', 'modify':'Modifier'}
        border_colors = {'accepted':'#4CAF50', 'rejected':'#f44336', 'modify':'#008CBA'}
        modify_url = """
            <A HREF="mailto:{mail_to_recipient}?subject={subject}&body={mail_body}" target="_top" style="padding: 8px 12px; border: 1px solid {border_color};border-radius: 2px;font-family: Helvetica, Arial, sans-serif;font-size: 14px; color: #ffffff;text-decoration: none;font-weight:bold;display: inline-block;">{button_text}</A>
        """.format(mail_to_recipient=mail_recipient, subject=subject, mail_body=mail_body, button_text=button_texts[response_type], border_color=border_colors[response_type])
        
        return modify_url
        
    # inquiry formatting
    def inquiry_formatting(self, choiceType, request, feeId, pnrId, feeOriginAmount, feeAmount, motif):
        request_reduce_pnr_fee, ticket_obj, ticket_total_cost, first_passenger, customers, pnr_total_cost = self.inquiry_data(request, feeId, pnrId, feeOriginAmount, feeAmount, motif)
        pnr_object = request_reduce_pnr_fee.pnr
        user = request_reduce_pnr_fee.user
        token = request_reduce_pnr_fee.token
        origin_amount = request_reduce_pnr_fee.origin_amount
        motif = request_reduce_pnr_fee.motif
        # subject
        subject = "Demande de diminution de frais de services: " + pnr_object.number
        
        # message formating
        heading_message = ''
        if choiceType == 'one':
            heading_message = "Une demande de diminution de frais de service a été envoyé par {username} pour le PNR : {pnr}".format(username=user.username, pnr=pnr_object.number)
            email_body = """
                <p>
                    <strong>Nom du premier passager : </strong> {first_passenger} </br>
                    <strong>Client(s) : </strong> {pnr_customers} </br>
                </p>
                <p>
                    <strong>Numéro du billet/EMD: </strong> {ticket_number}</br>
                    <strong>Passager: </strong> {ticket_passenger} </br>
                    <strong>Montant du billet: </strong> {ticket_cost} €</br>
                </p>
                <p>
                    <strong>Montant original du fee: </strong> {origin_amount} €</br>
                    <strong>Montant demandé : </strong> {amount} €</br>
                    <strong>Motif : </strong> {motif} </br>
                </p>
            """.format(first_passenger=first_passenger, pnr_customers=customers, ticket_number=str(ticket_obj) if ticket_obj is not None else '', ticket_passenger=str(ticket_obj.passenger) if ticket_obj is not None else '' ,ticket_cost=round(ticket_total_cost, 2), origin_amount=feeOriginAmount, amount=feeAmount, motif=motif)
        elif choiceType == 'all':
            heading_message = "Une demande de diminution de frais de service a été envoyé par {username} pour tous les billets/EMD du PNR : {pnr}".format(username=user.username, pnr=pnr_object.number)
            email_body = """
                <p>
                    <strong>Nom du premier passager : </strong> {first_passenger} </br>
                    <strong>Client(s) : </strong> {pnr_customers} </br>
                    <strong>Montant total du PNR: </strong> {total_cost} €</br>
                </p>
            """.format(first_passenger=first_passenger, pnr_customers=customers, total_cost=round(pnr_total_cost, 2))
            all_related_ticket = Ticket.objects.filter(pnr__id=pnrId, ticket_status=1).all()
            article_no = 1
            for ticket in all_related_ticket:
                ticket_number = ticket.number
                ticket_total = ticket.total
                ticket_passenger = ticket.passenger
                requested_fee = float(feeAmount)
                email_body += """
                    <p>
                        <strong>Article {article_no}: </strong> {ticket_number} </br>
                        <strong>Montant: </strong> {ticket_total} €</br>
                        <strong>Passager: </strong> {ticket_passenger}</br>
                        <strong>Montant initial du fee: </strong> {original_fee} €</br>
                        <strong>Montant demandé: </strong> {requested_fee} €</br>
                        <strong>Motif : </strong> {motif} </br>
                    </p>
                """.format(article_no=str(article_no), ticket_number=ticket_number, ticket_total=round(ticket_total,2), ticket_passenger=str(ticket_passenger), original_fee=round(origin_amount,2), requested_fee=requested_fee,motif=motif)
                article_no += 1
        
        url_accepted =  self.request_response_url('accepted', choiceType, token, pnr_object, customers, first_passenger, feeOriginAmount, feeAmount, ticket_total_cost, pnr_total_cost)
        url_rejected = self.request_response_url('rejected', choiceType, token, pnr_object, customers, first_passenger, feeOriginAmount, feeAmount, ticket_total_cost, pnr_total_cost)
        url_modify = self.request_response_url('modify', choiceType, token, pnr_object, customers, first_passenger, feeOriginAmount, feeAmount, ticket_total_cost, pnr_total_cost)
        
        message = """
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Demande de diminution de frais de service</title>
                    
                    </head>
                    <body>
                        <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                            Bonjour,<br /><br />
                            {heading_message}
                        </p>
                        {email_body}
                        <p> 
                            <table width="100%" cellspacing="0" cellpadding="0">
                                <tr>
                                    <td>
                                        <table cellspacing="0" cellpadding="0">
                                            <tr>
                                                <td style="border-radius: 2px;" bgcolor="#4CAF50">
                                                    {url_accepted}
                                                </td>
                                                <td style="border-radius: 2px;" bgcolor="#f44336">
                                                    {url_rejected}
                                                </td>
                                                <td style="border-radius: 2px;" bgcolor="#008CBA">
                                                    {url_modify}
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                </table>
                            
                        </p>
                    </body>
                    </html>
                """.format(heading_message=heading_message, email_body=email_body, url_accepted=url_accepted, url_rejected=url_rejected, url_modify=url_modify)
               
        return subject, message

    # formatting response
    def response_formatter(self, reduceFeeRequestObj, feeOriginAmount, feeAmount, modifiedAmount, decrease_status, choice_type, user_responder):
        # decrease_status: 0=denied, 1=accepted, 2=modified
        if decrease_status == 0:
            request = 'Refusé'
            accepted_amount = ''
        elif decrease_status == 1:
            request = 'Accepté'
            accepted_amount = "<strong>Montant accepté : </strong> {amount} €</br>".format(amount=round(float(feeAmount), 2))
        elif decrease_status == 2:
            request = 'Accepté, modifié'
            accepted_amount = "<strong>Montant accepté : </strong> {amount} €</br>".format(amount=round(float(modifiedAmount), 2))
        
        # data
        ticket_total_cost = 0
        pnr_total_cost = 0
        customers = ''
        first_passenger = ''
        try:
            pnr = reduceFeeRequestObj.pnr
            first_passenger = pnr.passengers.first().passenger
            pnr_customer = pnr.passenger_invoice.all().distinct()
            fee_obj = reduceFeeRequestObj.fee
            ticket_obj = fee_obj.ticket
            ticket_total_cost = ticket_obj.total if ticket_obj is not None else 0
            for temp_pnr_customer in pnr_customer:
                customers += str(temp_pnr_customer.client) + " - "
            pnr_total_cost = fee_obj.pnr.invoice.detail.total
        except:
            traceback.print_exc()
            pass
        
        subject = "Réponse de la demande de diminution de frais de services: " + pnr.number
        
        pnr_description = ''
        original_fee = reduceFeeRequestObj.origin_amount
        if choice_type == 'one':
            answer_header = "Réponse de votre demande de diminution de frais de service pour le PNR  {pnr}:".format(pnr=pnr.number)
            pnr_description = """
                <p>
                    <strong>Nom du premier passager : </strong> {first_passenger} </br>
                    <strong>Client(s) : </strong> {pnr_customers} </br>
                </p>
                <p>
                    <strong>Numéro du billet/EMD: </strong> {ticket_number}</br>
                    <strong>Passager: </strong> {ticket_passenger} </br>
                    <strong>Montant du billet: </strong> {ticket_cost} €</br>
                </p>
                <p>
                    <strong>Status : </strong> {response}</br>
                    <strong>Montant original du fee: </strong> {origin_amount} €</br>
                    <strong>Montant demandé : </strong> {amount} €</br>
                    {accepted_amount}
                </p>
            """.format(first_passenger=first_passenger, pnr_customers=customers, ticket_number=str(ticket_obj) if ticket_obj is not None else '', ticket_passenger=str(ticket_obj.passenger) if ticket_obj is not None else '', ticket_cost=round(ticket_total_cost, 2), response=request, origin_amount=round(float(feeOriginAmount), 2), amount=round(float(feeAmount), 2), accepted_amount=accepted_amount)
        elif choice_type == 'all':
            answer_header = "Réponse de votre demande de diminution des frais de service pour tous les billets/EMD du PNR  {pnr}:".format(pnr=pnr.number)
            pnr_description = """
                <p>
                    <strong>Nom du premier passager : </strong> {first_passenger} </br>
                    <strong>Client(s) : </strong> {pnr_customers} </br>
                    <strong>Montant total du PNR: </strong> {total_cost} €</br>
                </p>
            """.format(first_passenger=first_passenger, pnr_customers=customers, total_cost=round(pnr_total_cost, 2))
            all_related_ticket = Ticket.objects.filter(pnr__id=pnr.id, ticket_status=1).all()
            article_no = 1
            for ticket in all_related_ticket:
                ticket_number = ticket.number
                ticket_total = ticket.total
                ticket_passenger = ticket.passenger
                requested_fee = float(feeAmount)
                pnr_description += """
                    <p>
                        <strong>Article {article_no}: </strong> {ticket_number} </br>
                        <strong>Montant: </strong> {ticket_total} €</br>
                        <strong>Passager: </strong> {ticket_passenger}</br>
                        <strong>Montant initial du fee: </strong> {original_fee} €</br>
                        <strong>Montant demandé: </strong> {requested_fee} €</br>
                        <strong>Status : </strong> {response}</br>
                        {accepted_amount}
                    </p>
                """.format(article_no=str(article_no), ticket_number=ticket_number, ticket_total=round(ticket_total,2), ticket_passenger=str(ticket_passenger), original_fee=round(original_fee, 2), requested_fee=requested_fee, response=request, accepted_amount=accepted_amount)
                article_no += 1
            
        message = """
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Réponse de votre demande de dimunition de frais de service</title>
                    
                    </head>
                    <body>
                        <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                            Bonjour,<br /><br />
                            {answer_header}
                        </p>
                        {pnr_description}
                        <p>    
                            <strong>Demande traitée par:</strong> {request_handler}
                        </p>
                        <p>
                            Bien cordialement.
                        </p>
                    </body>
                    </html>
                    """.format(answer_header=answer_header, pnr_description=pnr_description, request_handler=user_responder)
        
        return subject, message
    
    # send response email
    def send_decrease_request_response(self, reduceFeeRequestObj, modified_amount, decrease_status, choice_type, user_responder):
        # decrease_status: 0=denied, 1=accepted, 2=modified
        try:
            feeOriginAmount = reduceFeeRequestObj.origin_amount
            feeAmount = reduceFeeRequestObj.amount
            
            subject, message = self.response_formatter(reduceFeeRequestObj, feeOriginAmount, feeAmount, modified_amount, decrease_status, choice_type, user_responder)
            
            recipient = reduceFeeRequestObj.user.email
            Sending.send_email_request(
                "feerequest.issoufali.pnr@outlook.com",
                [
                    # recipient,
                    # "superviseur@agences-issoufali.com",
                    # "pp@phidia.onmicrosoft.com",
                    "mihaja@phidia.onmicrosoft.com",
                    "tahina@phidia.onmicrosoft.com",
                    "famenontsoa@outlook.com"
                ],
                subject,
                message
            )
        except:
            traceback.print_exc()
        
        