from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    generics,
    status,
)
from rest_framework.settings import settings
import jwt
import os
from authentication.models import User
from rest_framework.permissions import AllowAny
from authentication.serializer import RegistrationSerializer
from authentication.renderers import UserJSONRenderer
from authentication.helpers.authorization_helpers import generate_validation_url
from authentication.helpers.tasks import send_email_notification

# Create your views here.
class RegistrationView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer
    renderer_classes= (UserJSONRenderer, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        message = [
            request, user_data[
                "email"
            ]
        ]
        url = generate_validation_url(message)

        payload ={
            "subject":"Welcome to A4A events, Please verify your account",
            "reciepent" :[user_data["email"]],
            "text_body":"activate_account.html",
            "html_body":"activate_account.txt",
            "context":{
                'username': user_data['username'],
                'url':url
            }

        }
        send_email_notification.delay(payload)
        response ={
            "data":{
                "user":dict (user_data),
                "message":"Account successfully created, Please check your mail box to verify this account",
            }
        }
        return Response(response, status= status.HTTP_201_CREATED)

class EmailVerificationView(APIView):

    def get(self, request):
        token, user_id = request.GET.get("token").split("~")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.exceptions.DecodeError:
            return self.sendResponse("Verification link is Invalid")
        except jwt.ExpiredSignatureError:
            url = generate_validation_url([request], user_id=user_id)
            user = User.objects.filter(id=user_id).first()
            payload = {
                "subject": "A4A events , Verify your Account",
                "recipient": [user.email],
                "text_body": "activate_account.txt",
                "html_body": "activate_account.html",
                "context": {
                    'username': user.first_name,
                    'url': url
                }
            }
            send_email_notification.delay(payload)

            message = "verification link is expired, we have " \
                      "sent you a new one."
            return self.sendResponse(message, status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=payload.get("email")).first()
        if user.is_verified:
            return self.sendResponse("Account is already activated")

        user.is_verified = True
        user.save()
        return  self.sendResponse("Email has been verified", status.HTTP_200_OK)

    def sendResponse(self, message, status=status.HTTP_200_OK):
        return Response({
            "message": message
        }, status)

       
        

