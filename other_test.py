'''
Created on Jul 20, 2023

@author: Famenontsoa
'''
import django
import os
# from AmadeusDecoder.utilities.SendMail import Sending

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'DjangoTravelAgency.settings'
)
django.setup()

from AmadeusDecoder.utilities.ServiceFeesDecreaseRequest import ServiceFeesDecreaseRequest

from AmadeusDecoder.models.invoice.Fee import ReducePnrFeeRequest
from AmadeusDecoder.models.pnr.Pnr import Pnr
from datetime import datetime


if __name__ == '__main__':
    
    '''
        !!!! Be careful bellow lines will send emails !!!!
    '''
    # try:
    #     targeted_request_list = ReducePnrFeeRequest.objects.filter(system_creation_date__date=datetime(2023, 7, 19, 0, 0, 0, 0).date()).all()
    #     for request in targeted_request_list:
    #         subject, message = ServiceFeesDecreaseRequest().inquiry_formatting('one', request, request.fee.id, request.pnr.id, request.origin_amount, request.amount, request.motif);
    #         # print(subject, message)
    #         Sending.send_email_request(
    #             'feerequest.issoufali.pnr@gmail.com',
    #             ['superviseur@agences-issoufali.com','pp@phidia.onmicrosoft.com','mihaja@phidia.onmicrosoft.com','tahina@phidia.onmicrosoft.com'],
    #             subject,
    #             message
    #         )
    # except Exception as e:
    #     raise e
    
    '''
        !!!!! Bellow lines will find and update fee according to fee request !!!!!!!
    '''
    # try:
    #     targeted_request_list = ReducePnrFeeRequest.objects.filter(system_creation_date__date__gte=datetime(2023, 7, 26, 0, 0, 0, 0).date(), status=0).all()
    #     for request in targeted_request_list:
    #         if request.pnr.number not in ['00DB0O', '00DIIH', 'VXX8ZL']:
    #             temp_fee = request.fee
    #             temp_fee.cost = request.amount
    #             temp_fee.total = request.amount
    #             temp_fee.newest_cost = request.amount
    #             temp_fee.old_cost = request.amount
    #             temp_fee.save()
    #
    #             request.status = 1
    #             request.save()
    #             print(request.pnr.number, ' Done')
    # except Exception as e:
    #     raise e
    
    # Pnr.objects.filter(number='N9VRXD').first().delete()
    # n9vrxd
    
    