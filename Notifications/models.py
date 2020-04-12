from django.db import models
from helpers.models import BaseAbstractModel
from Auth.models import Profile
# from Jobs.models import UserJob
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Notification(BaseAbstractModel):
    title = models.CharField(max_length=200)
    body = models.TextField()
    recipients = models.ManyToManyField(to=Profile,
                                        related_name='notifications',
                                        related_query_name='notification')
    time_stamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

# @receiver(post_save, sender=UserJob)
# def job_handler(sender, instance, **kwargs):
#     if instance.is_active:
#         profile_list = instance.author.profile.all()
#         subscribed_users = profile_list.filter(
#             Q(user__notification_subscription__in_app_notifications=True) | Q(
#                 user__notification_subscription__email_notifications=True))

#         email_subscribed_users = profile_list.filter(
#             user__notification_subscription__email_notifications=True)
#         if(subscribed_users.count() >= 1):

#             notification = Notification.objects.create(
#                 title="New Job on Twous",
#                 body=re.sub('  +', ' ', "{} has published another job \
#                                                 titled {}".format(
#                     instance.author.first_name.capitalize(),
#                     instance.title)))
#             notification.recipients.add(*subscribed_users)

#             if(email_subscribed_users.count() >= 1):
#                 send_emails_to_recipients(notification, email_subscribed_users)

#             notification.save()
