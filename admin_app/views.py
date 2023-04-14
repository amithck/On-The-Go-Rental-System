from django.shortcuts import render
from .models import admins
from bike_and_terminal.models import terminal, bike
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

@login_required(login_url='/signin')
def admin_signup(request):
    f=''
    flag = admin_required(request)
    if flag == 1:
        if request.method == 'POST':
            email=request.POST['email']
            password=request.POST['pass']
            fname=request.POST['fname']
            lname=request.POST['lname']
            nu= authenticate(request, username=email, password=password)
            if nu is not None:
                new_user= admins(user=email,password=password,fname=fname,lname=lname)
                new_user.save()
            else:
                f='Authentication Failed. Please try again.'
    else:
        return redirect('http://127.0.0.1:8000/')
    response={'f':f} 
    return render(request, 'admin_signup.html',response)
        
def admin_signin(request):
    flag = admin_required(request)
    if flag == 1:
        if request.method == 'POST':
            email=request.POST['email1']
            password=request.POST['pass1']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
    else:
        return redirect('http://127.0.0.1:8000/')
    return render(request, 'admin_signin.html')

@login_required(login_url='/signin')
def create_terminal(request):
    flag = admin_required(request)
    if flag == 1:
        if request.method == 'POST':
            term_id=request.POST['term_id']
            term_name=request.POST['term_name']
            latitude= float(request.POST['lat'])
            longitude = float(request.POST['lon'])
            new_term = terminal(term_id=term_id,term_name=term_name,latitude=latitude,longitude=longitude,no_of_bikes=0)
            new_term.save()
    else:
        return redirect('http://127.0.0.1:8000/')
    return render(request, 'add_terminal.html')

@login_required(login_url='/signin')
def create_bike(request):
    flag = admin_required(request)
    if flag == 1:
        if request.method == 'POST':
            bike_id=request.POST['bike_id']
            bike_name=request.POST['bike_name']
            bike_type= request.POST['bike_type']
            rent_cost = request.POST['rent_cost']
            term_id = request.POST['term_id']
            new_bike = bike(bike_id=bike_id,bike_name=bike_name,bike_type=bike_type,rent_cost=rent_cost,term_id_id=term_id)
            new_bike.save()
            with connection.cursor() as cursor:
                cursor.execute(f"update bike_and_terminal_terminal set no_of_bikes = (no_of_bikes + 1) where term_id = '{term_id}'")
    else:
        return redirect('http://127.0.0.1:8000/')
    return render(request, 'create_bike.html')



def admin_required(request):
    current_user = request.user
    flag=0
    with connection.cursor() as cursor:
        cursor.execute("select * from admin_app_admins")
        adm=cursor.fetchall()
    for adm1 in adm:
        if(str(current_user) == str(adm1[0])):
            flag = 1
    return flag