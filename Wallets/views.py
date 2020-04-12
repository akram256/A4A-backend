from django.shortcuts import render
from Wallets.serializers import UserWalletBalanceSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
import json
from datetime import datetime,date
import pytz
from django.conf import settings
from Auth.models import User
from utils import services
from rest_framework import status
from decimal import Decimal
import logging
from Wallets.models import Wallet
from django.conf import settings

logger = logging.getLogger(__name__)

# Create your views here.
class WalletBalanceView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user_wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            user_wallet = Wallet.objects.create(user=request.user)
        serializer = UserWalletBalanceSerializer(user_wallet)
        response = {
                'status': '00',
                'data': serializer.data
            }
        return Response(response, status=status.HTTP_200_OK)