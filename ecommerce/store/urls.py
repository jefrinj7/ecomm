from operator import index
from django.urls import path
from . import views
from store.controller import authview,carts,wishlist,checkout,order

urlpatterns = [
    path('',views.home, name="home"),
    path('collections',views.collections, name="collections"),
    path('collections/<str:slug>',views.collectionsview, name="collectionsview"),
    path('collections/<str:cate_slug>/<str:prod_slug>',views.productview,name="productview"),
    path('register/',authview.register, name="register"),
    path('login/',authview.loginpage, name="loginpage"),
    path('logout/',authview.logoutpage, name="logout"),
    path('add-to-cart',carts.addtocart,name="addtocart"),
    path('cart',carts.viewcart,name="cart"),
    path('update-cart',carts.updatecart,name="updatecart"),
    path('delete-cart-item',carts.deletecartitem,name="deletecartitem"),
    path('wishlist', wishlist.index,name="wishlist"),
    path('add-to-wishlist',wishlist.addtowishlist,name="addtowishlist"),
    path('delete-wishlist-item',wishlist.deletewishlistitem,name="deletewishlistitem"),
    path('checkout',checkout.index,name="checkout"),
    path('place-order',checkout.placeorder,name="placeorder"),
    path('proceed-to-pay',checkout.razorpaycheck,name="razorpaycheck"),
    path('my-orders',order.index,name="myorders"),
    path('view-order/<str:t_no>',order.vieworder,name="orderview"),
    path('product-list',views.productlist),
    path('searchproduct',views.searchproduct,name="searchproduct"),
    path('supplierproduct',views.supplierproduct,name="supplierproduct"),
    path('orderaccept/<product>',views.orderaccept,name='orderaccept'),
    path('orderdecline/<product>',views.orderdecline,name='orderdecline'),

    


]
