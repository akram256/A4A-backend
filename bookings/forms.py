from django import forms
from .models import Bookings
class BookingsCreateForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = ['user', 'venue', 'time_of_performance', 'conditions', 'location']