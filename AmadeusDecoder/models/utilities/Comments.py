
from django.db import models
from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.user.Users import User

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