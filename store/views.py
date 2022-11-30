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
import pandas as pd
from numpy import array

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
            product_dis=Product.objects.get(slug=prod_slug)
            prod=product_dis.name
            print(prod)
            if(OrderItem.objects.filter(product_name=prod)):
                recomendation = RecommendProduct(prod)
                rec_array = []
                for recomendations in recomendation:
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++",recomendations)
                    recomends=Product.objects.get(name=recomendations)
                    rec_array.append(recomends)
                    print(rec_array)
                    context={'products':products,'rec_array':rec_array}
            else:
                context={'products':products}

        

        else:
            messages.error(request,"No such product found")
            return redirect('collections')

    else:
        messages.error(request,"No such category found")
        return redirect('collections')
    return render(request,"store/products/view.html",context)

def RecommendProduct(prod):
    # product_name = str(product_name)
    p_array = []
    p_array.append(prod)
    # product_name = array(product_name)
    products_prob = pd.read_csv("D:/ecommerce/products_prob.csv")
    #Add item to baske
    basket = p_array
    
    #Select the number of relevant items to suggest
    no_of_suggestions = 3

    all_of_basket = products_prob[basket]
    all_of_basket = all_of_basket.sort_values(by = basket, ascending=False)
    suggestions_to_customer = list(all_of_basket.index[:no_of_suggestions])
    recommend_array = []
    for recommendations in suggestions_to_customer:
        recommend_array.append(products_prob.loc[recommendations,'Unnamed: 0'])
    print(recommend_array)
    return recommend_array

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

def supplier(request):
    user=Stocks.objects.filter(user=request.user)
    return render(request,"store/supplier.html",{'user':user})


def supplierproduct(request):
    products = Stocks.objects.filter(user_id=request.user)
    return render(request,"store/sup-pro.html",{'products':products})

def orderaccept(request,product):
    if Stocks.objects.filter(product=product).exists():
        obj=Stocks.objects.get(product=product)
        obj.status="Accepted"
        obj.save()
    return render(request,'store/supplier.html')    

def orderdecline(request,product):
    if Stocks.objects.filter(product=product).exists():
        obj=Stocks.objects.get(product=product)
        obj.status="Rejected"
        obj.save()
    return render(request,'store/supplier.html')   

def review(request):
    review=OrderItem.objects.filter(user=request.user).order_by('-id')
    return render(request, 'store/review.html'),{ 'review':review }
    













   




