from celery import task
from django.core.mail import send_mail
from .models import Bookings
@task
def Booking_created(order_id):
    """
    Task to send an e-mail notification when a booking is
    successfully created.
    """
    Bookings = Bookings.objects.get(id=order_id)
    subject = f'Bookings nr. {Bookings.id}'
    message = f'Dear {Bookings.first_name},\n\n' \
              f'You have successfully Booked.' \
              f'Your Bookings ID is {Bookings.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'karungilydia@gmail.com',
                          [Bookings.email])
    return mail_sent