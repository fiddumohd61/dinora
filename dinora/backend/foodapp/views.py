from django.shortcuts import render

def home(request):
    return render(request, 'foodapp/index.html')

def menu(request):
    return render(request, 'foodapp/menu.html')

def about(request):
    return render(request, 'foodapp/about.html')

def contact(request):
    return render(request, 'foodapp/contact.html')

def login(request):
    return render(request, 'foodapp/login.html')

def register(request):
    return render(request, 'foodapp/register.html')

def cart(request):
    return render(request, 'foodapp/cart.html')

def checkout(request):
    return render(request, 'foodapp/checkout.html')

def restaurants(request):
    return render(request, 'foodapp/restaurants.html')

def offers(request):
    return render(request, 'foodapp/offers.html')
