from django.db import models

class auth(models.Model):
    email = models.CharField(max_length = 30, primary_key = True)
    fname = models.CharField(max_length = 20)
    lname = models.CharField(max_length = 20)
    password = models.CharField(max_length = 15)
    phone = models.CharField(max_length = 10, unique = True)
    dl_num = models.CharField(max_length = 15, unique = True)
    balance = models.DecimalField(max_digits=8,decimal_places=2,default=0.00)