"""rental_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views as v1
from bike_and_terminal import views as v2
from admin_app import views as v3
from payments import views as v4


urlpatterns = [
    path('', v1.homepage, name="homepage"),
    path('admin/', admin.site.urls),
    path('signup', v1.signup, name='signup'),
    path('signin', v1.signin, name='signin'),
    path('show_loc', v2.show_loc, name='show_loc'),
    path('admin_signin', v3.admin_signin, name='admin_signin'),
    path('admin_signup', v3.admin_signup, name='admin_signup'),
    path('rent_cal',v2.rent_cal, name='show_loc3'),
    path('signout',v1.signout,name='signout'),
    path('add_terminal',v3.create_terminal,name='add_terminal'),
    path('rent_cal',v2.rent_cal,name='rent_cal'),
    path('create_bike',v3.create_bike,name='create_bike'),
    path('update_balance',v4.update_balance,name='update_balance'),
    path('payment',v4.payment,name='payment'),
    path('update_balance_receipt',v4.update_balance_receipt,name='update_balance_receipt'),
    path('show_transactions',v4.show_transactions,name='show_transactions'),
    path('all_term',v2.all_term,name='all_term'),
]
