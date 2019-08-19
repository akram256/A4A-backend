
from django.urls import path
from authentication.views import RegistrationView


app_name = 'authentication'

urlpatterns = [
  path("register/", RegistrationView.as_view(), name="register"),
]