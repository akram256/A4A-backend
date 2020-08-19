from django.contrib import admin
from .models import Bookings, Events


admin.site.register(Events)

@admin.register(Bookings)
class BookAdmin(admin.ModelAdmin):
    list_display = ['user', 'venue', 'time_of_performance', 'conditions', 'location',
    'paid','created', 'updated']
    list_filter = ['paid', 'created', 'updated']
   