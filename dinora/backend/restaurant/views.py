from django.shortcuts import render, redirect, get_object_or_404
from .forms import FoodForm, RestaurantProfileForm
from foodapp.models import Order, FoodItem, Restaurant, Review
from django.db.models import Sum, Count
from django.contrib import messages
from datetime import date
from django.contrib.auth import authenticate, login, logout
from .decorators import restaurant_owner_required


def restaurant_login(request):

    if request.user.is_authenticated:

        if Restaurant.objects.filter(owner=request.user).exists():
            return redirect("restaurant_dashboard")


    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            if Restaurant.objects.filter(owner=user).exists():

                login(request, user)

                return redirect("restaurant_dashboard")

            else:
                messages.error(
                    request,
                    "You are not registered as a restaurant owner."
                )

        else:
            messages.error(
                request,
                "Invalid username or password."
            )


    return render(
        request,
        "restaurant/login.html"
    )



@restaurant_owner_required
def restaurant_logout(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("restaurant_login")



@restaurant_owner_required
def dashboard(request):

    restaurant = get_object_or_404(
        Restaurant,
        owner=request.user
    )


    total_foods = FoodItem.objects.filter(
        restaurant=restaurant
    ).count()


    orders = Order.objects.filter(
        orderitem__food__restaurant=restaurant
    ).distinct()


    total_orders = orders.count()


    total_revenue = (
        orders.aggregate(
            Sum("total_amount")
        )["total_amount__sum"] or 0
    )


    pending_orders = orders.filter(
        status="Pending"
    ).count()


    recent_reviews = Review.objects.filter(
        restaurant=restaurant
    ).order_by("-created_at")[:5]


    today = date.today()


    today_orders = orders.filter(
        created_at__date=today
    )


    today_orders_count = today_orders.count()


    today_revenue = (
        today_orders.aggregate(
            Sum("total_amount")
        )["total_amount__sum"] or 0
    )
    total_reviews = Review.objects.filter(
        restaurant=restaurant
    ).count()


    average_rating = restaurant.rating


    best_selling_food = (
        FoodItem.objects.filter(
            restaurant=restaurant
        )
        .annotate(
            total_sold=Count("orderitem")
        )
        .order_by("-total_sold")
        .first()
    )


    context = {
        "restaurant": restaurant,
        "total_foods": total_foods,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "pending_orders": pending_orders,
        "recent_reviews": recent_reviews,
        "today_orders": today_orders_count,
        "today_revenue": today_revenue,
        "total_reviews": total_reviews,
        "average_rating": average_rating,
        "best_selling_food": best_selling_food,
    }


    return render(
        request,
        "restaurant/dashboard.html",
        context
    )



@restaurant_owner_required
def add_food(request):

    if request.method == "POST":

        form = FoodForm(
            request.POST,
            request.FILES
        )


        if form.is_valid():

            food = form.save(commit=False)


            restaurant = get_object_or_404(
                Restaurant,
                owner=request.user
            )


            food.restaurant = restaurant

            food.save()


            messages.success(
                request,
                "Food added successfully."
            )


            return redirect(
                "restaurant_dashboard"
            )


    else:

        form = FoodForm()


    context = {
        "form": form
    }


    return render(
        request,
        "restaurant/add_food.html",
        context
    )



@restaurant_owner_required
def view_foods(request):

    restaurant = get_object_or_404(
        Restaurant,
        owner=request.user
    )


    foods = FoodItem.objects.filter(
        restaurant=restaurant
    )


    context = {
        "foods": foods
    }


    return render(
        request,
        "restaurant/view_foods.html",
        context
    )



@restaurant_owner_required
def edit_food(request, id):

    food = get_object_or_404(
        FoodItem,
        id=id,
        restaurant__owner=request.user
    )


    if request.method == "POST":

        form = FoodForm(
            request.POST,
            request.FILES,
            instance=food
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "Food updated successfully."
            )


            return redirect(
                "view_foods"
            )


    else:

        form = FoodForm(
            instance=food
        )


    context = {
        "form": form
    }


    return render(
        request,
        "restaurant/edit_food.html",
        context
    )



@restaurant_owner_required
def delete_food(request, id):

    food = get_object_or_404(
        FoodItem,
        id=id,
        restaurant__owner=request.user
    )


    food.delete()


    messages.success(
        request,
        "Food deleted successfully."
    )


    return redirect(
        "view_foods"
    )



@restaurant_owner_required
def toggle_stock(request, id):

    food = get_object_or_404(
        FoodItem,
        id=id,
        restaurant__owner=request.user
    )


    food.is_available = not food.is_available

    food.save()


    messages.success(
        request,
        "Food stock status updated successfully."
    )


    return redirect(
        "view_foods"
    )



@restaurant_owner_required
def customer_orders(request):

    restaurant = get_object_or_404(
        Restaurant,
        owner=request.user
    )


    orders = (
        Order.objects.filter(
            orderitem__food__restaurant=restaurant
        )
        .distinct()
        .order_by("-created_at")
    )


    context = {
        "orders": orders
    }


    return render(
        request,
        "restaurant/customer_orders.html",
        context
    )


@restaurant_owner_required
def update_order_status(request, id):

    order = get_object_or_404(
        Order.objects.filter(
            orderitem__food__restaurant__owner=request.user
        ).distinct(),
        id=id
    )

    if request.method == "POST":

        order.status = request.POST.get("status")
        order.save()

        messages.success(
            request,
            "Order status updated successfully."
        )

    return redirect("customer_orders")


@restaurant_owner_required
def toggle_restaurant_status(request):

    restaurant = get_object_or_404(
        Restaurant,
        owner=request.user
    )


    restaurant.is_open = not restaurant.is_open

    restaurant.save()


    messages.success(
        request,
        "Restaurant status updated successfully."
    )


    return redirect(
        "restaurant_status"
    )



@restaurant_owner_required
def restaurant_status(request):

    restaurant = get_object_or_404(
        Restaurant,
        owner=request.user
    )


    context = {
        "restaurant": restaurant
    }


    return render(
        request,
        "restaurant/restaurant_status.html",
        context
    )



@restaurant_owner_required
def restaurant_profile(request):

    restaurant = get_object_or_404(
        Restaurant,
        owner=request.user
    )


    if request.method == "POST":

        form = RestaurantProfileForm(
            request.POST,
            request.FILES,
            instance=restaurant
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "Restaurant profile updated successfully."
            )


            return redirect(
                "restaurant_profile"
            )


    else:

        form = RestaurantProfileForm(
            instance=restaurant
        )


    context = {
        "form": form
    }


    return render(
        request,
        "restaurant/restaurant_profile.html",
        context
    )
