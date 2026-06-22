from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('restaurants/', views.restaurants, name='restaurants'),

    path('hotel_paradise_menu/', views.hotel_paradise_menu, name='hotel_paradise_menu'),
    path('pizzahut_menu/', views.pizzahut_menu, name='pizzahut_menu'),
    path('kfc_menu/', views.kfc_menu, name='kfc_menu'),

    path('offers/', views.offers, name='offers'),
]