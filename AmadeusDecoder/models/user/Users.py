from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel
from django.contrib.postgres.fields import HStoreField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Office(models.Model, BaseModel):
    
    class Meta:
        db_table = 't_office'
        constraints = [
                models.UniqueConstraint(fields=['code'], name='unique_office')
            ]
        
    name = models.CharField(max_length=200, null=False)
    location = models.CharField(max_length=200, null=True)
    code = models.CharField(max_length=200, null=True)
    # Add company identifier in order to have a distinction of company owned office or not
    company = models.ForeignKey(
        "AmadeusDecoder.CompanyInfo",
        on_delete = models.CASCADE,
        related_name='company',
        null=True
    )

    def __str__(self):
        return '{}: {}'.format(self.name, self.code)
    
class OfficeSubcontractor(models.Model, BaseModel):
    
    class Meta:
        db_table = 't_office_subcontractor'
        constraints = [
                models.UniqueConstraint(fields=['code'], name='unique_office_subcontractor')
            ]
        
    name = models.CharField(max_length=200, null=False)
    location = models.CharField(max_length=200, null=True)
    code = models.CharField(max_length=200, null=True)
    subcontracting_cost = models.DecimalField(max_digits=11, decimal_places=4, default=0)
    
    def __str__(self):
        return '{}: {}'.format(self.name, self.code)
        
class Role(models.Model, BaseModel):

    class Meta:
        db_table = 't_role'

    name = models.CharField(max_length=100)
    level = models.IntegerField()

    def __str__(self) :
        return '{}'.format(self.name)

class UserManager(BaseUserManager):

    def create_user(self, email, username, password, **fields):
        if not email:
            raise ValueError("Utilisateur doit avoir un email.")
        if not username:
            raise ValueError("Utilisateur doit avoir un nom d'utilisateur.")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            **fields
        )
        fields.set_default('is_active', True) 

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password, **fields):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            **fields
        )

        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True

        user.save(using=self._db)

        return user

class User(AbstractBaseUser, BaseModel):
    
    class Meta:
        db_table = 't_user'
        
    office = models.ForeignKey(
        'AmadeusDecoder.Office',
        on_delete=models.CASCADE,
        related_name='users',
        null=True
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    email = models.EmailField(verbose_name='email', unique=True, max_length=100, default='')
    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    gds_id = models.CharField(max_length=100, null=True)
    last_login_time = models.DateTimeField(auto_now=True)

    date_joined = models.DateField(auto_now_add=True, null=True)
    last_login = models.DateField(auto_now=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'first_name']

    objects = UserManager()


    def __str__(self):
        return '{}'.format(self.username)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Activation(models.Model, BaseModel):

    class Meta:
        db_table = 't_activation'

    type = models.CharField(max_length=100)
    state = models.IntegerField()
    duration = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    



class UserCopying(models.Model):

    class Meta:
        db_table='t_user_copying'

    document = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='copied_documents')
