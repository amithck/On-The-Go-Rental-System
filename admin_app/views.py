from django.shortcuts import render, redirect
from .models import admins
from bike_and_terminal.models import terminal, bike
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from common.auth_helpers import is_admin_user, admin_required
from django.db.models import F


@login_required(login_url='/signin')
def admin_signup(request):
    if not is_admin_user(request.user):
        return redirect('/')

    error = ''
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('pass', '').strip()
        fname = request.POST.get('fname', '').strip()
        lname = request.POST.get('lname', '').strip()

        nu = authenticate(request, username=email, password=password)
        if nu is not None:
            admins.objects.create(user=email, password=password, fname=fname, lname=lname)
            return redirect('/')
        error = 'Authentication failed. Please check the email and password.'

    return render(request, 'admin_signup.html', {'error': error})


def admin_signin(request):
    error = ''
    if request.method == 'POST':
        email = request.POST.get('email1', '').strip()
        password = request.POST.get('pass1', '').strip()
        user = authenticate(request, username=email, password=password)
        if user is not None and is_admin_user(user):
            login(request, user)
            return redirect('/')
        error = 'Login failed or user is not an admin.'
    return render(request, 'admin_signin.html', {'error': error})


@admin_required
def create_terminal(request):
    error = ''
    if request.method == 'POST':
        term_id = request.POST.get('term_id', '').strip()
        term_name = request.POST.get('term_name', '').strip()
        latitude = request.POST.get('lat')
        longitude = request.POST.get('lon')
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            terminal.objects.create(
                term_id=term_id,
                term_name=term_name,
                latitude=latitude,
                longitude=longitude,
                no_of_bikes=0,
            )
            return redirect('/')
        except (TypeError, ValueError):
            error = 'Latitude and longitude must be valid numbers.'

    return render(request, 'add_terminal.html', {'error': error})


@admin_required
def create_bike(request):
    error = ''
    if request.method == 'POST':
        bike_id = request.POST.get('bike_id', '').strip()
        bike_name = request.POST.get('bike_name', '').strip()
        bike_type = request.POST.get('bike_type', '').strip()
        rent_cost = request.POST.get('rent_cost', '').strip()
        term_id = request.POST.get('term_id', '').strip()
        try:
            rent_cost = int(rent_cost)
            bike.objects.create(
                bike_id=bike_id,
                bike_name=bike_name,
                bike_type=bike_type,
                rent_cost=rent_cost,
                term_id_id=term_id,
            )
            terminal.objects.filter(term_id=term_id).update(no_of_bikes=F('no_of_bikes') + 1)
            return redirect('/')
        except (ValueError, TypeError):
            error = 'Rent cost must be a valid integer.'

    return render(request, 'create_bike.html', {'error': error})