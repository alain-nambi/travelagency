from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import smtplib

class Sending():

    # send error on error
    def catch_error_on_sending_email(self, email_address):
        recipients = ["nasolo@phidia.onmicrosoft.com",
         "mihaja@phidia.onmicrosoft.com",
         "alain@phidia.onmicrosoft.com",
         "remi@phidia.onmicrosoft.com",
         "famenontsoa@outlook.com",
         "tahina@phidia.onmicrosoft.com",
         "pp@phidia.onmicrosoft.com"
         ]
        
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
        email_sender = "errorreport.issoufali.pnr@gmail.com"
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = subject

        message.attach(MIMEText(body, 'html'))

        try:
            # server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("errorreport.issoufali.pnr@gmail.com", "chnversafifnzagp")
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
        email_sender = "anomalie.issoufali.pnr@gmail.com"
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = subject + " - Application Gestion PNR"

        message.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("anomalie.issoufali.pnr@gmail.com", "qczyzeytdvlbcysq")
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print("{} NOTE: Email sent to \"{}\" address.".format(
                datetime.now(), recipients))
            server.quit()
        except Exception as e:
            print("{} ERROR: SMTP server connection error.".format(datetime.now()))
            print("{} ERROR: {}".format(datetime.now(), e))
            Sending().catch_error_on_sending_email("anomalie.issoufali.pnr@gmail.com")
            
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
        email_sender = "anomalie.issoufali.pnr@gmail.com"
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = "Application Gestion PNR - " + subject

        message.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("anomalie.issoufali.pnr@gmail.com", "qczyzeytdvlbcysq")
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print("{} NOTE: Email sent to \"{}\" address.".format(
                datetime.now(), recipients))
            server.quit()
        except Exception as e:
            print("{} ERROR: SMTP server connection error.".format(datetime.now()))
            print("{} ERROR: {}".format(datetime.now(), e))
            Sending().catch_error_on_sending_email("anomalie.issoufali.pnr@gmail.com")
            
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
        email_sender = "feerequest.issoufali.pnr@gmail.com"
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = subject + " - Application Gestion PNR"

        message.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("feerequest.issoufali.pnr@gmail.com", "tnkunwvygtdkxfxg")
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print("{} NOTE: Email sent to \"{}\" address.".format(
                datetime.now(), recipients))
            server.quit()
        except Exception as e:
            print("{} ERROR: SMTP server connection error.".format(datetime.now()))
            print("{} ERROR: {}".format(datetime.now(), e))
            Sending().catch_error_on_sending_email("feerequest.issoufali.pnr@gmail.com")
            
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
        
        recipients = [
            "nasolo@phidia.onmicrosoft.com",
            "mihaja@phidia.onmicrosoft.com",
            "alain@phidia.onmicrosoft.com",
            "remi@phidia.onmicrosoft.com",
            "famenontsoa@outlook.com",
            "tahina@phidia.onmicrosoft.com"
            # "pp@phidia.onmicrosoft.com"
        ]
        
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
        email_sender = "errorreport.issoufali.pnr@gmail.com"
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = subject

        message.attach(MIMEText(body, 'html'))

        try:
            # server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("errorreport.issoufali.pnr@gmail.com", "chnversafifnzagp")
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print("{} NOTE: Email sent to \"{}\" address.".format(
                datetime.now(), recipients))
            server.quit()
        except Exception as e:
            print("{} ERROR: SMTP server connection error.".format(datetime.now()))
            print("{} ERROR: {}".format(datetime.now(), e))

        return True
