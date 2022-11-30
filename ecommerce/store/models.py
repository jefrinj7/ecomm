import datetime
from distutils.command.upload import upload
from itertools import product
from multiprocessing import Value
from re import T
from statistics import mode
from turtle import up
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.db import models
import os
from django.contrib.auth.models import User
from django.forms import FloatField, IntegerField

def get_file_path(request,filename):
    original_filename=filename
    nowTime=datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename="%s%s"%(nowTime, original_filename)
    return os.path.join('uploads/',filename)

class Category(models.Model):
    slug=models.CharField(max_length=150,null=False,blank=False)
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=get_file_path,null=True,blank=True)
    status=models.BooleanField(default=False,help_text="0=default,1=hidden")
    trending=models.BooleanField(default=False,help_text="0=default,1=Trending")
    meta_title=models.CharField(max_length=150,null=False,blank=False)
    meta_keywords=models.CharField(max_length=150,null=False,blank=False)
    meta_description=models.CharField(max_length=150,null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug=models.CharField(max_length=150,null=False,blank=False)
    name=models.CharField(max_length=150,null=False,blank=False)
    product_image=models.ImageField(upload_to=get_file_path,null=True,blank=True)
    small_description=models.CharField(max_length=150,null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    quantity= models.IntegerField(null=False,blank=False)
    reorder_level=models.IntegerField(null=False,blank=False)
    original_price= models.FloatField(null=False,blank=False)
    selling_price= models.FloatField(null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0=default,1=hidden")
    trending=models.BooleanField(default=False,help_text="0=default,1=Trending")
    tag=models.CharField(max_length=150,null=False,blank=False)
    meta_title=models.CharField(max_length=150,null=False,blank=False)
    meta_keywords=models.CharField(max_length=150,null=False,blank=False)
    meta_description=models.CharField(max_length=150,null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product =models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    fname=models.CharField(max_length=150,null=False)
    lname=models.CharField(max_length=150,null=False)
    email=models.CharField(max_length=150,null=False)
    phone=models.CharField(max_length=150,null=False)
    address=models.TextField(null=False)
    city=models.CharField(max_length=150,null=False)
    pincode=models.IntegerField(max_length=150,null=False)
    total_price=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=150,null=False)
    payment_id=models.CharField(max_length=250,null=True)
    orderstatus=(
        ('Pending','Pending'),
        ('Out For Shipping','Out For Shipping'),
        ('Delivered','Delivered'),
    )
    status=models.CharField(max_length=150,choices=orderstatus,default='Pending')
    message= models.TextField(null=True)
    tracking_no=models.CharField(max_length=150,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return'{} - {}'.format(self.id, self.tracking_no)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    price=models.FloatField(null=False)
    quantity=models.FloatField(null=False)


    def __str__(self):
        return'{} - {}'.format(self.order.id, self.order.tracking_no)

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone=models.CharField(max_length=150, null=False)
    address=models.TextField(null=False)
    city=models.CharField(max_length=150, null=False)
    pincode=models.IntegerField(max_length=150, null=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Supplier(models.Model):
    sid = models.IntegerField(name="sid",primary_key=True,)
    username=models.CharField(max_length=100,name="username",null=False)
    email=models.EmailField(max_length=200,unique=True,null=False,name="email")
    password=models.CharField(max_length=50,name="password")
    status=models.CharField(max_length=20,default='N')
    def __str__(self):
        return self.username

class Stocks(models.Model):
    product=models.TextField(null=False)
    user=models.ForeignKey(Supplier, on_delete=models.CASCADE)
    orderstatus=(
        ('Accepted','Accepted'),
        ('Rejected','Rejected'),
        ('Default','Default'),
    )
    status=models.CharField(max_length=200,choices=orderstatus,default='Default')
    






    




