'''
Created on 27 Feb 2023

@author: Famenontsoa
'''
import datetime
import traceback
import os
import decimal

from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel
from django.contrib.postgres.fields import HStoreField
from AmadeusDecoder.utilities.DBConnect import DBConnect

class History(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_history'
        
    pnr = models.ForeignKey(
        'AmadeusDecoder.Pnr',
        on_delete=models.SET_NULL,
        related_name='history',
        null=True
    )
    
    pnr_number = models.CharField(max_length=100)
    
    user = models.ForeignKey(
        'AmadeusDecoder.User',
        on_delete=models.SET_NULL,
        related_name='history',
        null=True
    )
    
    username = models.CharField(max_length=100)
    
    # modification type
    # pnr, ticket, fee, flight, other_fee, ...
    modification_type = models.CharField(max_length=100)
    
    # the modification
    # For fee: initial_cost: ?, new_cost: ?, target_object: "parent ticket number" or "parent other fee designation"
    modification = HStoreField()
    
    modification_date = models.DateTimeField()
    
    def __str__(self):
        return self.modification_type + ' ' + self.modification_date
    
    # history for any modification on fees
    def fee_history(self, fee, user, initial_cost, new_cost, initial_total):
        connection = None
        c = None
        try:
            initial_cost = decimal.Decimal(initial_cost)
            new_cost = decimal.Decimal(new_cost)
            if initial_cost != new_cost:
                # Plpgsql parameters
                pnr_id = fee.pnr.id
                fee_id = fee.id
                user_id = user.id
                
                connection = DBConnect.db_connect()
                c = connection.cursor()
                c.execute("BEGIN")
                c.callproc("f_create_fee_history", (pnr_id, user_id, fee_id, initial_cost, new_cost, initial_total))
                c.execute("COMMIT")
        except:
            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                error_file.write('Fee history insertion error.')
                traceback.print_exc(file=error_file)
                error_file.write('\n')
        finally:
            if connection is not None:
                connection.close()
            if c is not None:
                c.close()
    