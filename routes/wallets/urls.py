from django.urls import path
from Wallets.views import WalletBalanceView


urlpatterns = [
    path('wallet/balance', WalletBalanceView.as_view(), name='wallet-balance'),
]