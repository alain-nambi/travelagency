from django.urls import path
from . import views

from .views import home
from .views.Dashboard import dashboard
from .views.Manage_customers import customers, create_customer, modify_customer_info, modify_customer_in_passenger_invoice, delete_customer
from .views.Manage_users import users, register
from .views.Account import account
from .views.Tools import tools, call_customer_import, call_product_import
from .views.Setting import setting
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
    path('home/get-all-coutries/', get_all_countries, name= 'get_all_countries')
]
