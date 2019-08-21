from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    generics,
    status,
)
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
            "text_body":"authentication/templates/activate_account.html",
            "html_body":"authentication/templates/activate_account.txt",
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

       
        

