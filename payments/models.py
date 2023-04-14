from django.db import models
from bike_and_terminal.models import bike
from user.models import auth
from datetime import datetime
from zoneinfo import ZoneInfo
from django.utils import timezone

class payments_bike(models.Model):
    receipt_no=models.CharField(max_length=5,primary_key=True)
    date=models.DateTimeField(default=timezone.now)
    bike_id=models.ForeignKey(bike,on_delete=models.SET_NULL,null=True)
    email=models.ForeignKey(auth,on_delete=models.SET_NULL,null=True)
    cost=models.CharField(max_length=10,default="")

class payments_user(models.Model):
    receipt_no=models.CharField(max_length=5,primary_key=True)
    date=models.DateTimeField(default=timezone.now)
    email=models.ForeignKey(auth,on_delete=models.SET_NULL,null=True)
    cost=models.CharField(max_length=10,default="")
    cardNo=models.CharField(max_length=16,default="")