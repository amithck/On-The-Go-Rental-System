from django.shortcuts import render
from .models import auth
from .forms import authform
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect




def signup(request):
    if request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/')
    form = authform()
    if request.method == 'POST':
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        password=request.POST['pass']
        phone=request.POST['phone']
        dl_num=request.POST['dl_num']


        new_user= auth(email=email,fname=fname,lname=lname,password=password,phone=phone,dl_num=dl_num,balance=0)
        new_user.save()
        user = User.objects.create_user(email, email, password)
        user.first_name = fname
        user.last_name = lname
        user.save()
    return render(request, 'signup.html')
        
def signin(request):
    f=''
    response={'f':f}
    if request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/')
    if request.method == 'POST':
        email=request.POST['email1']
        password=request.POST['pass1']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/')
        else:
            f='Login Failed. Please try again.'
            response={'f':f}
    return render(request, 'signin.html',response)

def signout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')

def homepage(request):
    flag=(admin_required(request))
    if (flag==1):
        return render(request, 'homepage_admin.html')
    elif request.user.is_authenticated:
        return render(request, 'homepage_loggedin.html')
    else:
        return render(request, 'homepage.html')


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