from django.contrib import admin
from .models import User,Profile
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
import csv
from datetime import datetime
# from rangefilter.filter import DateRangeFilter

# admin.site.register(User)
admin.site.register(Profile)
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        """ Refer to comment on line 34"""
        # field_names = [field.name for field in meta.fields]
        field_names = [ 'Phone Number', 'Email']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=lottoly-user-{}.csv'.format(datetime.now())
        writer = csv.writer(response)

        writer.writerow(field_names)
        """ Commented this out to handle the logic better for making this export feature more generic"""
        # for obj in queryset:
        #     row = writer.writerow([getattr(obj, field) for field in field_names])

        users = User.objects.all().values_list( 'phone_no', 'email',)
        for user in users:
            writer.writerow(user)

        return response

    export_as_csv.short_description = "Export as Csv"

class CustomUserAdmin(UserAdmin, ExportCsvMixin):
    list_display = ('id',  'email', 'phone_no','role',
                    'created_at')
    list_filter = ('created_at','is_active', 'is_staff')
    search_fields = ('phone_no',)
    ordering = ('created_at',)
    fieldsets = (
        ('Personal info', {'fields': ('phone_no','email','role',)}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser')}),
    )
    actions = ["export_as_csv"]

admin.site.register(User, CustomUserAdmin)
admin.site.site_header = "Twous Admin Portal"
admin.site.site_title = "Twous Admin Portal"
admin.site.index_title = "Welcome to Twous Admin Portal"
