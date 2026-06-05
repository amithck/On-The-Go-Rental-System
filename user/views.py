from django.shortcuts import render, redirect
from .models import auth
from .forms import authform
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from common.auth_helpers import is_admin_user
from django.db import IntegrityError




def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    error = ''
    form = authform()
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        fname = request.POST.get('fname', '').strip()
        lname = request.POST.get('lname', '').strip()
        password = request.POST.get('pass', '').strip()
        phone = request.POST.get('phone', '').strip()
        dl_num = request.POST.get('dl_num', '').strip()

        if not email or not password:
            error = 'Email and password are required.'
        elif User.objects.filter(username=email).exists() or auth.objects.filter(email=email).exists():
            error = 'A user with this email already exists.'
        else:
            try:
                auth.objects.create(
                    email=email,
                    fname=fname,
                    lname=lname,
                    password=password,
                    phone=phone,
                    dl_num=dl_num,
                    balance=0,
                )
                user = User.objects.create_user(username=email, email=email, password=password)
                user.first_name = fname
                user.last_name = lname
                user.save()
                return redirect('signin')
            except IntegrityError:
                error = 'Unable to create account. Please check your details and try again.'

    return render(request, 'signup.html', {'form': form, 'error': error})


def signin(request):
    if request.user.is_authenticated:
        return redirect('/')

    error = ''
    if request.method == 'POST':
        email = request.POST.get('email1', '').strip()
        password = request.POST.get('pass1', '').strip()
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        error = 'Login failed. Please try again.'

    return render(request, 'signin.html', {'error': error})

def signout(request):
    logout(request)
    return redirect('/')

def homepage(request):
    if is_admin_user(request.user):
        return render(request, 'homepage_admin.html')
    if request.user.is_authenticated:
        return render(request, 'homepage_loggedin.html')
    return render(request, 'homepage.html')


