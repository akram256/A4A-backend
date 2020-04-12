import re
from rest_framework import serializers
import math
from utils import services
from Auth.models import User


def validate_phone_number(phone):
    """Validate the phone number to match expected format"""
    p = re.compile(r'\+?\d{3}\s?\d{3}\s?\d{7}')
    q = re.compile(r'^.{10,16}$')
    if not (p.match(phone) and q.match(phone)):
        raise serializers.ValidationError(
            "Phone number must be of the format +234 123 4567890"
        )

def phonelookup(phone_no,use_con_code=None):
  phone_pattern = services.number_rule
  users= User.objects.all()
  phonelookup.phone_response = { 'exist' : {'message':'This phone number: {} , already belongs to a user on Twous'.format(phone_no),} , 'valid' : 'number looks good' , 'invalid' : {'message':'Phone number: {} is not valid'.format(phone_no),} }

  if phone_pattern(phone_no):
    if use_con_code is None:
      userx = [i for i in users if i.phone_no[-10:] == phone_no[-10:]]
    else:
      sample = phone_no[-10:]
      prefix = ('0','+234','234')
      bank = [i+sample for i in prefix]
      userx = [i.phone_no for i in users if i.phone_no in bank]
      return userx
    if userx:
      if use_con_code is None:
        return 'exist', userx[0]
    else:
       return 'valid', None
  else:
    if use_con_code is None:
      return 'invalid', None
    else:
      return None