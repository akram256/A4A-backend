from django.db import models
from Auth.models import User
from helpers.models import BaseAbstractModel
from decimal import Decimal


class Wallet(BaseAbstractModel):
    """This is model for  wallets for Providers and Users """

    user = models.OneToOneField(to='Auth.User', on_delete=models.CASCADE)
    last_credited_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, default=Decimal('0.00'))
    bonus_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, default=Decimal('0.00'))

    def __str__(self):
        return "{}".format(self.user)
 
    def is_balance_sufficient(self, amount):
        """This is a  function to check whether is enough balance on the wallet"""

        if self.balance > Decimal(amount) or self.balance == Decimal(amount):
            return True
        return False

    def allow_bonus_and_balance_aggregation(self, amount):
        if self.balance == Decimal('0.00'):
            return False
        return True

class WalletTranscationHistory(BaseAbstractModel):
    """This is a model for web transaction on the web"""

    user = models.ForeignKey(to='Auth.User', on_delete=models.DO_NOTHING, null=True)
    transaction = models.CharField(max_length=255, blank=False, null=False)
    reference = models.CharField(max_length=255, blank=False, null=False, default=0)
    description = models.CharField(max_length=20, null=True)

    def __str__(self):
        return "{}".format(self.reference)
