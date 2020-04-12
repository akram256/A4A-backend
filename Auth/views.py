import os
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from .serializers import RegistrationSerializer,RatingSerializer,ReviewSerializer, ProfileSerializer,LoginSerializer, FacebookAuthSerializer,UserSerializer,GoogleAuthSerializer,TwitterAuthSerializer,PasswordResetSerializer,PasswordResetConfirmSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, Http404
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView,RetrieveUpdateAPIView
from Auth.models import User,Profile,Reviews
from django.contrib.auth import authenticate
from rest_framework import authentication
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
import json
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.conf import settings
from decimal import Decimal
from rest_framework import generics
from utils.tasks import send_user_email
from datetime import timedelta, datetime, time, date
import secrets
import re
import requests
import jwt
from utils import services
import logging
from django.template.loader import render_to_string
from Wallets.models import Wallet
import decimal
from helpers.validators import phonelookup
from Auth.permissions import IsProvider, IsUser,IsProfileOwner
logger = logging.getLogger(__name__)



class RegistrationAPIView(generics.GenericAPIView):
    """Register new users."""
    serializer_class = RegistrationSerializer
    permission_class = (AllowAny,)

    def post(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(data=request.data)
        phone_no = request.data.get('phone_no')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        role = request.data.get('role') 
        email= str(email)
        print(email)
        email = email.lower()
        email_pattern = services.EMAIL_PATTERN
        password_pattern = services.PASSWORD_PATTERN
        url_param = get_current_site(request).domain

        if not re.match(password_pattern,password):
            return Response({'message':'Password is weak, please use atleast 1 UPPERCASE, 1 LOWERCASE, 1 SYMBOL',}, status=status.HTTP_400_BAD_REQUEST)
        
        resp, user = phonelookup(phone_no)        

        if resp != 'valid' and ((not user)):
            return Response(phonelookup.phone_response[resp], status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.info(phonelookup.phone_response[resp])
        
        if re.match(email_pattern,email):
            user = [i for i in users if i.email == email]
            if user:
                return Response({'message':'This email: {} , already belongs to a user on Twous'.format(email),}, status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.info('email looks good')
        else:
            return Response({'message':'Email: {} is not valid'.format(email),}, status=status.HTTP_400_BAD_REQUEST)
        #     return Response({'message': f"Please visit your email {email} to complete registration", 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid(raise_exception=True) and phone_no:
            user=User(email=email,phone_no=phone_no,password=password,first_name=first_name,last_name=last_name,role=role, is_active=True)
            user.set_password(password)
            user.save()
            bonus_balance = settings.BONUS_VALUE
            Wallet.objects.create(user=user,bonus_balance=bonus_balance)
            # Profile.objects.create(user=user,first_name=first_name,last_name=last_name, location=location, profile_pic=profile_pic, avg_rating=avg_rating)
            # cache_time = settings.EMAIL_CACHE_TIME 
            email_verification_url=reverse('Auth:verify')
            full_url= request.build_absolute_uri(email_verification_url + '?token='+user.token)
            email_data = {'subject':'Welcome To Twous','email_from':settings.EMAIL_FROM}
            content = render_to_string('activate_account.html',{'token':'{}'.format(full_url),} )
            send_user_email.delay(email,content,**email_data)
            details = {'field':'auth','phone_no':phone_no,'password':password,'email':email,role:'role'}
            # cache_data = details
            # cache.set(cache_key, cache_data, cache_time)

            logger.info(f'user {phone_no} has been registered')
            return Response({'message': "Registration successful", 'status': '00','token':user.token}, status=status.HTTP_200_OK)
        return Response({'message': "Invalid credentials", 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)


def valid_number(phone_no,users,usecase=0):
    phone_pattern = services.PHONE_PATTERN
    if re.match(phone_pattern,phone_no) or (phone_no.startswith('0') and len(phone_no)==11):
        
        if not usecase:
            user = [i for i in users if i.phone_no[-10:] == phone_no[-10:]]
            if user:
                return 1,({'message':'This phone number: {} , already belongs to a user on Twous'.format(phone_no),},status.HTTP_400_BAD_REQUEST)
            else:
                return 0,'number looks good'
        else:
            user = [i for i in users if i.phone_no == phone_no]
            if not user:
                return 1,({'error':'This phone number: {} , does not belong to any user on Twous'.format(phone_no),}, status.HTTP_400_BAD_REQUEST)
            else:
                return 0,'phone number exists in the db'
    else:
        if not usecase:
            return 1,({'message':'Phone number: {} is not valid'.format(phone_no),}, status.HTTP_400_BAD_REQUEST)
        else:
            return 1,({'error':'Phone number: {} is not valid'.format(phone_no),}, status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        phone_no = request.data.get('phone_no')
        password = request.data.get('password')
        role = request.data.get('role')

        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=phone_no, password=password, role=role) 
            if user is None:
                users = User.objects.all()
                validity,resp_message = valid_number(phone_no,users,usecase=1)
                if validity:
                    logger.info(resp_message)
                    return Response(resp_message[0],status=resp_message[1])
                else:
                    #logger.info(User.objects.get(phone_no=phone_no).check_password(password))
                    if User.objects.get(phone_no=phone_no).is_active:
                        return Response({'error': "Incorrect Password"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'error': "Your account has not been activated, Please check your mail"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if not user.is_active:
                    raise serializers.ValidationError(
                        'This user has been deactivated.'
                    )
                else:
                    logger.info('login successful for {}'.format(phone_no))

            resp ={
                    'status':'00',
                    'token':user.token,

                    'message':'user loggedin successfully'
                }
            return Response(resp, status=status.HTTP_200_OK)
                
        return Response({'message': "Invalid credentials", 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)




class VerifyAccount(APIView):
    permission_classes = (AllowAny, )
    def get(self,request,format=None):
        token = request.GET['token']
        payload = jwt.decode(token, settings.SECRET_KEY, 'utf-8')
        id = payload['id']
        user = User.objects.filter(id=id)
        user.update(is_active=True)
        return Response(
            {
                'message': 'Account successfully verified,'
                'your free to  now login'
            },
            status=status.HTTP_200_OK)

class FacebookSocialAuthView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FacebookAuthSerializer

    def post(self, request):
        serializer_class = FacebookAuthSerializer
        user = request.data.get('user', {})
        serializer = serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GoogleSocialAuthView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GoogleAuthSerializer

    def post(self, request):
        serializer_class = GoogleAuthSerializer
        user = request.data.get('user', {})
        serializer = serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TwitterSocialAuthView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TwitterAuthSerializer

    def post(self, request):
        serializer_class = TwitterAuthSerializer
        user = request.data.get('user', {})
        serializer = serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ResetPasswordRequest(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer
    def get_object(self,phone_no):
        try:
            return User.objects.get(phone_no=phone_no)
        except:
            return None
    def post(self, request,):
        unregistered_email = request.data.get('email')
        request.data.pop('email',None)
        serializer = self.serializer_class(data=request.data)
        phone_no = request.data.get('phone_no')
        user = self.get_object(phone_no)
        
        if not user:
            return Response({'message':'This phone_no: {} , does not belong to any user on Twous'.format(phone_no),}, status=status.HTTP_400_BAD_REQUEST)
        email = user.email
        if (not email) and (not unregistered_email):
            return Response({'message':'This user does not have an email','status':'99'},status=status.HTTP_200_OK)
        elif unregistered_email:
            user.email = unregistered_email
            user.save()
            email = unregistered_email
        if serializer.is_valid() and user:
            
            template_data={'reset_link':settings.RESET_PASSWORD}    
            email_data = {'subject':'Password Reset','email_from':services.EMAIL_FROM}
            content = render_to_string('reset_password.html', template_data)
            send_user_email.delay(email,content,**email_data)
            resp = {
                'status': '00',
                'email':email,
                'message':'Please check your email to reset password'
            }
            return Response(resp, status=status.HTTP_200_OK)
        
        return Response({'message':'wrong field query', }, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirm(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer
    def get_object(self,email):
        try:
            return User.objects.get(email=email)
        except:
            return None

    def post(self, request,):
        serializer = self.serializer_class(data=request.data)
        password1 = request.data.get('password')
        password2 = request.data.get('confirm_password')
        email = request.data.get('email')
        user = self.get_object(email)
        logger.info(email)
        logger.info(user)
        logger.info('after user')
        if not user:
            return Response({'message':'This email: {} does not belong to any user on Twous'.format(email),}, status=status.HTTP_400_BAD_REQUEST)
        pattern = services.PASSWORD_PATTERN
        if serializer.is_valid():
            if password1 != password2:
                return Response({'message':'Password mismatch', 'status': '00'})
            if re.match(pattern,password1):
                user.set_password(password1)
                user.save()
                logger.info('user new password is {}'.format(password1))
                return Response({'message':'Password ok, password reset', 'status': '00'})
            else:
                Response({'message':'bad password',}, status=status.HTTP_400_BAD_REQUEST)

        
        return Response({'message':'wrong field query',}, status=status.HTTP_400_BAD_REQUEST)


class ListProfileView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class RetrieveUpdateProviderProfileView(RetrieveUpdateDestroyAPIView):
    """
    This class allows a Provider to view a profile
    and only its owner to edit it
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field='id'
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), id=self.kwargs.get('id'))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message':'Profile has been successfully updated'},serializer.data)
        # partial = kwargs.pop('partial', False)
        # instance = self.get_object()

        # users= User.objects.all()
        # rdata = request.data
        # phone_no = rdata['user.phone_no']
        # email = request.data['user']['email']
        # tempdata = {'user':dict(),'location':0,"avg_rating":"",'profile_pic':""}
        # for i in rdata:
        #     l=i.split('.')[-1]
        #     if l in ["location","avg_rating","profile_pic"]:
        #         tempdata[l]=rdata[i]
        #     else:
        #         tempdata['user'].setdefault(l,rdata[i])
        # phone_no = tempdata['user']['phone_no']
        # # print(phone_no)
        # # print(request.user.phone_no)
        # email = rdata['user.email']
        # email=email.lower()
        # phone_pattern = services.number_rule
        # email_pattern = services.EMAIL_PATTERN
        # if phone_no and (phone_no != request.user.phone_no):
        #     resp, user = phonelookup(phone_no)        
        #     if resp != 'valid' and (not user):
        #         return Response(phonelookup.phone_response[resp], status=status.HTTP_400_BAD_REQUEST)
        #     else:
        #         # tempdata['user']['phone_no'] = phone_no
        #         phone_no = rdata['user.phone_no']
        #         logger.info(phonelookup.phone_response[resp])
        # else:
        #     tempdata['user']['phone_no']= ''
        #     # rdata['user.phone_no']=''
        #     logger.info('phone_no didnt change so its reformatted')
        # # rdata['user.phone_no']=''
        # tempdata['user']['phone_no']= ''
        # print(tempdata)
      
        # tempdata = {'user':{'phone_no':1111,'first_name':'hjjhk','last_name':'khkl'}}
        # serializer = self.get_serializer(instance, data=request.data,
        #                                  partial=partial)
        # print(serializer)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        # return Response({'message':'Profile has been successfully updated',
        #                  "data":serializer.data
        #                 },status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Profile  has been successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)


class ReviewView(ListCreateAPIView):
    permission_classes=(IsUser,)
    serializer_class= ReviewSerializer

    def get_queryset(self, **kwargs):
        reviewer = get_object_or_404(Profile, pk=self.kwargs.get('id'))
        print(reviewer)
        queryset = Reviews.objects.filter(
            profile=reviewer)
        if queryset:
            return queryset
        else:
            raise Http404

    def create(self, request, *args, **kwargs):
        """ allows users to add reviews to a provider """

        try:
            userprofile=Profile.objects.get(
                pk=kwargs.get('id'))
            print(Profile,'thththhtht')
        except Profile.DoesNotExist:
            return Response({
                "errors": "Provider not found"
            }, status=status.HTTP_404_NOT_FOUND)

        payload = request.data
        # payload['user'] = userprofile
        print(payload)
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save(profile=userprofile)
        response = {
            "message": "Your review has been added"
        }
        return Response(response, status.HTTP_201_CREATED)

class ListProvidersView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer
   

    def get_queryset(self):
        user = Profile.objects.filter(user__role="PROVIDER")
        return user

    def get(self, request):
        data=self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response({'message':'Provider has been successfully retrieved',
                         "data":serializer.data
                        },status=status.HTTP_200_OK)


class RatingsView(ListCreateAPIView):
    """
    implements methods to handle rating providers
    """
    serializer_class = RatingSerializer
    permission_classes = (IsUser,)

    def post(self, request, id=None):
        """
        method to post a rating for an article
        """
        data = self.serializer_class.update_data(
            request.data.get("provider", {}), id, request.user)

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
