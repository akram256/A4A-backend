
from django.urls import path
from authentication.views import (RegistrationView, EmailVerificationView)


app_name = 'authentication'

urlpatterns = [
  path("register/", RegistrationView.as_view(), name="register"),
  path("verify/", EmailVerificationView.as_view(), name="verify")
]