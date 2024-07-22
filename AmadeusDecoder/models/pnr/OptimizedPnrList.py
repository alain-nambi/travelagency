from django.db import models

class OptimisedPnrList(models.Model):
    number = models.CharField(max_length=255)
    passengers = models.CharField(max_length=255)
    date_of_creation = models.DateField()
    status = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)
    emitter = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    is_invoiced = models.BooleanField()
    is_read = models.BooleanField()
    status_value = models.IntegerField()

    class Meta:
        managed = False  # No migration will be created for this model
        db_table = 'optimised_pnr_list'
