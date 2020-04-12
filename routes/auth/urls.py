from django.urls import path

from Auth.views import (
    RegistrationAPIView,LoginAPIView,
    VerifyAccount,FacebookSocialAuthView,GoogleSocialAuthView,TwitterSocialAuthView,
    ResetPasswordRequest,ResetPasswordConfirm,ListProfileView,
    RetrieveUpdateProviderProfileView,ReviewView,
    # UserViewProviderProfile,
    ListProvidersView,
    RatingsView
    # ProfileUpdate
    )

app_name = 'Auth'

urlpatterns = [
    path('verify/',VerifyAccount.as_view(),name='verify'),
    path("register/", RegistrationAPIView.as_view(), name='register'),
    path("login/",LoginAPIView.as_view(), name='login'),
    path('facebook/', FacebookSocialAuthView.as_view(),name='facebook'),
    path('google/', GoogleSocialAuthView.as_view(), name='google'),
    path('twitter/', TwitterSocialAuthView.as_view(),name='twitter'),
    path('resetpassword/request', ResetPasswordRequest.as_view(), name='password-reset-request'),
    path('resetpassword/confirm', ResetPasswordConfirm.as_view(), name='password-reset-confirm'),
    path('profile',ListProfileView.as_view(), name='list profiles'),
    path('profile/<int:id>',RetrieveUpdateProviderProfileView.as_view(), name='update-and-delete-profile'),
    # path('user/view/provider/profiles',UserViewProviderProfile.as_view(), name='user-view-provider-profiles'),
    path('provider/',ListProvidersView.as_view(),name='get-all-providers'),
    # path('profile/<str:id>',ProfileUpdate.as_view(), name='update-and-delete-profile'),
    path('reviews/<int:id>',ReviewView.as_view(),name='get-and-add-reviews'),
    path('provider/rate/<int:id>',RatingsView.as_view(),name='rating'),

]
