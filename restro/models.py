from django.db import models
from django.contrib.auth.models import User

class Keys(models.Model):
    key=models.CharField(max_length=10)


class Profile(models.Model):
    key=models.CharField(max_length=10,primary_key=True)
    mobile=models.IntegerField(max_length=10)
    email=models.CharField(max_length=100)
    name=models.CharField(max_length=100)

class Restaurants(models.Model):
    restraunt_owner=models.OneToOneField(User)
    restraunt_name=models.CharField(max_length=100)
    restraunt_id=models.IntegerField(primary_key=True)
    mobile=models.IntegerField(max_length=10,null=False)
    pin=models.IntegerField(default=1234)


class Visits(models.Model):
    visit_count=models.IntegerField()
    user_id=models.ForeignKey(Profile,unique=False)
    restaurant=models.ForeignKey(Restaurants,unique=False)
    last_visit=models.DateField()
class Discounts(models.Model):
    visit_count=models.IntegerField()
    discount_rate=models.IntegerField()
    restarant=models.ForeignKey(Restaurants,unique=False)
class Special_discount(models.Model):
    discount_rate=models.IntegerField()
    restaurant=models.ForeignKey(Restaurants)
    date=models.DateField()







