from email import message
from itertools import product
from multiprocessing import context
import re
from telnetlib import STATUS
from unicodedata import category
from django.http import JsonResponse
from django.shortcuts import redirect, render
from flask import request
from . models import *
from django.contrib import messages
from django.views.generic import CreateView,ListView
from .forms import *

def home(request):
    trending_products = Product.objects.filter(trending=1)
    context = {'trending_products':trending_products}
    return render(request,"store/index.html",context)

def collections(request):
    category=Category.objects.filter(status=0)
    context={'category':category}
    return render(request,'store/collections.html',context)

def collectionsview(request, slug):
    if(Category.objects.filter(slug=slug, status=0)):
        products=Product.objects.filter(category__slug=slug)
        category=Category.objects.filter(slug=slug).first()
        context={'products':products,'category':category}
        return render(request,'store/products/index.html',context)
    else:
        messages.warning(request,"No such category found")
        return redirect('collections')

def productview(request, cate_slug,prod_slug):
    if(Category.objects.filter(slug=cate_slug,status=0)):
        if(Product.objects.filter(slug=prod_slug,status=0)):
            products=Product.objects.filter(slug=prod_slug,status=0).first
            context={'products':products}
            

        else:
            messages.error(request,"No such product found")
            return redirect('collections')

    else:
        messages.error(request,"No such category found")
        return redirect('collections')
    return render(request,"store/products/view.html",context)

def productlist(request):
    products = Product.objects.filter(status=0).values_list('name',flat=True)
    productlist= list(products)

    return JsonResponse(productlist, safe=False)

def searchproduct(request):
    if request.method == 'POST':
        searcheditem=request.POST.get('productsearch')
        if searcheditem =="":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains=searcheditem).first()

            if product:
                return redirect('collections/'+product.category.slug+'/'+product.slug)
            else:
                messages.info(request,"No Product Found")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

def supplierproduct(request):
    products = Stocks.objects.raw('SELECT * from store_stocks where status="Default"')
    return render(request,"store/sup-pro.html",{'products':products})

def orderaccept(request,product):
    if Stocks.objects.filter(product=product).exists():
        obj=Stocks.objects.get(product=product)
        obj.status="Accepted"
        obj.save()
    return render(request,'store/supplier.html')    

def orderdecline(request,product):
    if Stocks.objects.filter(product=product).exists():
        obj=Stocks.objects.get(product=product).delete()
        obj.status="Rejected"
        obj.save()
    return render(request,'store/supplier.html')    
    













   




