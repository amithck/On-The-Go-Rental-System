from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from requests.adapters import HTTPAdapter, Retry
from django.db import connection
from .models import payments_bike,payments_user
import string
import random
from datetime import datetime

@login_required(login_url='/signin')
def payment(request):
    if request.method == 'POST':
        id=request.POST['bike_chosen']
        
        current_user = request.user
        with connection.cursor() as cursor:
            cursor.execute(f"select fromt from bike_and_terminal_rent where bike_id_id = '{id}'")
            fromt=cursor.fetchall()
            fromt1=fromt[0]
            cursor.execute(f"select tot from bike_and_terminal_rent where bike_id_id = '{id}'")
            tot=cursor.fetchall()
            tot1=tot[0]
            fromt2=str(fromt1[0])
            tot2=str(tot1[0])
            cursor.execute(f"update bike_and_terminal_bike set term_id_id='{tot2}' where bike_id = '{id}'")
            cursor.execute(f"update bike_and_terminal_terminal set no_of_bikes= (no_of_bikes - 1) where term_id = '{fromt2}'")
            cursor.execute(f"update bike_and_terminal_terminal set no_of_bikes= (no_of_bikes + 1) where term_id = '{tot2}'")
            cursor.execute(f"select rent_cost from bike_and_terminal_rent where bike_id_id = '{id}'")
            rent0=cursor.fetchall()
            rent1=rent0[0]
            cursor.execute(f"update user_auth set balance = (balance - {rent1[0]}) where email = '{current_user}'")
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        new_receipt= payments_bike(email_id=current_user,cost=rent1[0],bike_id_id=id,receipt_no=str(res))
        new_receipt.save()
        query_results = [str(res),datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),id,current_user,rent1[0]]
        context={'query_results':query_results}
    return render(request, 'payment.html',context)

@login_required(login_url='/signin')
def update_balance(request):
    current_user = request.user
    with connection.cursor() as cursor:
        cursor.execute(f"select balance from user_auth where email = '{current_user}'")
        bal=cursor.fetchall()
        bal0=bal[0]
        balance=bal0[0]
    text=(f"Curent balance:{balance}")        
    context={'text':text}
    return render(request, 'update_balance.html',context)

@login_required(login_url='/signin')
def update_balance_receipt(request):
    if request.method == 'POST':
        add_balance=request.POST['balance']
        credit= request.POST['card']
        current_user = request.user
        with connection.cursor() as cursor:
                cursor.execute(f"update user_auth set balance = (balance + {add_balance}) where email = '{current_user}'")
                cursor.execute(f"select balance from user_auth where email = '{current_user}'")
                bal=cursor.fetchall()
                bal0=bal[0]
                balance=bal0[0]
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        new_receipt= payments_user(email_id=current_user,cost=add_balance,receipt_no=str(res),cardNo=credit)
        new_receipt.save()
        query_results = [str(res),datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),current_user,add_balance,credit]
        text=(f"Curent balance:{balance}")
        context={'query_results':query_results,'text':text}
    return render(request, 'update_balance_receipt.html',context)

@login_required(login_url='/signin')
def show_transactions(request):
    current_user = request.user
    user_pay=payments_user.objects.filter(email=str(current_user))
    bike_pay=payments_bike.objects.filter(email=str(current_user))
    context={'user_pay':user_pay,'bike_pay':bike_pay}
    return render(request, 'show_transactions.html',context)
