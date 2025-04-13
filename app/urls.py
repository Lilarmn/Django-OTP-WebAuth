from django.contrib import admin
from django.urls import path , include
from django.shortcuts import render
from . import views as vw



urlpatterns = [
    path("login/", vw.loginMethod, name="login"),
    path("login/simple/",vw.simple_login , name="simple-login"),
    path("login/simple/signup/",vw.signup_view , name="signup"),
    path('login/OTP/', vw.send_otp, name='otp'),
    path('login/OTP/send_otp/', vw.send_otp, name='send_otp'),  # صفحه ارسال OTP
    path('login/OTP/verify_otp/', vw.verify_otp, name='verify_otp'),  # صفحه تایید OTP
    #path("logout/", vw.logout, name="logout"),
    #path("register/", vw.register, name="register"),
    path("home/", vw.home, name="home"),
]
