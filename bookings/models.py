from django.db import models
from Auth.models import User
from helpers.models import BaseAbstractModel
from decimal import Decimal
from Jobs.models import Artist
# Create your models here.

class Bookings(BaseAbstractModel):
    """models for artist's bookings"""
    user=models.ForeignKey(to='Auth.User', on_delete=models.CASCADE)
    venue=models.CharField(max_length=255, blank=True, null=True)
    time_of_performance=models.DateTimeField(null=True)
    conditions=models.TextField(null=True)
    location=models.CharField(max_length=255, blank=True, null=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)

class Events(BaseAbstractModel):
    """model for events"""
    artist=models.ForeignKey(to="Jobs.Artist", on_delete=models.CASCADE)
    venue_of_performance=models.CharField(max_length=255, blank=True, null=True)
    date_of_event=models.DateTimeField(null=True)




