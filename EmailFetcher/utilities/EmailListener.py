'''
Created on 18 Aug 2022

@author: Famenontsoa
'''
import traceback
import datetime
import os

from EmailFetcher.utilities import email_listener
# from EmailFetcher.utilities import email_listener_outlook as email_listener

class EmailListener():
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
           '''
        self._email = ''
        self._app_password = ''
        self._folder = ''
        self._attachments_dir = ''
        self._email_listener_obj = ''

    def get_email_listener_obj(self):
        return self.__email_listener_obj

    def get_email(self):
        return self.__email

    def get_app_password(self):
        return self.__app_password

    def get_folder(self):
        return self.__folder

    def get_attachments_dir(self):
        return self.__attachments_dir

    def set_email(self, value):
        if value == '' or value is None:
            raise ValueError('Email cannot be void')
        self.__email = value

    def set_app_password(self, value):
        if value == '' or value is None:
            raise ValueError('Password cannot be void')
        self.__app_password = value

    def set_folder(self, value):
        if value == '' or value is None:
            raise ValueError('Folder cannot be void')
        self.__folder = value

    def set_attachments_dir(self, value):
        if value == '' or value is None:
            raise ValueError('Attachments directory cannot be void')
        self.__attachments_dir = value
        
    def set_email_listener_obj(self, value):
        self.__email_listener_obj = value

    def del_email(self):
        del self.__email

    def del_app_password(self):
        del self.__app_password

    def del_folder(self):
        del self.__folder

    def del_attachments_dir(self):
        del self.__attachments_dir
    
    def del_email_listener_obj(self):
        del self.__email_listener_obj

    email = property(get_email, set_email, del_email, "email's docstring")
    app_password = property(get_app_password, set_app_password, del_app_password, "app_password's docstring")
    folder = property(get_folder, set_folder, del_folder, "folder's docstring")
    attachments_dir = property(get_attachments_dir, set_attachments_dir, del_attachments_dir, "attachments_dir's docstring")
    email_listener_obj = property(get_email_listener_obj, set_email_listener_obj, del_email_listener_obj, "email_listener_obj's docstring")
    
    # fetch email and attachments
    def fetch_email(self):
        el = None
        try:
            el = email_listener.EmailListener(self.email, self.app_password, self.folder, self.attachments_dir)
            el.login()
            el.listen()
        except Exception as e:
            if el is not None:
                try:
                    el.logout()
                except:
                    pass
            self.fetch_email()
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                traceback.print_exc(file=error_file)
                error_file.write('\n')
    
'''
print('Passed here')
email = "travelagency.mgbi@gmail.com"
app_password = "ksoqlemqpuptzfkn"
folder = "Inbox"
attachment_dir = "attachements_dir/"
el = email_listener.EmailListener(email, app_password, folder, attachment_dir)

el.login()

messages = el.scrape()
print(messages)

timeout = 1
el.listen(timeout)'''