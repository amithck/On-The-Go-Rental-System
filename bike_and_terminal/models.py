from django.db import models


class terminal(models.Model):
    term_id=models.CharField(max_length = 5, primary_key = True)
    term_name=models.CharField(max_length = 20)
    no_of_bikes=models.IntegerField(default = 0)
    latitude= models.DecimalField(max_digits=8,decimal_places=4)
    longitude= models.DecimalField(max_digits=8,decimal_places=4)


class bike(models.Model):
    Electric = 'ev'
    Fuel = 'fe'
    BIKETYPES=[(Electric,'electric'),(Fuel,'fuel')]
    bike_id=models.CharField(max_length = 5, primary_key = True)
    bike_name=models.CharField(max_length=15)
    bike_type=models.CharField(max_length=2,choices=BIKETYPES)
    rent_cost=models.IntegerField()
    term_id=models.ForeignKey(terminal,on_delete=models.SET_NULL,null=True)

class distance(models.Model):
    term_id=models.ForeignKey(terminal,on_delete=models.CASCADE,null=True)
    startdistance=models.CharField(max_length=20,default="")
    enddistance=models.CharField(max_length=20,default="")

class rent(models.Model):
    bike_id=models.ForeignKey(bike,on_delete=models.CASCADE,null=True)
    rent_cost=models.CharField(max_length=10)
    fromt=models.CharField(max_length=5,default="")
    tot=models.CharField(max_length=5,default="")