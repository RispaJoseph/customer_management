# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Maker, Checker

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'photo', 'resume']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class MakerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Maker
        fields = ['checker']

class CheckerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Checker
        fields = []
