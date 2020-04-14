from django.db import models
from Auth.models import User
from helpers.models import BaseAbstractModel
from decimal import Decimal

# Create your models here.


class ArtistCategory(BaseAbstractModel):
    """ This is model that categorizes the jobs to be done """

    name= models.CharField(max_length=255, blank=True, null=True)
    details=models.TextField(null=True)models.ForeignKey

    def __str__(self):
        return "{}".format(self.name)



class Artist(BaseAbstractModel):
    
    """This is a model for the jobs input by the user """
    id = models.CharField(max_length=200, primary_key=True, unique=True,)
    first_name= models.CharField(max_length=255, blank=True, null=True)
    last_name= models.CharField(max_length=255, blank=True, null=True)
    stage_name=models.CharField(max_length=255, blank=True, null=True)
    pictures=models.ImageField(upload_to='pictures/', null=True)
    price= models.DecimalField(max_digits=12, decimal_places=2, null=True)
    category= models.ForeignKey(to='Jobs.ArtistCategory', on_delete=models.DO_NOTHING, null=True) 
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.stage_name

    @property
    def artist_category(self):
        return self.category.name