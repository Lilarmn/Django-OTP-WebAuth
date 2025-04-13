from django.shortcuts import redirect
from .redis_cli import redis_client
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import random
from django.contrib.auth.hashers import make_password

def user_is_authenticated(view_func):
    def wrapper(request , *args, **kwargs):
        if request.user.is_authenticated and redis_client.get(request.META.get('REMOTE_ADDR')):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login') 
    return wrapper

def get_client_ip(request):
    return request.META.get('REMOTE_ADDR')




def generate_otp():
    otp = str(random.randint(100000, 999999))
    return make_password(otp)[-8:] 


# kimiaforeducation@gmail.com