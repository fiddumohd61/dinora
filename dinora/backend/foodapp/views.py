from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'foodapp/index.html')

def menu(request):
    return render(request, 'foodapp/menu.html')

def about(request):
    return render(request, 'foodapp/about.html')

def contact(request):
    return render(request, 'foodapp/contact.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'foodapp/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'foodapp/register.html')

def cart(request):
    return render(request, 'foodapp/cart.html')

def checkout(request):
    return render(request, 'foodapp/checkout.html')

def restaurants(request):
    return render(request, 'foodapp/restaurants.html')

def offers(request):
    return render(request, 'foodapp/offers.html')
