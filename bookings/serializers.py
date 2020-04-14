from rest_framework import serializers
from bookings.models import Bookings,Events
from Auth.models import User


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ('user', 'venue', 'time_of_performance', 'conditions', 'location',)

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model= Events
        fields=('artist','venue_of_performance','date_of_event')