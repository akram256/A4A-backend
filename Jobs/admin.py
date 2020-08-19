from django.contrib import admin
from .models import ArtistCategory, Artist

# Register your models here.

admin.site.register(ArtistCategory)

@admin.register(Artist)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'stage_name', 'manager_name',
                    'management_label', 'manager_phone_no', 'pictures', 'price',
                    'category', 'is_active']
   