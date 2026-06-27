from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from foodapp.models import Restaurant
from accounts.decorators import customer_required

# Create your views here.
def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Prevent restaurant owners from using customer login
            if Restaurant.objects.filter(owner=user).exists():

                # Clear any existing authenticated session
                logout(request)

                messages.warning(
                    request,
                    "This account is registered as a restaurant owner. Please use the Restaurant Login page."
                )

                return redirect("restaurant_login")

            login(request, user)

            messages.success(
                request,
                "Welcome back!"
            )

            return redirect("home")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect('home')

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
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'accounts/register.html')

def forgot_password(request):
    return render(request, 'accounts/forgot_password.html')
@login_required(login_url='login')
def profile(request):

    if request.method == "POST":

        form = UserProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        form = UserProfileForm(
            instance=request.user
        )

    context = {
        "form": form
    }

    return render(
        request,
        "accounts/profile.html",
        context
    )