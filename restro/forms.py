from django import forms
from .models import *
class ProfileForms(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['key','mobile','email','name']
class LogForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput)
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		fields = ['username', 'password']
class Restaurant_discount_Form(forms.Form):
    visits=forms.IntegerField()
    discounts=forms.IntegerField()
class Restaurant_special_discount_Form(forms.Form):
    discount_rate=forms.IntegerField()
    date=forms.DateField()
class User_redeemForm(forms.Form):
    amount=forms.IntegerField()
    pin=forms.IntegerField()
class Restarant_redeemForm(forms.Form):
    user_key=forms.CharField(widget=forms.TextInput)
    amount=forms.IntegerField()
class User_infoForm(forms.Form):
    user_key=forms.CharField(widget=forms.TextInput)









