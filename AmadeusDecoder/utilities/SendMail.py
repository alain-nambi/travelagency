from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import smtplib

EMAIL_SENDING_ERROR_NOTIFICATION_RECIPIENTS = [
    "nasolo@phidia.onmicrosoft.com",
         "mihaja@phidia.onmicrosoft.com",
         "alain@phidia.onmicrosoft.com",
         "remi@phidia.onmicrosoft.com",
         "famenontsoa@outlook.com",
         "tahina@phidia.onmicrosoft.com",
         "pp@phidia.onmicrosoft.com"
]
EMAIL_SENDING_ERROR_NOTIFICATION_SENDER = ["errorreport.issoufali.pnr@gmail.com"]
EMAIL_SENDING_ERROR_NOTIFICATION_SENDER_PASSWORD = ["chnversafifnzagp"]
EMAIL_SENDING_ERROR_NOTIFICATION_SENDER_SMTP = ["smtp.gmail.com"]
EMAIL_SENDING_ERROR_NOTIFICATION_SENDER_PORT = [587]

ANOMALY_EMAIL_SENDER = ["anomalie.issoufali.pnr@gmail.com"]
ANOMALY_EMAIL_SENDER_SMTP = ["smtp.gmail.com"]
ANOMALY_EMAIL_SENDER_PORT = [587]
ANOMALY_EMAIL_SENDER_PASSWORD = ["qczyzeytdvlbcysq"]

PNR_NOT_FETCHED_NOTIFICATION_SENDER = ["anomalie.issoufali.pnr@gmail.com"]
PNR_NOT_FETCHED_NOTIFICATION_SENDER_SMTP = ["anomalie.issoufali.pnr@gmail.com"]
PNR_NOT_FETCHED_NOTIFICATION_SENDER_PORT = [587]
PNR_NOT_FETCHED_NOTIFICATION_SENDER_PASSWORD = ["qczyzeytdvlbcysq"]

FEE_REQUEST_SENDER = ["feerequest.issoufali.pnr@gmail.com"]
FEE_REQUEST_SENDER_SMTP = ["smtp.gmail.com"]
FEE_REQUEST_SENDER_PORT = [587]
FEE_REQUEST_SENDER_PASSWORD = ["tnkunwvygtdkxfxg"]

PNR_PARSING_ERROR_NOTIFICATION_SENDER = ["errorreport.issoufali.pnr@gmail.com"]
PNR_PARSING_ERROR_NOTIFICATION_SENDER_SMTP = ["smtp.gmail.com"]
PNR_PARSING_ERROR_NOTIFICATION_SENDER_PORT = [587]
PNR_PARSING_ERROR_NOTIFICATION_SENDER_PASSWORD = ["chnversafifnzagp"]
PNR_PARSING_ERROR_NOTIFICATION_RECIPIENTS = [
            "nasolo@phidia.onmicrosoft.com",
            "mihaja@phidia.onmicrosoft.com",
            "alain@phidia.onmicrosoft.com",
            "remi@phidia.onmicrosoft.com",
            "famenontsoa@outlook.com",
            "tahina@phidia.onmicrosoft.com"
            "pp@phidia.onmicrosoft.com"
        ]

class Sending():
    
    def __init__(self):
        '''
        '''

    # send error on error
    def catch_error_on_sending_email(self, email_address):
        recipients = EMAIL_SENDING_ERROR_NOTIFICATION_RECIPIENTS
        
        subject = "Email error"
        
        body = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Email error</title>
            
            </head>
            <body>
                <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                    Bonjour,<br /><br />
                </p>
                <p>
                    Une erreur est survenue lors de l'envoi de l'email.
                </p>
                <p>
                    Adresse avec erreur: {email_target}
                </p>
                <p>
                    Bien cordialement.
                </p>
            </body>
            </html>
            """.format(email_target=email_address)
        
        message = MIMEMultipart()
        email_sender = EMAIL_SENDING_ERROR_NOTIFICATION_SENDER[0]
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = subject

        message.attach(MIMEText(body, 'html'))

        try:
            # server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server = smtplib.SMTP(EMAIL_SENDING_ERROR_NOTIFICATION_SENDER_SMTP[0], EMAIL_SENDING_ERROR_NOTIFICATION_SENDER_PORT[0])
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_SENDING_ERROR_NOTIFICATION_SENDER[0], EMAIL_SENDING_ERROR_NOTIFICATION_SENDER_PASSWORD[0])
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print("{} NOTE: Email sent to \"{}\" address.".format(
                datetime.now(), recipients))
            server.quit()
        except Exception as e:
            print("{} ERROR: SMTP server connection error.".format(datetime.now()))
            print("{} ERROR: {}".format(datetime.now(), e))

        return True
    
    '''Class use when sending mail notification'''
    @staticmethod
    def send_email(sender, recipients, subject, body):

        message = MIMEMultipart()
        email_sender = ANOMALY_EMAIL_SENDER[0]
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = subject + " - Application Gestion PNR"

        message.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP(ANOMALY_EMAIL_SENDER[0], ANOMALY_EMAIL_SENDER_PORT[0])
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(ANOMALY_EMAIL_SENDER[0], ANOMALY_EMAIL_SENDER_PASSWORD[0])
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print("{} NOTE: Email sent to \"{}\" address.".format(
                datetime.now(), recipients))
            server.quit()
        except Exception as e:
            print("{} ERROR: SMTP server connection error.".format(datetime.now()))
            print("{} ERROR: {}".format(datetime.now(), e))
            Sending().catch_error_on_sending_email(ANOMALY_EMAIL_SENDER[0])
            
        return True
    
    # '''Class use when sending mail notification'''
    # @staticmethod
    # def send_email_pnr_not_sent(sender, recipients, subject, body):
    #     message = MIMEMultipart()
    #     email_sender = "anomalie.issoufali.pnr@gmail.com"
        
    #     message['From'] = email_sender
    #     message['To'] = ";".join(recipients)
    #     message['Subject'] = subject + " - Application Gestion PNR"

    #     message.attach(MIMEText(body, 'html'))

    #     try:
    #         server = smtplib.SMTP('smtp.gmail.com', 587)
    #         server.ehlo()
    #         server.starttls()
    #         server.ehlo()
    #         server.login("anomalie.issoufali.pnr@gmail.com", "qczyzeytdvlbcysq")
    #         text = message.as_string()
    #         server.sendmail(email_sender, recipients, text)
    #         print("{} NOTE: Email sent to \"{}\" address.".format(
    #             datetime.now(), recipients))
    #         server.quit()
    #     except Exception as e:
    #         print("{} ERROR: SMTP server connection error.".format(datetime.now()))
    #         print("{} ERROR: {}".format(datetime.now(), e))
    #         Sending().catch_error_on_sending_email("anomalie.issoufali.pnr@gmail.com")
            
    #     return True

    @staticmethod
    def send_email_pnr_not_fetched(sender, recipients, subject, body):

        message = MIMEMultipart()
        email_sender = PNR_NOT_FETCHED_NOTIFICATION_SENDER[0]
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = "Application Gestion PNR - " + subject

        message.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP(PNR_NOT_FETCHED_NOTIFICATION_SENDER_SMTP[0], PNR_NOT_FETCHED_NOTIFICATION_SENDER_PORT[0])
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(PNR_NOT_FETCHED_NOTIFICATION_SENDER[0], PNR_NOT_FETCHED_NOTIFICATION_SENDER_PASSWORD[0])
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print("{} NOTE: Email sent to \"{}\" address.".format(
                datetime.now(), recipients))
            server.quit()
        except Exception as e:
            print("{} ERROR: SMTP server connection error.".format(datetime.now()))
            print("{} ERROR: {}".format(datetime.now(), e))
            Sending().catch_error_on_sending_email(PNR_NOT_FETCHED_NOTIFICATION_SENDER[0])
            
        return True

    @staticmethod
    def send_email_error(sender, recipients, subject, body):

        message = MIMEMultipart()
        email_sender = "error.issoufali.pnr@outlook.com"
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = subject + " - Application Gestion PNR"

        message.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("error.issoufali.pnr@outlook.com", "Mgbi@261!+")
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print("{} NOTE: Email sent to \"{}\" address.".format(
                datetime.now(), recipients))
            server.quit()
        except Exception as e:
            print("{} ERROR: SMTP server connection error.".format(datetime.now()))
            print("{} ERROR: {}".format(datetime.now(), e))
            Sending().catch_error_on_sending_email("error.issoufali.pnr@outlook.com")

        return True
    
    @staticmethod
    def send_email_request(sender, recipients, subject, body):

        message = MIMEMultipart()
        email_sender = FEE_REQUEST_SENDER[0]
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = subject + " - Application Gestion PNR"

        message.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP(FEE_REQUEST_SENDER_SMTP[0], FEE_REQUEST_SENDER_PORT[0])
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(FEE_REQUEST_SENDER[0], FEE_REQUEST_SENDER_PASSWORD[0])
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print("{} NOTE: Email sent to \"{}\" address.".format(
                datetime.now(), recipients))
            server.quit()
        except Exception as e:
            print("{} ERROR: SMTP server connection error.".format(datetime.now()))
            print("{} ERROR: {}".format(datetime.now(), e))
            Sending().catch_error_on_sending_email(FEE_REQUEST_SENDER[0])
            
        return True

    @staticmethod
    def send_email_tjq(sender, recipients, subject, body):

        message = MIMEMultipart()
        email_sender = "tjq.issoufali.pnr@outlook.com"
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = subject + " - Application Gestion PNR"

        message.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("tjq.issoufali.pnr@outlook.com", "Mgbi@261!+")
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print("{} NOTE: Email sent to \"{}\" address.".format(
                datetime.now(), recipients))
            server.quit()
        except Exception as e:
            print("{} ERROR: SMTP server connection error.".format(datetime.now()))
            print("{} ERROR: {}".format(datetime.now(), e))
            Sending().catch_error_on_sending_email("tjq.issoufali.pnr@outlook.com")
            
        return True
    
    @staticmethod
    def send_email_pnr_parsing(not_parsed_file):
        
        recipients = PNR_PARSING_ERROR_NOTIFICATION_RECIPIENTS
        
        subject = "Connection already closed"
        
        body = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Database error</title>
            
            </head>
            <body>
                <p style="padding-bottom: 1%; padding-top: 1%; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                    Bonjour,<br /><br />
                </p>
                <p>
                    {error}
                </p>
                <p>
                    {not_parsed}
                </p>
                <p>
                    Bien cordialement.
                </p>
            </body>
            </html>
            """.format(error = "Les transactions au niveau de la base de données de Gestion PNR ont été suspendues."
                       , not_parsed = ("Fichier non-traité: " + not_parsed_file))
        
        message = MIMEMultipart()
        email_sender = PNR_PARSING_ERROR_NOTIFICATION_SENDER[0]
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = subject

        message.attach(MIMEText(body, 'html'))

        try:
            # server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server = smtplib.SMTP(PNR_PARSING_ERROR_NOTIFICATION_SENDER_SMTP[0], PNR_NOT_FETCHED_NOTIFICATION_SENDER_PORT[0])
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(PNR_PARSING_ERROR_NOTIFICATION_SENDER[0], PNR_NOT_FETCHED_NOTIFICATION_SENDER_PASSWORD[0])
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print("{} NOTE: Email sent to \"{}\" address.".format(
                datetime.now(), recipients))
            server.quit()
        except Exception as e:
            print("{} ERROR: SMTP server connection error.".format(datetime.now()))
            print("{} ERROR: {}".format(datetime.now(), e))

        return True
