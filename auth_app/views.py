from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
        else:
            print(form.errors)
    template_name = 'auth_app/register.html'
    context = {'form': form}
    return render(request, template_name, context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_url')
        else:
            print("Invalid credentials")
    template_name = 'auth_app/login.html'
    return render(request, template_name)


def logout_user(request):
    logout(request)
    return redirect('login_url')