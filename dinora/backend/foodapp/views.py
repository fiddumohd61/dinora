from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import restaurant

def home(request):
    return render(request, 'foodapp/index.html')

def menu(request):
    return render(request, 'foodapp/menu.html')

def about(request):
    return render(request, 'foodapp/about.html')

def contact(request):
    return render(request, 'foodapp/contact.html')



def cart(request):
    return render(request, 'foodapp/cart.html')

def checkout(request):
    return render(request, 'foodapp/checkout.html')

def restaurants(request):
    restaurant_list = restaurant.objects.all()
    return render(request, 'foodapp/restaurants.html', {
        'restaurants': restaurant_list
    })

def hotel_paradise_menu(request):
    return render(request, 'foodapp/hotel_paradise_menu.html', {
        'restaurant_name': 'Hotel Paradise'
    })

def food_court_menu(request):
    return render(request, 'foodapp/menu_items.html', {
        'restaurant_name': 'Food Court'
    })

def offers(request):
    return render(request, 'foodapp/offers.html')
