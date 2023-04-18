'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel
from django.contrib.postgres.fields.array import ArrayField

class FlightType(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_flighttype'
    
    type = models.CharField(max_length=50, null=False)

class FlightClass(models.Model, BaseModel):
    
    class Meta:
        db_table = 't_flightclass'
        
    flightclass = models.CharField(max_length=50, null=False)
    
class ServiceFeesMercure(models.Model, BaseModel):
    
    class Meta:
        db_table = 't_servicefees_flight_class_based'
        
    flighttype = models.ForeignKey(
        "AmadeusDecoder.FlightType",
        on_delete = models.CASCADE
    )
    flightclassid = models.ForeignKey(
        "AmadeusDecoder.FlightClass",
        on_delete = models.CASCADE
    )
    price = models.DecimalField(max_digits=11, decimal_places=4, default=0)

class ServiceFeesIssoufali(models.Model, BaseModel):
    
    class Meta:
        db_table = 't_servicefees_amount_based'
        constraints = [
            models.UniqueConstraint(fields=['min_interval', 'max_interval'], name="unique_service_fees")
        ]
        
    min_interval = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    max_interval = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    fee = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    last_update = models.DateTimeField(null=True)
    last_update_user = models.ForeignKey(
        'AmadeusDecoder.User',
        on_delete=models.CASCADE,
        related_name='updated_fees',
        null=True
    )
    from django.utils import timezone
    effective_date = models.DateTimeField(default=timezone.now)
    
class ClassSign(models.Model, BaseModel):
    
    class Meta:
        db_table = 't_classsign'
        
    type = models.CharField(max_length=50, null=False)
    gdsprovider = models.CharField(max_length=100, null=False)
    sign = ArrayField(
            models.CharField(max_length=10, null=True),
            size=8
        )

class ServiceFeesPrime(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_service_fees_prime'
        constraints = [
            models.UniqueConstraint(fields=['company', 'type'], name="unique_service_fees_prime")
        ]
    
    company = models.ForeignKey(
        "AmadeusDecoder.CompanyInfo",
        on_delete=models.CASCADE,
        related_name='service_fees_prime',
        null=True
    )
    
    type = models.IntegerField(default=0) # 0: regional, 1: international/metropole
    fee_value = models.DecimalField(max_digits=11, decimal_places=4, default=0)

class RegionalFlight(models.Model, BaseModel):
    
    class Meta:
        db_table = 't_company_regional_flight'
        constraints = [
            models.UniqueConstraint(fields=['company', 'country'], name="unique_region_company")
        ]
    
    company = models.ForeignKey(
        "AmadeusDecoder.CompanyInfo",
        on_delete=models.CASCADE,
        related_name='regional_flights'
    )
    
    country = models.ForeignKey(
        "AmadeusDecoder.Country",
        on_delete=models.CASCADE,
        related_name='company_as_regional'
    )

class ServiceFeesEMD(models.Model, BaseModel):
    '''
    classdocs
    '''
    
    class Meta:
        db_table = 't_service_fees_emd'
        constraints = [
            models.UniqueConstraint(fields=['company'], name="unique_service_fees_emd")
        ]
    
    company = models.ForeignKey(
        "AmadeusDecoder.CompanyInfo",
        on_delete=models.CASCADE,
        related_name='service_fees_emd',
        null=True
    )
    
    fee_value = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    