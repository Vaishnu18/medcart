from django.contrib import admin
from django.urls import path,include
from ecommerceapp import views
urlpatterns = [
    
    path('',views.index,name="index"),
    path('contact',views.contact,name="contact"),
    path('about',views.about,name="about"),
    path('checkout/',views.checkout,name="Checkout"),
    path('payment/',views.payment,name="payment"),
    path('orders/',views.orders,name="orders"),
    path('search/', views.search, name='search'),

]
