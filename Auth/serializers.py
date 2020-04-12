from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from Auth.models import User,Profile,Reviews,Rating
from helpers.validators import validate_phone_number
from helpers.socialauth.socialvalidators import GoogleAuthHandler,TwitterAuthHandler, FacebookAuthHandler
from helpers.socialauth.register import register_user
import logging
import re
logger = logging.getLogger(__name__)


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer registration requests and create a new user."""

    role = serializers.ChoiceField(
        choices=[('PROVIDER', 'Provider'), ('USER', 'User')])

    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        error_messages={
            "min_length": "Password should be at least {min_length} characters"
        }
    )
    confirmed_password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        error_messages={
            "min_length": "Password should be at least {min_length} characters"
        }
    )

    class Meta:
        model = User
        fields = ["email", "phone_no", "first_name", "last_name",
                  "password", "confirmed_password", "role",]

    def validate(self, data):
        """Validate data before it gets saved."""

        confirmed_password = data.get("confirmed_password")
        try:
            validate_password(data["password"])
        except ValidationError as identifier:
            raise serializers.ValidationError({
                "password": str(identifier).replace(
                    "["", "").replace(""]", "")})

        if not self.do_passwords_match(data["password"], confirmed_password):
            raise serializers.ValidationError({
                "passwords": ("Passwords do not match")
            })

        return data

    def create(self, validated_data):
        """Create a user."""
        del validated_data["confirmed_password"]
        return User.objects.create_user(**validated_data)

    def do_passwords_match(self, password1, password2):
        """Check if passwords match."""
        return password1 == password2



class LoginSerializer(serializers.Serializer):
    phone_no = serializers.CharField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    # is_viewed_gameid=serializers.CharField(max_length=255, allow_blank=True,read_only=False)
    # is_verified_token=serializers.CharField(max_length=255,allow_blank=True, read_only=False)

    def validate_phone_no(self, value):
        if not value:
            raise serializers.ValidationError(
                'An phone_no is required to log in.'
            )
        return value 
    def validate_password(self, value):
        if value is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        return value

class FacebookAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):

        user_data = FacebookAuthHandler.validate(auth_token)
        print(user_data)
        try:
            user_data['email']
        except Exception:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        email = user_data['email']
        name = user_data['name']
        
        return email, name
    


class TwitterAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):

        user_info = TwitterAuthHandler.validate(auth_token)
        try:
            user_info['email']
        except Exception:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        email = user_info['email']
        name = user_info['name']

        return register_user(email=email, name=name)


class GoogleAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):

        user_data = GoogleAuthHandler.validate(auth_token)
        print(user_data)
        try:
            user_data['email']
        except Exception:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        email = user_data['email']
        name = user_data['name']
        picture=user_data['picture']

        return name , email, picture

class PasswordResetSerializer(serializers.Serializer):
    phone_no = serializers.CharField(max_length=255,write_only=True)

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128,write_only=True)
    confirm_password = serializers.CharField(max_length=128,write_only=True)
    email = serializers.CharField(max_length=255,write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','phone_no','role',]
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'phone_no':{
                'required': False,'allow_blank':True,'allow_null':True, "read_only":True
            }
        }

# # class UserProfileSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Profile
# #         fields = ['location',"avg_rating",'profile_pic']

# def swap(value,new):
#     if value :
#         return value
#     else:
#         return new




# class ProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     # profile=UserProfileSerializer()
#     def update(self, instance, validated_data):
#         validated_data=validated_data['user']
#         logger.info(instance.user.phone_no)
#         logger.info(instance.user.email)
#         logger.info(validated_data)
#         instance.user.email = swap(validated_data.get('email'), instance.user.email)
#         instance.user.first_name = swap(validated_data.get('first_name'), instance.user.first_name)
#         instance.user.last_name = swap(validated_data.get('last_name'), instance.user.last_name)
#         instance.user.role = swap(validated_data.get('role'), instance.user.role)
#         instance.location = swap(validated_data.get('location'), instance.location)
#         instance.avg_rating = swap(validated_data.get('avg_rating'), instance.avg_rating)
#         instance.profile_pic = swap(validated_data.get('profile_pic'), instance.profile_pic)
#         phone_no = swap(validated_data.get('phone_no'), instance.user.phone_no)
#         logger.info(phone_no+' xxxxx')
#         instance.user.phone_no = phone_no if phone_no.startswith('0') else phone_no if re.match('\+?234',phone_no) else '0'+phone_no
#         logger.info(instance.user.phone_no)
#         logger.info(instance.user.email)
#         # instance.user.save()
#         instance.save()
#         return instance
#     class Meta:
#         model = Profile
#         fields = ['user', 'location','profile_pic','avg_rating']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields=('reviews','created_at',)

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.first_name')
    reviews=ReviewSerializer(many=True)

    class Meta:
        fields = ('id','user','phone_no','first_name','last_name','email', 'average_rating',
            'location','details', 'profile_pic','Cost','Deals','reviews',)
        model = Profile
        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'id': {
                'read_only': True
            },
        }

class RatingSerializer(serializers.ModelSerializer):
    """
    class holding logic for article rating
    """
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    profile = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all())
    score = serializers.DecimalField(required=True, max_digits=5,
                                     decimal_places=2)

    @staticmethod
    def update_data(data, id, user: User):
        """
        method to update the provider with a rating
        """
        try:
            profile = Profile.objects.get(id__exact=id)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Provider is not found.")

        score = data.get("score", 0)
        if score > 5 or score < 0:
            raise serializers.ValidationError({
                "error": ["Score value must not go "
                          "below `0` and not go beyond `5`"]
            })

        data.update({"profile": profile.pk})
        data.update({"author": user.pk})
        return data


    def create(self, validated_data):
        """
        method to create and save a rating for
        """
        author = validated_data.get("author", None)
        profile = validated_data.get("profile", None)
        score = validated_data.get("score", 0)

        try:
            rating = Rating.objects.get(
                    author=author, 
                    profile__id=profile.id
                    )
        except Rating.DoesNotExist:
            return Rating.objects.create(**validated_data)

        rating.score = score
        rating.save()
        return rating

    class Meta:
        """
        class behaviours
        """
        model = Rating
        fields = ("score", "profile","author")