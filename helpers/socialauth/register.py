from django.contrib.auth import authenticate
from Auth.models import User


# def register_user(phone_no, email):
#     user = User.objects.filter(phone_no=phone_no)

#     if not user.exists():
#         user = {
#             'phone_no': phone_no, 'email': email, 'password': 'XXXXXXXX','role':role}
#         User.objects.create_user(**user)
#         new_user = authenticate(phone_no=phone_no, password="XXXXXXXX",role=role)
#         return new_user.token
#     else:
#         User.objects.filter(phone_no=phone_no)
#         registered_user = authenticate(phone_no=phone_no, password="XXXXXXXX",role=role)
#         return registered_user.token



def register_user(email, name):
    user = User.objects.filter(email=email)

    if not user.exists():
        user = {
            'username': name, 'email': email, 'password': 'XXXXXXXX'}
        User.objects.create_user(**user)
        new_user = authenticate(email=email, password="XXXXXXXX")
        return new_user.token
    else:
        User.objects.filter(email=email)
        registered_user = authenticate(email=email, password="XXXXXXXX")
        return registered_user.token