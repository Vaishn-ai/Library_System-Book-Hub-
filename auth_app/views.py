from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP
import random

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register_url')

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect('register_url')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register_url')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        otp_code = str(random.randint(100000, 999999))
        EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp_code, 'is_verified': False})

        send_mail(
            subject='BookHub — Your OTP Verification Code',
            message=f'Hi {username},\n\nYour OTP is: {otp_code}\n\nThis code is valid for 10 minutes.\n\n— BookHub Team',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        request.session['otp_user_id'] = user.id
        messages.success(request, f"OTP sent to {email}. Please verify to activate your account.")
        return redirect('verify_otp_url')

    return render(request, 'auth_app/register.html')


def verify_otp_view(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        return redirect('register_url')

    user = User.objects.filter(id=user_id).first()
    if not user:
        return redirect('register_url')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        otp_obj = EmailOTP.objects.filter(user=user).first()

        if otp_obj and otp_obj.otp == entered_otp:
            user.is_active = True
            user.save()
            otp_obj.is_verified = True
            otp_obj.save()
            del request.session['otp_user_id']
            messages.success(request, "Email verified! You can now login.")
            return redirect('login_url')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'auth_app/verify_otp.html', {'email': user.email})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home_url')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'auth_app/login.html')


def logout_view(request):
    logout(request)
    return redirect('login_url')