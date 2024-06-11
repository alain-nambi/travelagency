
from django.db import models
from datetime import datetime
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.pnr.Passenger import Passenger
from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.user.Users import User
from django.contrib.postgres.fields import HStoreField

class Comment(models.Model):
    
    class Meta:
        db_table = 't_comment'

    pnr_id = models.ForeignKey(Pnr, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=800)
    state = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now=True)


class Response(models.Model):

    class Meta:
        db_table = 't_response'

    pnr_id = models.ForeignKey(Pnr, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.TextField(max_length=800)
    creation_date = models.DateTimeField(auto_now=True)

class NotFetched(models.Model):

    class Meta:
        db_table = 't_pnr_not_fetched'

    pnr_number = models.CharField(max_length=100, null=False)
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now=True)
    
class CategorieAnomalie(models.Model):
    class Meta:
        db_table = 't_categorie_anomalie'

    name = models.CharField(max_length=100, null=False)

    def __str__(self) :
        return '{}'.format(self.name)
    
class Anomalie(models.Model):
    
    class Meta:
        db_table = 't_anomalie'
        ordering = ['-creation_date']
        
    pnr = models.ForeignKey(Pnr, on_delete=models.CASCADE)
    categorie = models.CharField(max_length=250)
    infos = HStoreField(null=False)
    creation_date = models.DateTimeField(null=False)
    issuing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issuing_user', null=True)
    status = models.IntegerField(default=0)
    response_date = models.DateTimeField(null=True)

