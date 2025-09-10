from django.contrib import admin
from django.urls import path
from .views import signup_view ,login_view ,logout_view,edit_profile,verify_otp,resend_code



urlpatterns = [
    path('signup/',signup_view,name='signup_view'),
    path('login/',login_view,name='login_view'),
    path('logout/', logout_view, name='logout'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('resend-code/', resend_code, name='resend_code'),
    path('verify-otp/', verify_otp, name='verify_otp'),
]
