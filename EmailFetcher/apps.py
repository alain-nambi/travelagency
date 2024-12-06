import shutil
from django.apps import AppConfig
from threading import Thread, Timer
import os
import traceback
#import schedule
import time
from django.apps.registry import apps

from datetime import datetime, timedelta, timezone


class RepeatTimer(Timer):  
    daemon=True 
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


'Function that call mail notification of direction'
def start_pnr_daily_report_schedule():
    from AmadeusDecoder.utilities.DailyPnrChecker import get_daily_pnr, notify_direction
    pnrs = get_daily_pnr() 
    today = datetime.now()
    if today.strftime('%H') == '19' and today.strftime('%M') == '15':
        notify_direction(pnrs)


def pnr_unissued_opc_checking():
    from AmadeusDecoder.utilities.PnrUnissuedOpcChecking import get_opc_as_datetime, notify_user
    print("OPC checking...")
    opcs = get_opc_as_datetime()
    tdate = datetime.now() + timedelta(1)
    strtdate = tdate.strftime('%Y-%m-%d %H:%M')
    
    for opc in opcs :
        opc_date = opc.doc_date.strftime('%Y-%m-%d %H:%M')
        if strtdate  ==  opc_date :
            notify_user(opc)

def tjq_mail_alert():
    from AmadeusDecoder.utilities.TjqMailAlert import alert_tjq
    
    tdate = datetime.now()
    checkdate = tdate.strftime('%Y-%m-%d %H:%M')
    mididate = tdate.strftime('%Y-%m-%d 13:50')
    enddate = tdate.strftime('%Y-%m-%d 19:30')
    
    if checkdate  ==  mididate or checkdate  == enddate :
        alert_tjq()

def process_data_control() :
    from AmadeusDecoder.utilities.ProcessDataControl import control_data_gp_odoo
    print("Process control data running...")
    tdate = datetime.now()
    checkdate = tdate.strftime('%Y-%m-%d %H:%M')
    mididate = tdate.strftime('%Y-%m-%d 15:47')
    if checkdate  ==  mididate :
        control_data_gp_odoo()

    

'Function checking call every second that will whech in ftp if there are new csv of products'
def running_product_synhcro():
    from AmadeusDecoder.utilities.FtpConnection import download_file
    product_dir = '/export/products'
    download_file(product_dir)


def checking_pnr_missing():
    from AmadeusDecoder.utilities.MailNotificationParser import MailNotification
    now = datetime.now(timezone.utc).replace(microsecond=0)
    # dt = '2022-12-28 09:26:51.000'
    # date_test = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=timezone.utc)
    MailNotification.pnr_missing_notification(now)


def checking_passenger_segment_missing():
    from AmadeusDecoder.utilities.MailNotificationParser import MailNotification
    now = datetime.now(timezone.utc).replace(microsecond=0)
    # dt = '2022-12-28 09:26:51.000'
    # date_test = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=timezone.utc)
    MailNotification.passenger_segment_missing_notification(now)

def get_all_missing_document():
    from AmadeusDecoder.utilities.MailNotificationParser import MailNotification
    MailNotification.all_passenger_segment_missing_notification()
    MailNotification.all_pnr_missing_notification()
    
def checking_pnr_not_uploaded_in_pnr_management():
    from AmadeusDecoder.utilities.MailNotificationParser import MailNotification
    now = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(hours=3)
    
    print("⚙️  PNR update checking...")
    MailNotification.pnr_upload_notification(now)
    
def checking_pnr_not_sent_to_odoo():
    from AmadeusDecoder.utilities.MailNotificationParser import MailNotification
    now = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(hours=3)
    
    # ==================== PNR not sent to Odoo checking ====================
    MailNotification.pnr_not_sent_to_odoo(now)
    
# # send fee modification history
def send_fee_update_list():
    from AmadeusDecoder.utilities.ReportUtility import ReportUtility
    
    current_time = datetime.now()
    
    if current_time.hour == 17:
        print('Fee history report is being processed.')
        ReportUtility().fee_history_report(datetime.now())
    
    # def task():
    #     ReportUtility().fee_history_report(datetime.now())
    #
    # # Schedule operation to run every day at 5:00 PM
    # schedule.every().day.at("17:00").do(task)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    
# Fonction that send fee decrease report everyday at 6am o'clock
def checking_pnr_with_fee_decrease_request():
    from AmadeusDecoder.utilities.MailNotificationParser import MailNotification
    now = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(hours=3)
    # print('---------------------------- COUCOU ------------------------------')
    # print(now)
    # ====================== PNR with fee decrease request ======================
    MailNotification.fee_decrease_request(now)

def fetch_email():
    try:
        import AmadeusDecoder.utilities.configuration_data as configs
        from EmailFetcher.utilities.EmailListener import EmailListener
        print('Email listener is starting')
        EMAIL_PNR = configs.EMAIL_PNR
        email_listener_obj = EmailListener()
        # email_listener_obj.email = "mercurevoyages.pnr@gmail.com"
        # email_listener_obj.app_password = "ftraxhoftbbkicps"
        print(EMAIL_PNR)
        email_listener_obj.email = EMAIL_PNR['address']
        email_listener_obj.app_password = EMAIL_PNR['password']
        # email_listener_obj.email = "issoufali.pnr@outlook.com"
        # email_listener_obj.app_password = "Mgbi@261!+"
        email_listener_obj.folder = "Inbox"
        email_listener_obj.attachments_dir = os.path.join(os.getcwd(), "EmailFetcher/utilities/attachments_dir/")
        email_listener_obj.fetch_email()
    except Exception:
        traceback.print_exc()
        with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
            error_file.write('{}: \n'.format(datetime.now()))
            traceback.print_exc(file=error_file)
            error_file.write('\n')

def load_config():
    print('Loading configurations ...')
    # assign current company to local variable 'session_variable'
    import AmadeusDecoder.utilities.configuration_data as configs
    import AmadeusDecoder.utilities.session_variables as session_variables
    from AmadeusDecoder.utilities.ConfigReader import ConfigReader
    # session_variables.current_company = ConfigReader.get_company()
    
    apps.get_models()
    # load company info
    ConfigReader.load_company_info()
    ConfigReader.load_email_source()
    ConfigReader.load_emd_parser_tool_data()
    ConfigReader.load_tst_parser_tool_data()
    ConfigReader.load_zenith_parser_tool_data()
    ConfigReader.load_zenith_parser_receipt_tool_data()
    ConfigReader.load_ticket_parser_tool_data()
    ConfigReader.load_fee_request_tool_data()
    ConfigReader.load_report_email_data()
    ConfigReader.load_pnr_parser_tool_data()
    
    # assign current company to local variable 'session_variable'
    session_variables.current_company = configs.COMPANY_NAME
    print('Configurations loaded.')
    
def delete_all_files_in_attachments_dir():
    """
    Deletes all files and directories recursively in the attachments directory.
    """
    print("*-- Deletes all files and directories recursively in the attachments directory --*")
    
    # Define the path to the attachments directory
    attachments_dir = os.path.join("/", "opt", "travelagency", "EmailFetcher", "utilities", "attachments_dir")
    
    # Iterate over all items (files and directories) in the attachments directory
    for item in os.scandir(attachments_dir):
        # Construct the full path to the current item
        item_path = os.path.join(attachments_dir, item.name)
        
        # Check if the item is a file
        if os.path.isfile(item_path):
            # Remove the file
            os.remove(item_path)
            print("📢 ========> Deleted file:", item_path)
        # Check if the item is a directory
        elif os.path.isdir(item_path):
            # Remove the directory and its contents recursively
            shutil.rmtree(item_path)
            print("📢 ========> Deleted directory:", item_path)
        else:
            # Handle the case if the item is neither a file nor a directory
            print("📢 ========> Unknown item type:", item_path)

class EmailfetcherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EmailFetcher'
    
    def ready(self):
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE_EMAIL')
        
        if run_once is not None:
            return
        os.environ['CMDLINERUNNER_RUN_ONCE_EMAIL'] = 'True'
        
        # load_configs = Thread(target=load_config)
        # load_configs.start()
        #
        
        email_thread_once = Thread(target=fetch_email)
        email_thread_once.start()

        now = datetime.now()
        repeat_timer_for_pnr_upload_notification = 0
        
        # Delete all files in attachments every 1 minutes 
        task_schedule = RepeatTimer(1 * 60, delete_all_files_in_attachments_dir)
        task_schedule.start()
        
        def pnr_upload_repeat_timer(repeat_timer_for_pnr_upload_notification):
            print("📢 Mail notification for pnr not updated in pnr management...")
            timer_update_check = RepeatTimer(repeat_timer_for_pnr_upload_notification, checking_pnr_not_uploaded_in_pnr_management)
            timer_update_check.start()
    
        if now.weekday() in [0, 1, 2, 3, 4]: # [Lundi, Mardi, Mercredi, Jeudi, Vendredi]            
            repeat_timer_for_pnr_upload_notification = 10 * 60
            pnr_upload_repeat_timer(repeat_timer_for_pnr_upload_notification)
        if now.weekday() in [5]: # [Samedi]            
            repeat_timer_for_pnr_upload_notification = 60 * 60
            pnr_upload_repeat_timer(repeat_timer_for_pnr_upload_notification)
        if now.weekday() in [6]: # [Dimanche]
            repeat_timer_for_pnr_upload_notification = 60 * 180
            pnr_upload_repeat_timer(repeat_timer_for_pnr_upload_notification)
        
        # print("==================== Mail notification for pnr not sent to Odoo ====================")
        # timer_update_check = RepeatTimer(1, checking_pnr_not_sent_to_odoo)
        # timer_update_check.start()
        
        print('Mail notification is starting....')
        timer_pnr_misssing = RepeatTimer(1, checking_pnr_missing)
        timer_pnr_misssing.start()
        timer_passenger_segment_missing = RepeatTimer(1, checking_passenger_segment_missing)
        timer_passenger_segment_missing.start()

        # print('Daily Pnr created starting')
        # timer_schedule = RepeatTimer(60, start_pnr_daily_report_schedule)
        # timer_schedule.start()

        print('Pnr unissued OPC checking is running...')
        timer = RepeatTimer(60, pnr_unissued_opc_checking)  
        timer.start()
        
        print("📢 ==================== Mail notification for pnr with fee decrease request ====================")
        timer_update_check = RepeatTimer(1, checking_pnr_with_fee_decrease_request)
        timer_update_check.start()
        
        # print('Product synchronisation is starting')
        # timer_synchro = RepeatTimer(5, running_product_synhcro)
        # timer_synchro.start()

        # from AmadeusDecoder.utilities.FtpConnection import download_file
        # dest_dir = '/export/products'
        
        # send daily pnr fee update report
        daily_thread_once = RepeatTimer(3600, send_fee_update_list)
        daily_thread_once.start()
        
