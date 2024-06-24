from django.urls import path
from . import views

from .views import home
from .views.Dashboard import dashboard
from .views.Manage_customers import *
from .views.Manage_users import *
from .views.Account import account
from .views.Tools import *
from .views.Setting import *
from .views.Login import *
from .views.Home import *
from .views.Comment import *


urlpatterns = [
    path('', index, name = "index"),
    path('loginPage/', loginPage, name = "loginPage"),
    path('logout/', logoutUser, name = "logout"),
    path('home/', home, name = "home"),
    path('home/pnr/<int:pnr_id>/', pnr_details, name = 'pnr_details'),
    path('dashboard/', dashboard, name = "dashboard"),
    path('customers/', customers, name = "customers"),
    path('users/', users, name = "users"),
    path('register/', register, name = "register"),
    path('tools/', tools, name = "tools"),
    path('setting/', setting, name = "setting"),
    path('account/', account, name = "account"),
    path('comment/', comment, name = 'comment'),
    path('comment-list/', comment_list, name = 'comment-list'),
    path('comment-detail/<int:comment_id>', comment_detail, name = 'comment-detail'),
    path('comment-list/update-comment-state/', update_comment_state, name = "update-comment-state"),
    path('comment-detail/update-comment-state/', update_comment_state, name = "update-comment-state"),
    path('home/get-pnr-user-copying/', get_pnr_user_copying, name='get-pnr-user-copying'),
    path('home/pnr/create-customer/', create_customer, name = 'create_customer'),
    path('home/pnr/<int:pnr_id>/get-order/', get_order, name='get-order'),
    path('home/pnr_research', pnr_research, name = 'pnr_research'), 
    path('home/pnr_search_by_pnr_number', pnr_search_by_pnr_number, name = 'pnr_search_by_pnr_number'),
    path('home/reduce-fee-request', reduce_fee, name = 'reduce_fee_request'),
    path('home/fee-request-accepted/<int:request_id>/<str:amount>/<str:choice_type>/<str:token>', reduce_fee_request_accepted, name='reduce_fee_request_accepted'),
    path('home/fee-request-rejected/<int:request_id>/<str:choice_type>/<str:token>', reduce_fee_request_rejected, name='reduce_fee_request_rejected'),
    path('home/fee-request-modify/<int:request_id>/<str:choice_type>/<str:token>', reduce_fee_request_modify, name='reduce_fee_request_modify'),
    path('home/pnr/<int:pnr_id>/get-quotation/', get_quotation, name='get-quotation'),
    path('home/pnr/modify-customer/', modify_customer_info, name = 'modify_customer'),
    path('home/pnr/modify-customer-in-passenger-invoice/', modify_customer_in_passenger_invoice, name = 'modify_customer_in_passenger_invoice'),
    path('home/pnr/<int:pnr_id>/get-product/', get_product, name= 'get_product'),
    path('home/get-not-fetched-pnr/', get_pnr_not_fetched, name= 'get_pnr_not_fetched'),
    path('home/pnr/<int:pnr_id>/save_pnr_detail_modification/', save_pnr_detail_modification, name='save_pnr_detail_modification'),
    path('home/pnr/<int:pnr_id>/import_product/', import_product, name='import_product'),
    path('home/pnr/<int:pnr_id>/delete-customer/', delete_customer, name='delete_customer'),
    path('home/pnr/<int:pnr_id>/find-customer/', find_customer, name='find_customer'),
    path('home/customer/import_customer/', call_customer_import, name='import_customer'),
    path('home/product/import_product_odoo/', call_product_import, name='import_product_odoo'),
    path('home/search-customer/', search_client_by_intitule, name= 'search_client_by_intitule'),
    path('home/get-all-coutries/', get_all_countries, name= 'get_all_countries'),
    path('home/get-all-departments/', get_all_departments, name= 'get_all_departments'),
    path('home/get-all-municipalities/', get_all_municipalities, name= 'get_all_municipalities'),
    path('home/other-fee/remove/', remove_other_fee_service, name='remove_other_fee_service'),
    path('home/get-all-products/', get_all_products, name='get_all_products'),
    path('home/get-invoice-number-to-uncommand/<str:numeroPnr>', get_invoice_number, name='get_invoice_number'),
    path('home/unorder-pnr',unorder_pnr, name='unorder_pnr'),
    path('home/get-all-pnr-unordered',get_all_pnr_unordered, name='get_all_pnr_unordered'),
    path('home/unordered-pnr-research', unordered_pnr_research, name= 'unordered_pnr_research'),
    path('home/verif/ticket', verif_ticket, name= 'verif_ticket'),
    path('home/save-ticket-anomalie', save_ticket_anomalie, name= 'save_ticket_anomalie'),
    path('home/get-all-anomalies', get_all_anomalies, name='get_all_anomalies'),
    path('home/update-ticket', update_ticket, name='update_ticket'),
    path('home/get-passengers-and-segments', getPassengersAndSegmets, name= 'getPassengersAndSegmets'),
    path('home/get-passenger-and-segment-By-Id', getPassengerAndSegmentById, name='getPassengerAndSegmentById'),
    path('home/anomaly-details/<int:pnr_id>', anomaly_details, name='anomaly_details'),
    path('home/liste-commandes', liste_commandes, name='liste_commandes'),
    path('home/refuse-anomaly', refuse_anomaly, name='refuse_anomaly'),
    path('home/drop-anomaly',drop_anomaly, name='drop_anomaly'),
    path('home/update-anomaly', updateAnomaly, name='update_anomaly'),
    path('setting/email',email_setting, name='email_setting'),
    path('setting/parsing',parsing_setting, name='parsing_setting'),
    path('setting/ftp',ftp_setting, name='ftp_setting'),
    path('setting/general-update',updateGeneralSetting, name='updateGeneralSetting'),
    path('setting/saving-protocol-update',saving_protocol_update, name='saving_protocol_update'),
    path('setting/email-pnr-update',email_pnr_update,name='email_pnr_update'),
    path('setting/email-notif-sender-update',email_notif_sender_update,name='email_notif_sender_update'),
    path('setting/email-notif-update',email_notif_update,name='email_notif_update'),
    path('setting/email-fees-update',email_fees_update,name='email_fees_update'),
    path('setting/email-fee-sender-update',email_fee_sender_update, name='email_fee_sender_update'),
    path('setting/parsing-update',parsing_update,name='parsing_update'),
    path('setting/general-information-create',general_information_create,name='general_information_create'),
    path('setting/general-file-protocol-create',general_file_protocol_create,name='general_file_protocol_create'),
    path('setting/email-pnr-create',email_pnr_create,name='email_pnr_create'),
    path('setting/email-notification-recipients-create',email_notification_recipients_create,name='email_notification_recipients_create'),
    path('setting/email-notification-sender-create',email_notification_sender_create,name='email_notification_sender_create'),
    path('setting/email-fee-sender-create',email_fee_sender_create,name='email_fee_sender_create'),
    path('setting/email-fee-recipient-create',email_fee_recipient_create,name='email_fee_recipient_create'),
    path('setting/pnr-parsing-create',pnr_parsing_create,name='pnr_parsing_create'),
    path('setting/ticket-parsing-create',ticket_parsing_create,name='ticket_parsing_create'),
    path('setting/tst-parsing-create',tst_parsing_create,name='tst_parsing_create'),
    path('setting/zenith-parsing-create',zenith_parsing_create,name='zenith_parsing_create'),
    path('setting/zenith-receipt-parsing-create',zenith_receipt_parsing_create,name='zenith_receipt_parsing_create'),
    path('setting/emd-parsing-create',emd_parsing_create,name='emd_parsing_create'),
    path('setting/emd-statues-update',emd_statues_update,name='emd_statues_update'),
    path('setting/test-parsing',test_parsing,name='test_parsing'),
    path('setting/test-parsing-zenith',test_parsing_zenith,name='test_parsing_zenith'),
    path('setting/test-parsing-text',test_parsing_text,name='test_parsing_text'),
    path('home/ticket-delete',ticket_delete,name='ticket_delete'),
    path('setting/test-parsing-upload-file',test_parsing_upload_file,name='test_parsing_upload_file'),
    path('comment/reply-comment',reply_comment,name='reply_comment'),
    path('pnr/to/excel/<int:pnr_id>/',pnr_to_excel, name='pnr_to_excel'),
    path('pnr/list/to/excel',pnr_list_to_excel, name='pnr_list_to_excel'),
    path('user/details/<int:user_id>/',user_details,name='user_details'),
    path('user/archive',archive_user, name="archive_user"),
    path('user/reactive',reactive_user, name="reactive_user"),
    path('user/UpdatePassword',update_password, name='update_password'),
    path('user/updateInfo',update_info,name='update_info'),
    path('home/user-research', user_research, name= 'user_research'),
    path('home/user-filter', user_filter, name= 'user_filter'),
    path('stat/',graph_view, name='graph_view'),
    path('stat/passenger',passenger_graph_view, name='passenger_graph_view'),
    path('stat/anomaly',anomaly_graph_view, name='anomaly_graph_view'),
    path('stat/user',user_graph_view, name='user_graph_view'),
    path('comment/get-unshowed-tickets',get_unshowed_tickets, name='get_unshowed_tickets'),
    path('anomaly/add-category',add_anomaly_category,name="add_anomaly_category"),
    path('anomaly/all-canceled-ticket',get_all_canceled_ticket,name="get_all_canceled_ticket"),
    path('anomaly/canceled-ticket-detail/<int:pnr_id>',get_canceled_ticket_detail,name="get_canceled_ticket_detail"),
    path('home/canceled-ticket-research', canceled_ticket_research, name= 'canceled_ticket_research'),
    path('home/canceled-ticket-filter', canceled_ticket_filter, name= 'canceled_ticket_filter'),
    path('home/canceled-ticket-advanced-research', canceled_ticket_advanced_search, name= 'canceled_ticket_advanced_search'),
    path('home/unordered-pnr-filter', unordered_pnr_filter, name= 'unordered_pnr_filter'),
    path('home/unordered-pnr-advanced-research', unordered_pnr_advanced_search, name= 'unordered_pnr_advanced_search'),
    path('home/pnr-non-remonte',pnr_non_remonte,name='pnr_non_remonte'),
    path('home/unremounted-pnr',all_unremounted_pnr,name='all_unremounted_pnr'),
    path('home/unremounted-pnr-details/<int:unremounted_pnr_id>',unremounted_pnr_details,name='unremounted_pnr_details'),
    path('check-uninvoiced-status/', uncheck_ticket_in_passenger_invoiced, name='uncheck_ticket_in_passenger_invoiced'),
    path('anomaly/accept/unremounted-pnr',accept_unremounted_pnr, name='accept_unremounted_pnr'),
    path('anomaly/refuse/unremounted-pnr',refuse_unremounted_pnr, name='refuse_unremounted_pnr'),
    path('home/unremounted-pnr-research', unremounted_pnr_research, name= 'unremounted_pnr_research'),
    path('customer/details/<int:customer_id>',customer_details,name="customer_details"),
    path('home/unremounted-pnr-research', unremounted_pnr_research, name= 'unremounted_pnr_research'),
    path('customer/updateInfo',modify_customer,name='modify_customer'),
    
]
