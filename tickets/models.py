import uuid
from django.db import models
from helpers.models import BaseAbstractModel
from decimal import Decimal

# Create your models here.

class Tickets(BaseAbstractModel):
    """Model for Tickets"""

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event=models.CharField(max_length=255, blank=True, null=True)
    price= models.DecimalField(max_digits=12, decimal_places=2, null=True)
    venue=models.CharField(max_length=255, blank=True, null=True)
    time_of_event=models.DateTimeField(null=True)
    no_of_tickets=models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.event
