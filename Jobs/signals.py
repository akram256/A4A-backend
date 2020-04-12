from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import secrets
from Jobs.models import Artist

@receiver(pre_save, sender=Artist)
def create_job(sender, instance,**kwargs):
   instance.id=secrets.token_hex(8)
