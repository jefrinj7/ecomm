from dataclasses import field
import email
from django.contrib.auth.forms import UserCreationForm
from platformdirs import user_cache_dir
from.models import Supplier, User
from django import forms

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2',}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2',}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2',}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2',}))
    FRUIT_CHOICES= [
    ('user', 'user'),
    ('supplier', 'supplier'),
    ]
    status= forms.CharField(label='Your status', widget=forms.Select(choices=FRUIT_CHOICES))

    class Meta:
        model=User
        fields = ['username','email','password1','password2','status']



    



