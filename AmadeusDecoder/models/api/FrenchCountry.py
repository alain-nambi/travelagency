from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class Department(models.Model, BaseModel):
    class Meta:
        db_table = "t_departments"
    
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    code_region = models.IntegerField()
    
class Municipality(models.Model, BaseModel):
    class Meta:
        db_table = "t_municipalities"
    
    nom = models.CharField(max_length=255)
    code_departement = models.CharField(max_length=255)
    codes_postaux = models.CharField(max_length=255)