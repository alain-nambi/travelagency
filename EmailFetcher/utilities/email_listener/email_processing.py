"""email_processing: Optional processing methods to be used with EmailListener.listen().

Example:

    # Create the EmailListener
    email = "example@gmail.com"
    password = "badpassword"
    folder = "Inbox"
    attachment_dir = "/path/to/attachments"
    el = EmailListener(email, password, folder, attachment_dir)

    # Pass to the listen() function
    timeout = 5
    el.listen(timeout, process_func=write_txt_file)

"""

# Imports from other packages
import json
import os
import traceback
import datetime
# Imports from this package
from email_listener.email_responder import EmailResponder
import AmadeusDecoder.utilities.configuration_data as configs

def write_txt_file(msg_dict, folder):
    """Write the email message data returned from scrape to text files.

    Args:
        email_listener (EmailListener): The EmailListener object this function
            is used with.
        msg_dict (dict): The dictionary of email message data returned by the
            scraping function.

    Returns:
        A list of file paths of files that were created and written to.

    """

    # List of files to be returned
    file_list = []
    attachment_list = []
    # For each key, create a file and ensure it doesn't exist
    for key in msg_dict.keys():
        temp_content = {}
        
        email_date = None
        if 'email_date' in msg_dict[key]:
            email_date = msg_dict[key]['email_date']
        file_path = os.path.join(folder[key], "{}.txt".format(key))
        temp_content['email_date'] = email_date
        temp_content['file_path'] = file_path
        
        if os.path.exists(file_path):
            print("File has already been created.")
            continue

        # Open the file
        file = None
        # Convert the message data to a string, and write it to the file
        msg_string = __msg_to_str(msg_dict[key])
        try:
            try:
                file = open(file_path, "w+")
                file.write(msg_string)
            except:
                file = open(file_path, "w+", encoding="utf-8")
                file.write(msg_string)
        except:
            error_path = os.path.join(os.getcwd(), 'error.txt')
            with open(error_path, 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                traceback.print_exc(file=error_file)
                error_file.write('\n')
        finally:
            if file is not None:
                file.close()
        # Add the file name to the return list
        file_list.append(temp_content)
        # Add attachment_list
        if 'attachments' in msg_dict[key]:
            if msg_dict[key]['attachments'][0].split('.')[-1] == 'pdf' :
                temp_content_ewa_pdf = {}
                temp_content_ewa_pdf['email_date'] = email_date
                temp_content_ewa_pdf['attachment'] = msg_dict[key]['attachments']
                
                attachment_list.append(temp_content_ewa_pdf)

    return file_list, attachment_list


def __msg_to_str(msg):
    """Convert a dictionary containing message data to a string.

    Args:
        msg (dict): The dictionary containing the message data.

    Returns:
        A string version of the message

    """

    # String to be returned
    msg_string = ""
    
    # Append the subject
    subject = msg.get('Subject')
    msg_string += "Subject\n\n{}\n\n\n".format(subject)

    # Append the plain text
    plain_text = msg.get('Plain_Text')
    if plain_text is not None:
        msg_string += "Plain_Text\n\n{}\n\n\n".format(plain_text)

    # Append the plain html and html
    plain_html = msg.get('Plain_HTML')
    html = msg.get('HTML')
    if plain_html is not None:
        msg_string += "Plain_HTML\n\n{}\n\n\n".format(plain_html)
        msg_string += "HTML\n\n{}\n\n\n".format(html)

    # Append the attachment list
    attachments = msg.get('attachments')
    if attachments is None:
        return msg_string

    msg_string += "attachments\n\n"
    for file in attachments:
        msg_string += "{}\n".format(file)

    return msg_string


def send_basic_reply(email_listener, msg_dict):
    """Write the messages to files, and then send a simple automated reply.

    Args:
        email_listener (EmailListener): The EmailListener object this function
            is used with.
        msg_dict (dict): The dictionary of email message data returned by the
            scraping function.

    Returns:
        A list of file paths of files that were created and written to.

    """

    # Write the email messages to files for use later
    file_list = write_txt_file(msg_dict)

    er = EmailResponder(email_listener.email, email_listener.app_password)
    er.login()

    # Create the automated response
    subject = "Thank you!"
    message = "Thank you for your email, your request is being processed."

    # For each email
    for key in msg_dict.keys():
        # Split the key up to remove the email uid
        sender_email_parts = key.split('_')
        sender_email = "_".join(sender_email_parts[1:])
        # Send the email
        er.send_singlepart_msg(sender_email, subject, message)

    er.logout()

    return file_list


def write_json_file(email_listener, msg_dict):
    """Write the email message data returned from scrape to json files.

    Args:
        email_listener (EmailListener): The EmailListener object this function
            is used with.
        msg_dict (dict): The dictionary of email message data returned by the
            scraping function.

    Returns:
        A list of file paths of files that were created and written to.

    """

    # List of files to be returned
    file_list = []
    # For each key, create a file and ensure it doesn't exist
    for key in msg_dict.keys():
        file_path = os.path.join(email_listener.attachment_dir, "{}.json".format(key))
        if os.path.exists(file_path):
            print("File has already been created.")
            continue

        # Convert the returned dict to json
        json_obj = json.dumps(msg_dict[key], indent = 4)

        # Open the file
        file = open(file_path, "w+")
        # Write the json object to the file
        file.write(json_obj)
        file.close()
        # Add the file name to the return list
        file_list.append(file_path)

    return file_list