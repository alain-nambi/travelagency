# if receipt_pnr has sent -> ssl.SSLEOFError: EOF occurred in violation of protocol (_ssl.c:2426)

import imaplib
import email
import ssl

class EmailListener:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.imap_host = 'imap.gmail.com'
        self.imap_port = 993
    
    def fetch_email(self):
        try:
            # Connect to Gmail IMAP server
            context = ssl.create_default_context()
            self.imap_conn = imaplib.IMAP4_SSL(self.imap_host, self.imap_port, ssl_context=context)
            self.imap_conn.login(self.username, self.password)
            print("Successfully connected to Gmail IMAP server.")
            
            # Select the INBOX folder
            self.imap_conn.select('INBOX')
            
            # Call the listen method to start fetching emails
            self.listen()
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def listen(self):
        try:
            # Enter IDLE mode to listen for new messages
            self.imap_conn.idle()
            print("Entered IDLE mode. Listening for new messages...")
            
            # Keep the connection alive indefinitely
            while True:
                # Check for any new messages or updates
                responses = self.imap_conn.idle_check(timeout=30)
                if responses:
                    print("New messages or updates received.")
                    # Process the new messages or updates here
                    self.process_emails()
                else:
                    print("No new messages or updates received. Continuing to listen...")
        except (ssl.SSLEOFError, imaplib.IMAP4.abort, BrokenPipeError) as e:
            # Handle SSL EOF error or other connection-related errors
            print(f"Connection error: {e}. Retrying...")
            # Close the current connection and attempt to reconnect
            self.imap_conn.logout()
            self.fetch_email()  # Attempt to reconnect and fetch emails again
        except Exception as e:
            print(f"An error occurred: {e}")
            # Handle other exceptions here
    
    def process_emails(self):
        # Fetch the latest email(s) from the INBOX folder
        result, data = self.imap_conn.search(None, 'ALL')
        if result == 'OK':
            for num in data[0].split():
                result, email_data = self.imap_conn.fetch(num, '(RFC822)')
                if result == 'OK':
                    raw_email = email_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    # Process the email message
                    print("Subject:", msg['Subject'])
                    print("From:", msg['From'])
                    print("Date:", msg['Date'])
                    print("Body:", msg.get_payload())
        else:
            print("Error fetching emails.")

if __name__ == "__main__":
    # Replace 'your_username' and 'your_password' with your Gmail credentials
    username = 'your_username@gmail.com'
    password = 'your_password'
    
    el = EmailListener(username, password)
    el.fetch_email()
