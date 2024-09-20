from django.db import models

class OptimisedPnrList(models.Model):
    number = models.CharField(max_length=255)
    passengers = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)
    emitter = models.CharField(max_length=255)
    agency_name = models.CharField(max_length=255)
    agency_office_code = models.CharField(max_length=255)
    agency_office_name = models.CharField(max_length=255)
    is_invoiced = models.BooleanField(db_index=True)
    date_of_creation = models.DateTimeField(db_index=True)
    is_read = models.BooleanField()
    status_value = models.IntegerField()
    state = models.IntegerField()
    client = models.CharField(max_length=255)
    pnr_comment_state = models.IntegerField()
    pnr_min_doc_state = models.DateTimeField(db_index=True)
    max_issuing_date = models.DateTimeField(db_index=True)
    
    class Meta:
        managed = False  # No migration will be created for this model
        db_table = 'optimised_pnr_list'
