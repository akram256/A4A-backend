from django.contrib import admin
from .models import Wallet
from rangefilter.filter import DateRangeFilter

# Register your models here.


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user','balance','bonus_balance','created_at',)
