from rest_framework import serializers
from .models import Wallet


class UserWalletBalanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Wallet
        fields = ('balance', 'bonus_balance','user', 'last_credited_amount')