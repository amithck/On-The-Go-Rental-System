from django.db import models

class admins(models.Model):
    user=models.CharField(max_length=20,primary_key=True)
    password=models.CharField(max_length=20)
    fname=models.CharField(max_length=20,default="")
    lname=models.CharField(max_length=20,default="")