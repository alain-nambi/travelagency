from django.db import models
from AmadeusDecoder.models.user.Users import User

class Notification(models.Model):

    class Meta:
        db_table = 't_notification'

    message = models.CharField(max_length=300)
    document_number = models.CharField(max_length=100, unique=True)
    document_parent = models.ForeignKey('self', to_field="document_number", null=True, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=False)
    creation_date = models.DateTimeField(auto_now=True)