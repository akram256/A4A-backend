# Create your tasks here
from celery import task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from utils.services import send_Email
from django.conf import settings
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)
"""A handy class to send emails."""

@task()
def send_user_email(email, message, **kwargs):
    if settings.EMAIL_SWITCH != 'off':
        send_Email(email,message,**kwargs)
    else:
        logger.info(' emailservice has been paused')
    return True