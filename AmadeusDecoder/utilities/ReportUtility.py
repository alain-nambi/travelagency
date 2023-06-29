'''
Created on Jun 20, 2023

@author: Famenontsoa
'''
import os
import django
from AmadeusDecoder.utilities.SendMail import Sending

FEE_HISTORY_REPORT_LOCAL_RECIPIENTS = [
            "phpr974@gmail.com",
            "pp@phidia.onmicrosoft.com",
            # "nasolo@phidia.onmicrosoft.com",
            "mihaja@phidia.onmicrosoft.com",
            "tahina@phidia.onmicrosoft.com",
            # "remi@phidia.onmicrosoft.com",
            # "famenontsoa@outlook.com",
            # "alain@phidia.onmicrosoft.com",
        ]

FEE_HISTORY_REPORT_CUSTOMER_RECIPIENTS = other_users_mail = [
            "stephanie@agences-issoufali.com",
            # "fahar@agences-issoufali.com",
            # "samir@agences-issoufali.com",
            # "oulfate@agences-issoufali.com",
            # "mraati@agences-issoufali.com",
            # "fouadi@agences-issoufali.com",
            # "roihamina@agences-issoufali.com",
            # "mouniati@agences-issoufali.com",
            # "sylvia@agences-issoufali.com",
            # "anziza@agences-issoufali.com",
            # "sejours@agences-issoufali.com",
            # "sarmada@agences-issoufali.com",
            # "lola@agences-issoufali.com",
            # "farida@agences-issoufali.com",
            # "goula@agences-issoufali.com",
            # "saouda@agences-issoufali.com",
            # "riziki@agences-issoufali.com",
            # "karim@agences-issoufali.com",
            # "josianenovou@agences-issoufali.com",
            # "anaissa@agences-issoufali.com",
            # "hassanati@agences-issoufali.com",
            # "saidmaoulida@agences-issoufali.com",
            # "madjid@agences-issoufali.com",
            # "sity@agences-issoufali.com",
            # "koro@agences-issoufali.com",
            "issoufali.pnr@outlook.com",
            # "danielbehava2@agences-issoufali.com",
            "david.domitin@agences-issoufali.com",
            # "eric@agences-issoufali.com",
            # "taanli@agences-issoufali.com",
            # "shoulaya@agences-issoufali.com",
        ]


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'DjangoTravelAgency.settings'
)
django.setup()

from AmadeusDecoder.models.history.History import History
import datetime

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
        
        history_list = []
        for history in target_history_list:
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
                <p> Vous trouverez ci-après la liste des diminutions de frais de service accordées pour le {list_issuing_date}.</p>
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
        
        if len(target_history_list) > 0:
            Sending.send_email(
                "issoufali.pnr@outlook.com", 
                mgbi_users_mail + other_users_mail, 
                # ['famenontsoa@outlook.com'],
                subject=subject, 
                body=message
            )