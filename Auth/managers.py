from django.contrib.auth.models import BaseUserManager
from django.db.models import QuerySet
import string
import random

class UserManager(BaseUserManager):
    def create_user(self, phone_no, password=None, **kwargs):
        user = self.model(phone_no=phone_no, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class AuthGen():
    @classmethod
    def createToken(cls,n=8):
        NUMSEQ = string.digits
        token = lambda n: (''.join(random.choice(NUMSEQ) for _ in range(n)))
        return token(n)
    
    @classmethod
    def uniqueToken(cls,token,tokenbank):
        lock = True
        while lock:
            value = tokenbank.get(token,False)
            lock = True if value else value
        return token



class CustomQuerySet(QuerySet):
    """
    Custom queryset that will be reused by different models.
    It enables soft delete and precise filtering, (ie to get all
    property that has not been soft deleted, simply run:
        Property.active_objects.all_objects()
        )
    """

    def _active(self):
        """Return only objects that haven't been soft deleted."""
        return self.filter(is_deleted=False)

    def all_objects(self):
        """Return all objects that haven't been soft deleted"""
        return self._active()