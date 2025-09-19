from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import smtplib
from email.mime.base import MIMEBase
from email import encoders
import os
import AmadeusDecoder.utilities.configuration_data as configs

# EMAIL_SENDING_ERROR_NOTIFICATION_RECIPIENTS = [
#     'nasolo@phidia.onmicrosoft.com',
#     'mihaja@phidia.onmicrosoft.com',
#     'alain@phidia.onmicrosoft.com',
#     'remi@phidia.onmicrosoft.com',
#     'famenontsoa@outlook.com',
#     'tahina@phidia.onmicrosoft.com',
#     'pp@phidia.onmicrosoft.com']
# EMAIL_SENDING_ERROR_NOTIFICATION = {"port":587, "smtp":"smtp.gmail.com", "address":"errorreport.issoufali.pnr@gmail.com", "password":"chnversafifnzagp"}
# ANOMALY_EMAIL_SENDER = {"port":587, "smtp":"smtp.gmail.com", "address":"anomalie.issoufali@alita.re", "password":"qczyzeytdvlbcysq"}
# PNR_NOT_FETCHED_NOTIFICATION_SENDER = {"port":587, "smtp":"smtp.gmail.com", "address":"anomalie.issoufali@alita.re", "password":"qczyzeytdvlbcysq"}
# FEE_REQUEST_SENDER = {"port":587, "smtp":"smtp.gmail.com", "address":"feerequest.issoufali.pnr@gmail.com", "password":"tnkunwvygtdkxfxg"}
# PNR_PARSING_ERROR_NOTIFICATION_SENDER = {"port":587, "smtp":"smtp.gmail.com", "address":"errorreport.issoufali.pnr@gmail.com", "password":"chnversafifnzagp"}
# PNR_PARSING_ERROR_NOTIFICATION_RECIPIENTS = [
#     'nasolo@phidia.onmicrosoft.com',
#     'mihaja@phidia.onmicrosoft.com',
#     'alain@phidia.onmicrosoft.com',
#     'remi@phidia.onmicrosoft.com',
#     'famenontsoa@outlook.com',
#     'tahina@phidia.onmicrosoft.com',
#     'pp@phidia.onmicrosoft.com']

EMAIL_SENDING_ERROR_NOTIFICATION_RECIPIENTS = configs.EMAIL_SENDING_ERROR_NOTIFICATION_RECIPIENTS
EMAIL_SENDING_ERROR_NOTIFICATION = configs.EMAIL_SENDING_ERROR_NOTIFICATION
ANOMALY_EMAIL_SENDER = configs.ANOMALY_EMAIL_SENDER
PNR_NOT_FETCHED_NOTIFICATION_SENDER = configs.PNR_NOT_FETCHED_NOTIFICATION_SENDER
FEE_REQUEST_SENDER = configs.FEE_REQUEST_SENDER
PNR_PARSING_ERROR_NOTIFICATION_SENDER = configs.PNR_PARSING_ERROR_NOTIFICATION_SENDER
PNR_PARSING_ERROR_NOTIFICATION_RECIPIENTS = configs.PNR_PARSING_ERROR_NOTIFICATION_RECIPIENTS

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
        email_sender = EMAIL_SENDING_ERROR_NOTIFICATION['address']
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = subject

        message.attach(MIMEText(body, 'html'))

        try:
            # server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server = smtplib.SMTP(EMAIL_SENDING_ERROR_NOTIFICATION["smtp"], int(EMAIL_SENDING_ERROR_NOTIFICATION["port"]))
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_SENDING_ERROR_NOTIFICATION["address"], EMAIL_SENDING_ERROR_NOTIFICATION["password"])
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
    def send_email(sender, recipients, subject, body, attachments=None):

        try:
            message = MIMEMultipart()
            email_sender = ANOMALY_EMAIL_SENDER["address"]
            password = ANOMALY_EMAIL_SENDER["password"].strip().rstrip('\r\n')

            message['From'] = email_sender
            message['To'] = ";".join(recipients)
            message['Subject'] = subject + " - Application Gestion PNR"

            message.attach(MIMEText(body, 'html'))

            # 📎 Ajout des pièces jointes s'il y en a
            if attachments:
                for file_path in attachments:
                    try:
                        with open(file_path, "rb") as f:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                "Content-Disposition",
                                f'attachment; filename="{os.path.basename(file_path)}"'
                            )
                            message.attach(part)
                    except Exception as e:
                        print(f"Erreur lors de l'attachement du fichier {file_path} : {e}")
            
            # Connexion avec méthode d'authentification explicite
            server = smtplib.SMTP(ANOMALY_EMAIL_SENDER['smtp'], int(ANOMALY_EMAIL_SENDER['port']))
            server.set_debuglevel(1)
            server.ehlo()
            if server.has_extn('STARTTLS'):
                server.starttls()
                server.ehlo()
        
            # Essayer différentes méthodes d'authentification
            try:
                # Méthode 1: LOGIN
                server.login(email_sender, password)
            except smtplib.SMTPAuthenticationError:
                try:
                    # Méthode 2: PLAIN
                    auth_string = f"\0{email_sender}\0{password}"
                    server.docmd("AUTH", "PLAIN " + base64.b64encode(auth_string.encode()).decode())
                except:
                    # Méthode 3: CRAM-MD5 (si disponible)
                    import hmac, hashlib
                    def auth_cram_md5(challenge, email_sender, password):
                        challenge = base64.b64decode(challenge)
                        response = hmac.HMAC(password.encode(), challenge, hashlib.md5).hexdigest()
                        return base64.b64encode(f"{email_sender} {response}".encode()).decode()
                    
                    resp = server.docmd("AUTH", "CRAM-MD5")
                    if resp[0] == 334:
                        server.docmd(auth_cram_md5(resp[1].decode(), email_sender, password))
        
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print(f"{datetime.now()} NOTE: Email sent to {recipients}")
            server.quit()
            return True
        
        except Exception as e:
            print(f"{datetime.now()} ERROR: {e}")
            return False

    @staticmethod
    def send_email_pnr_not_fetched(sender, recipients, subject, body):
        print("++++++++++++++++++ INIT SENDING PNR NOT FETCHED MAIL ++++++++++++++++++")
        message = MIMEMultipart()
        email_sender = PNR_NOT_FETCHED_NOTIFICATION_SENDER['address']
        password = PNR_NOT_FETCHED_NOTIFICATION_SENDER["password"].strip().rstrip('\r\n')
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = "Application Gestion PNR - " + subject

        message.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP(PNR_NOT_FETCHED_NOTIFICATION_SENDER['smtp'], int(PNR_NOT_FETCHED_NOTIFICATION_SENDER['port']))
            server.set_debuglevel(1)
            server.ehlo()
            if server.has_extn('STARTTLS'):
                server.starttls()
                server.ehlo()
        
            # Essayer différentes méthodes d'authentification
            try:
                # Méthode 1: LOGIN
                server.login(email_sender, password)
            except smtplib.SMTPAuthenticationError:
                try:
                    # Méthode 2: PLAIN
                    auth_string = f"\0{email_sender}\0{password}"
                    server.docmd("AUTH", "PLAIN " + base64.b64encode(auth_string.encode()).decode())
                except:
                    # Méthode 3: CRAM-MD5 (si disponible)
                    import hmac, hashlib
                    def auth_cram_md5(challenge, email_sender, password):
                        challenge = base64.b64decode(challenge)
                        response = hmac.HMAC(password.encode(), challenge, hashlib.md5).hexdigest()
                        return base64.b64encode(f"{email_sender} {response}".encode()).decode()
                    
                    resp = server.docmd("AUTH", "CRAM-MD5")
                    if resp[0] == 334:
                        server.docmd(auth_cram_md5(resp[1].decode(), email_sender, password))
        
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print(f"{datetime.now()} NOTE: Email sent to {recipients}")
            server.quit()
            return True
        
        except Exception as e:
            print(f"{datetime.now()} ERROR: {e}")
            return False

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
        print("++++++++++++++++++ INIT SENDING REQUEST MAIL ++++++++++++++++++")
        message = MIMEMultipart()
        email_sender = FEE_REQUEST_SENDER['address']
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = subject + " - Application Gestion PNR"

        message.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP(FEE_REQUEST_SENDER['smtp'], int(FEE_REQUEST_SENDER['port']))
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(FEE_REQUEST_SENDER['address'], FEE_REQUEST_SENDER['password'])
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print("{} NOTE: Email sent to \"{}\" address.".format(
                datetime.now(), recipients))
            server.quit()
        except Exception as e:
            print("{} ERROR: SMTP server connection error.".format(datetime.now()))
            print("{} ERROR: {}".format(datetime.now(), e))
            Sending().catch_error_on_sending_email(FEE_REQUEST_SENDER['address'])
            
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
        email_sender = PNR_PARSING_ERROR_NOTIFICATION_SENDER['address']
        
        message['From'] = email_sender
        message['To'] = ";".join(recipients)
        message['Subject'] = subject

        message.attach(MIMEText(body, 'html'))

        try:
            # server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server = smtplib.SMTP(PNR_PARSING_ERROR_NOTIFICATION_SENDER['smtp'], int(PNR_NOT_FETCHED_NOTIFICATION_SENDER['port']))
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(PNR_PARSING_ERROR_NOTIFICATION_SENDER['address'], PNR_NOT_FETCHED_NOTIFICATION_SENDER['password'])
            text = message.as_string()
            server.sendmail(email_sender, recipients, text)
            print("{} NOTE: Email sent to \"{}\" address.".format(
                datetime.now(), recipients))
            server.quit()
        except Exception as e:
            print("{} ERROR: SMTP server connection error.".format(datetime.now()))
            print("{} ERROR: {}".format(datetime.now(), e))

        return True