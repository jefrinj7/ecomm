from ast import Delete
from multiprocessing import context
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from store.models import Carts,Order, OrderItem, Product, Profile
import random 
from django.contrib import messages
from django.contrib.auth.models import User

@login_required(login_url='loginpage')
def index(request):
    rawcart = Carts.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            return render(request,"store/cart.html" )
    
    cartitems=Carts.objects.filter(user=request.user)
    total_price=0
    for item in cartitems:
        total_price= total_price + item.product.selling_price * item.product_qty
    
    userprofile= Profile.objects.filter(user=request.user).first()
        
    context ={'cartitems':cartitems,'total_price':total_price,'userprofile':userprofile}
    return render(request,"store/checkout.html",context)

@login_required(login_url='loginpage')
def placeorder(request):
    if(request.method == 'POST'):

        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name:
            currentuser.first_name= request.POST.get('fname')
            currentuser.last_name= request.POST.get('lname')
            currentuser.save()
        
        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone=request.POST.get('phone')
            userprofile.address=request.POST.get('address')
            userprofile.city=request.POST.get('city')
            userprofile.pincode=request.POST.get('pincode')
            userprofile.save()


        neworder=Order()
        neworder.user=request.user
        neworder.fname=request.POST.get('fname')
        neworder.lname=request.POST.get('lname')
        neworder.email=request.POST.get('email')
        neworder.phone=request.POST.get('phone')
        neworder.address=request.POST.get('address')
        neworder.city=request.POST.get('city')
        neworder.pincode=request.POST.get('pincode')
        neworder.payment_mode=request.POST.get('payment_mode')
        neworder.payment_id=request.POST.get('payment_id')

        cart=Carts.objects.filter(user=request.user)
        cart_total_price=0
        for item in cart:
            cart_total_price=cart_total_price + item.product.selling_price * item.product_qty

        neworder.total_price = cart_total_price
        trackno = 'abc'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'abc'+str(random.randint(1111111,9999999))

        neworder.tracking_no=trackno
        neworder.save()

        neworderitems = Carts.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price * item.product_qty,
                quantity=item.product_qty
            )
            #To decrease stock
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()

        Carts.objects.filter(user=request.user).delete()


        payMode = request.POST.get('payment_mode')
        if(payMode == "Online Transaction"):
            return JsonResponse({'status':"Your order has been placed Successfully"})
        
        else:
            messages.success(request,"Your order has been placed Successfully")
    return redirect('/')

@login_required(login_url='loginpage')
def razorpaycheck(request):
    cart = Carts.objects.filter(user=request.user)
    total_price=0
    for item in cart:
        total_price = total_price + item.product.selling_price * item.product_qty

    return JsonResponse({
        'total_price': total_price
    })


