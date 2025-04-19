from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.timezone import now
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .redis_cli import redis_client
from .utils import get_client_ip , user_is_authenticated,generate_otp
from .forms import SignupForm ,EmailAuthenticationForm , OTPRequestForm
from .models import *

@user_is_authenticated
def redirect_to_home_or_login(request):
    return render(request, 'home.html')  
    

@user_is_authenticated
def home(request):
    return render(request, 'home.html', {})


def loginMethod(request):
    return render(request, 'loginMethod.html' )


def simple_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "welcome...")
            redis_client.set(f"{get_client_ip(request)}", now().isoformat(), ex=120)
            return redirect('home')
        else:
            messages.error(request, "wrong info")
    else:
        form = EmailAuthenticationForm()
    return render(request, "simple_login.html", {'form': form})

def signup_view(request):
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = CustomUser(email=email)
            user.set_password(password)  # رمز هش می‌شه ✅
            user.save()
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def send_otp(request):
    if request.method == 'POST':
        form = OTPRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user:
                otp = generate_otp()  # تولید OTP
                otp_instance = OTP(
                    user=user,
                    code_hash=otp,
                    expires_at=timezone.now() + timezone.timedelta(minutes=1),  # OTP برای ۵ دقیقه معتبر است
                    is_used=False
                )
                otp_instance.save()

                send_mail(
                    'OTP',
                    otp,
                    'YOUR_EMAIL_THAT_YOU_TO_SEND_FROM',  
                    [email], 
                    fail_silently=False,
                )
                print(otp)
                messages.success(request, "OTP Sent..")
                request.session['email'] = email
                return redirect('verify_otp') 
    else:
        form = OTPRequestForm()

    return render(request, 'send_otp.html', {'form': form ,"email":0})



def verify_otp(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')  

        user = CustomUser.objects.get(email = request.session['email'])
        otp_instance = OTP.objects.filter(user=user).last()  
        if otp_code == otp_instance.code_hash:
            otp_instance.is_used = True 
            otp_instance.save()

            # ورود کاربر
            login(request, user)
            redis_client.set(f"{get_client_ip(request)}", now().isoformat(), ex=120)
            return redirect('home')
        else:
            messages.error(request, "expired or wrong code ...")
    return render(request, 'verify_otp.html')


