from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from helpers.models import BaseAbstractModel
from .managers import UserManager
import uuid
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

class User(AbstractBaseUser, PermissionsMixin, BaseAbstractModel):
    """This is a user model """
    ROLES = (
        ('PROVIDER', 'PROVIDER'),
        ('USER', 'USER')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=255, blank=True, null=True, choices=ROLES)
    phone_no = models.CharField(max_length=15, unique=True,blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = ['email',]
    objects = UserManager()

    def __str__(self):
        if self.first_name:
            return "{}".format(self.first_name)
        return "{}".format(self.phone_no)

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=365)

        token = jwt.encode({
            'id': str(self.pk),
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

class Subscription(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="notification_subscription"
    )
    email_notifications = models.BooleanField(default=False)
    in_app_notifications = models.BooleanField(default=False)

class Profile(BaseAbstractModel):
    """This is model for  Profile """
    user =models.OneToOneField(to='Auth.User', on_delete=models.CASCADE, null=True) 
    location = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile/', null=True)
    user_rates = models.CharField(max_length=10, default=0)
    details=models.TextField(null=True)
    # reviews=models.ForeignKey(to='')
    Deals = models.IntegerField(blank=True, null=True, default=0)
    Cost=models.DecimalField(max_digits=12, decimal_places=2, null=True)


    def __str__(self):
        return "{}".format(self.user)

    @property
    def phone_no(self):
        return self.user.phone_no

    @property
    def first_name(self):
        return self.user.first_name
    
    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def average_rating(self):
        """
        method to calculate the average rating of a user.
        """
        ratings = self.scores.all().aggregate(score=Avg("score"))
        return float('%.2f' % (ratings["score"] if ratings['score'] else 0))


    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            Subscription.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

    
    @property
    def user_phone_no(self):
        self.user.phone_no

class Reviews(BaseAbstractModel):
    """This is model for both user and job reviews"""
    
    profile=models.ForeignKey(to='Auth.Profile', on_delete=models.DO_NOTHING, null=True,related_name='reviews')
    rating = models.IntegerField(blank=True, null=True)
    reviews= models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.reviews)

class Rating(models.Model):
    """
        Model for rating an provider
    """
    author = models.ForeignKey(
        'Auth.User',
        on_delete=models.CASCADE,
        null=True)
    profile = models.ForeignKey(
        'Auth.Profile',
        on_delete=models.CASCADE,
        related_name="scores",
        null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ["-score"]


