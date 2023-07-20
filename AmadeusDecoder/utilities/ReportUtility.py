'''
Created on Jun 20, 2023

@author: Famenontsoa
'''
import os
import django
import datetime

import AmadeusDecoder.utilities.configuration_data as configs

from AmadeusDecoder.utilities.SendMail import Sending

# EMD_IDENTIFIER = ["EMD"]
# AIRPORT_AGENCY_CODE = ["DZAUU000B", "Mayotte ATO"]

EMD_IDENTIFIER = configs.EMD_IDENTIFIER
AIRPORT_AGENCY_CODE = configs.AIRPORT_AGENCY_CODE

FEE_HISTORY_REPORT_LOCAL_RECIPIENTS = configs.FEE_HISTORY_REPORT_LOCAL_RECIPIENTS

FEE_HISTORY_REPORT_CUSTOMER_RECIPIENTS = configs.FEE_HISTORY_REPORT_CUSTOMER_RECIPIENTS


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'DjangoTravelAgency.settings'
)
django.setup()

from AmadeusDecoder.models.history.History import History
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.Fee import OthersFee
from django.db.models import Q

class ReportUtility():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    # fee history report
    def fee_history_report(self, target_date):
        target_history_list = History.objects.filter(modification_type='Fee', modification_date__year=target_date.year,
                                                     modification_date__month=target_date.month, modification_date__day=target_date.day).order_by('-modification_date').all()
        
        final_target_history_list = []
        history_list = []
        
        for target_history in target_history_list:
            related_object_id = target_history.related_object_id
            if related_object_id is not None:
                temp_ticket_airport = Ticket.objects.filter(Q(issuing_agency__code__in=AIRPORT_AGENCY_CODE) | Q(issuing_agency_name__in=AIRPORT_AGENCY_CODE), id=related_object_id, ticket_type__in=EMD_IDENTIFIER).first()
                temp_other_fee_airport = OthersFee.objects.filter(id=related_object_id, fee_type__in=EMD_IDENTIFIER, issuing_agency_name__in=AIRPORT_AGENCY_CODE).first()
                
                if temp_ticket_airport is not None or temp_other_fee_airport is not None:
                    final_target_history_list.append(target_history)
                
        for history in final_target_history_list:
            temp_modification = {}
            temp_modification['modified_object'] = history.modification_type
            temp_modification['modified_pnr'] = history.pnr_number
            temp_modification['username'] = history.username
            temp_modification['modification_date'] = history.modification_date
            modif_type = {"initial_cost": "Montant initial", "new_cost": "Montant actuel", 
                          "initial_total": "Total initial", "new_total": "Total actuel", 
                          "target_object": "Billet parent"}
            history_modification = history.modification
            modification_display = "<ul>"
            for modif_type_key in modif_type:
                modification_display += "<li>" + modif_type[modif_type_key] + ': ' + history_modification[modif_type_key] + "</li>"
            modification_display += "</ul>"
            temp_modification['modification'] = modification_display
            history_list.append(temp_modification)
        
        email_body = \
        """ <table
                style="border-collapse: collapse;width: 100%;">
            <thead class="bg-info">
                <tr>
                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Objet modifié</th>
                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">PNR associé</th>
                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Agent modificateur</th>
                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Date de la modification</th>
                    <th style="border:1px solid #ddd;padding:8px;padding-top:12px;padding-bottom:12px;text-align:left;background-color:#17a2b8;color:white;">Eléments modifiés</th>
                </tr>
            </thead>
            <tbody>"""
        for history in history_list:
            email_body += """<tr>"""
            for key in history:
                if key == 'modification_date':
                    email_body += """
                        <td style="border:1px solid #ddd;padding:8px;">{col_val}</td>
                    """.format(col_val=history[key].strftime("%d/%m/%Y %H:%M:%S"))
                else:
                    email_body += """<td style="border:1px solid #ddd;padding:8px;">{col_val}</td>""".format(col_val=history[key])
                
            email_body += """ </tr>"""
        
        email_body += """
            </tbody>
        </table> """
        
        message = \
        """
            <!DOCTYPE html>
            <html>
            <body>
                <p> Bonjour, </p>
                <p> Vous trouverez ci-après la liste des diminutions de frais de service passées à l'aéroport pour le {list_issuing_date}.</p>
                <p> Bonne réception. </p>
                <p> Cordialement, </p>
                {email_body}
            </body>
            </html>
        """.format(list_issuing_date=datetime.datetime.now().strftime("%d/%m/%Y"), email_body=email_body)
        
        subject = f"Rapport des modifications de frais de service accordées"
        
        # send current content as email for administrator
        mgbi_users_mail = FEE_HISTORY_REPORT_LOCAL_RECIPIENTS
        
        other_users_mail = FEE_HISTORY_REPORT_CUSTOMER_RECIPIENTS
        
        if len(final_target_history_list) > 0:
            Sending.send_email(
                "issoufali.pnr@outlook.com", 
                mgbi_users_mail + other_users_mail, 
                # ['famenontsoa@outlook.com'],
                subject=subject, 
                body=message
            )