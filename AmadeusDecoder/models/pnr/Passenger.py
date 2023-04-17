'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel
from AmadeusDecoder.models.invoice.Ticket import Ticket

class Passenger(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_passengers'
        
    name = models.CharField(max_length=200, null=True)
    surname = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=20, null=True)
    birthdate = models.DateField(null=True)
    passeport = models.CharField(max_length=200, null=True)
    types = models.CharField(max_length=200, null=True) # For EWA 
    order = models.CharField(max_length=200, null=True) # P1 ou P2 ou .....
    
    # get passenger by pnr and pnr passenger
    def get_passenger_by_pnr_passenger(self, pnr):
        passenger = Passenger.objects.filter(name=self.name, surname=self.surname, designation=self.designation, passenger__pnr__id=pnr.id).first()
        return passenger
    
    # compare current PNR's passengers with newly parsed passengers and delete those who doesn't appear on new PNR
    def compare_and_delete(self, pnr, new_passenger_list):
        current_passenger_list = Passenger.objects.filter(passenger__pnr=pnr).all()
        for current_passenger in current_passenger_list:
            tester = False
            for new_passenger in new_passenger_list:
                if current_passenger.name == new_passenger.name and \
                        current_passenger.surname == new_passenger.surname and \
                        current_passenger.designation == new_passenger.designation:
                    tester = True
            if not tester:
                current_passenger.delete()
    
    # update ticket passenger
    def update_ticket_passenger(self, pnr):
        temp_ticket = Ticket.objects.filter(pnr=pnr, related_passenger_order=self.order).first()
        if temp_ticket is not None:
            temp_ticket.passenger = self
            temp_ticket.save()
        
    def __str__(self):
        displayed_name = ''
        if self.name is not None:
            displayed_name  += self.name
        if self.surname is not None:
            displayed_name += ' ' + self.surname
        if self.designation is not None:
            displayed_name += ' ' + self.designation
        return displayed_name