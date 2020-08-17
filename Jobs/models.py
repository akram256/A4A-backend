from django.db import models
from Auth.models import User
from helpers.models import BaseAbstractModel
from decimal import Decimal
from django.core.validators import RegexValidator

# Create your models here.


class ArtistCategory(BaseAbstractModel):
    """ This is model that categorizes the jobs to be done """

    name= models.CharField(max_length=255, blank=True, null=True)
    details=models.TextField(null=True)

    def __str__(self):
        return "{}".format(self.name)



class Artist(BaseAbstractModel):
    
    """This is a model for the jobs input by the user """
    id = models.CharField(max_length=200, primary_key=True, unique=True,)
    first_name= models.CharField(max_length=255, blank=True, null=True)
    last_name= models.CharField(max_length=255, blank=True, null=True)
    stage_name=models.CharField(max_length=255, blank=True, null=True)
    manager_name= models.CharField(max_length=255, blank=-True, null=True)
    management_label= models.CharField(max_length=255, blank=-True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    manager_phone_no = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    pictures=models.ImageField(upload_to='pictures/', null=True)
    price= models.DecimalField(max_digits=12, decimal_places=2, null=True)
    category= models.ForeignKey(to='Jobs.ArtistCategory', on_delete=models.DO_NOTHING, null=True) 
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.stage_name

    @property
    def artist_category(self):
        return self.category.name