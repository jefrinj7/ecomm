from email import message
from imaplib import _Authenticator
import imp
from unicodedata import name
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from multiprocessing import context
from django.shortcuts import redirect, render
from flask import request
from store.forms import CustomUserForm

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form= CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered Succesfully")
            return redirect('/login')
    context ={'form':form}
    return render(request,"store/auth/register.html",context)


def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in")
        return redirect('/')
    else:
        if request.method == 'POST':
            name=request.POST.get('username')
            passwd=request.POST.get('password')
            user= authenticate(request,username=name,password=passwd)
            
            if user is not None:
                if user.is_staff == True:
                    login(request,user)
                    messages.success(request,"Logged in succesfully")
                    return render(request,"store/supplier.html")
                else:
                    login(request,user)
                    messages.success(request,"Logged in succesfully")
                    return redirect("/")
            
            else:
                messages.error(request,"Invalid Username or Password")
                return redirect('/login')
        return render(request,"store/auth/login.html")


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect("/")

    