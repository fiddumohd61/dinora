from django.db.models import Avg,Q
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, FoodItem, Cart, CartItem, Order, OrderItem, Review
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from accounts.decorators import customer_required
from django.contrib.auth.models import User


@customer_required
def home(request):

    context = {
        "total_orders": Order.objects.count(),
        "total_customers": User.objects.count(),
        "total_restaurants": Restaurant.objects.count(),
        "average_delivery": 30,
    }

    return render(request, "foodapp/index.html", context)

@customer_required
def menu(request):
    query = request.GET.get("q")

    if query:
        foods = FoodItem.objects.filter(name__icontains=query)
    else:
        foods = FoodItem.objects.all()

    context = {"foods": foods}

    return render(request, "foodapp/menu.html", context)

@customer_required
def search(request):

    query = request.GET.get("q", "")

    restaurants = Restaurant.objects.filter(
        name__icontains=query
    )

    foods = FoodItem.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )

    context = {
        "query": query,
        "restaurants": restaurants,
        "foods": foods,
    }

    return render(
        request,
        "foodapp/search_results.html",
        context
    )
@customer_required
def about(request):
    return render(request, "foodapp/about.html")

@customer_required
def contact(request):
    return render(request, "foodapp/contact.html")
@customer_required
def restaurants(request):

    restaurant_list = Restaurant.objects.all()

    context = {
        "restaurants": restaurant_list,
    }

    return render(
        request,
        "foodapp/restaurants.html",
        context
    )

@customer_required
def restaurant_detail(request, id):

    restaurant = get_object_or_404(Restaurant, id=id)

    foods = FoodItem.objects.filter(restaurant=restaurant)

    reviews = Review.objects.filter(restaurant=restaurant).order_by("-created_at")
    review_count = reviews.count()
    context = {
        "restaurant": restaurant,
        "foods": foods,
        "reviews": reviews,
        "review_count": review_count,
    }

    return render(request, "foodapp/restaurant_detail.html", context)

@customer_required
def offers(request):
    return render(request, "foodapp/offers.html")

@customer_required
@login_required(login_url="login")
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)
    total = 0

    for item in cart_items:
        total += item.food.price * item.quantity

    context = {
        "cart_items": cart_items,
        "total": total,
    }
    return render(request, "foodapp/cart.html", context)

@customer_required
@login_required(login_url="login")
def add_to_cart(request, food_id):

    food = get_object_or_404(FoodItem, id=food_id)

    # ==========================================
    # Check Food Availability
    # ==========================================

    if not food.is_available:
        messages.error(request, "This item is currently out of stock.")

        return redirect("restaurant_detail", id=food.restaurant.id)
    # ==========================================
    # Check Restaurant Status
    # ==========================================

    if not food.restaurant.is_open:
        messages.error(request, "This restaurant is currently closed.")

        return redirect("restaurant_detail", id=food.restaurant.id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, food=food)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")

@customer_required
@login_required(login_url="login")
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()

    return redirect("cart")

@customer_required
@login_required(login_url="login")
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart")

@customer_required
@login_required(login_url="login")
def remove_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()

    return redirect("cart")

@customer_required
@login_required(login_url="login")
def place_order(request):

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total = 0

    for item in cart_items:
        total += item.food.price * item.quantity

    order = Order.objects.create(user=request.user, total_amount=total)

    for item in cart_items:
        OrderItem.objects.create(order=order, food=item.food, quantity=item.quantity)

    cart_items.delete()

    return redirect("order_success")

@customer_required
@login_required(login_url="login")
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    context = {
        "orders": orders,
    }

    return render(request, "foodapp/order_history.html", context)
@customer_required
@login_required(login_url='login')
def order_details(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order_items = OrderItem.objects.filter(
        order=order
    )

    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(
        request,
        'foodapp/order_details.html',
        context
    )
@customer_required
@login_required(login_url="login")
def checkout(request):
    return render(request, "foodapp/checkout.html")

@customer_required
@login_required(login_url="login")
def order_success(request):
    return render(request, "foodapp/order_success.html")

@customer_required
@login_required(login_url='login')
def write_review(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
        status="Delivered"
    )

    if Review.objects.filter(order=order).exists():
        messages.info(request, "You have already reviewed this order.")
        return redirect("order_history")

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.order = order
            review.user = request.user
            review.restaurant = order.orderitem_set.first().food.restaurant

            review.save()

            # ==========================================
            # Update Restaurant Rating
            # ==========================================

            restaurant = review.restaurant

            average_rating = Review.objects.filter(
                restaurant=restaurant
            ).aggregate(
                Avg('rating')
            )['rating__avg']

            restaurant.rating = round(average_rating, 1)

            restaurant.save()

            messages.success(request, "Review submitted successfully!")

            return redirect("order_history")

    else:

        form = ReviewForm()

    context = {
        "form": form,
        "order": order
    }

    return render(
        request,
        "foodapp/write_review.html",
        context
    )
