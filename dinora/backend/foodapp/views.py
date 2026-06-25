from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from .models import Restaurant,FoodItem,Cart,CartItem,Order, OrderItem
from django.contrib.auth.decorators import login_required


def home(request):
    restaurants = Restaurant.objects.all()
    foods = FoodItem.objects.all()

    context = {
        'restaurants': restaurants,
        'foods': foods,
    }

    return render(request, 'foodapp/index.html', context)

def menu(request):
    query = request.GET.get('q')

    if query:
        foods = FoodItem.objects.filter(name__icontains=query)
    else:
        foods = FoodItem.objects.all()

    context = {
        'foods': foods
    }

    return render(request, 'foodapp/menu.html', context)

def about(request):
    return render(request, 'foodapp/about.html')

def contact(request):
    return render(request, 'foodapp/contact.html')







def restaurants(request):
    restaurant_list = Restaurant.objects.all()
    return render(request, 'foodapp/restaurants.html', {
        'restaurants': restaurant_list
    })
def restaurant_detail(request, id):
    restaurant = Restaurant.objects.get(id=id)
    foods = FoodItem.objects.filter(restaurant=restaurant)

    context = {
        'restaurant': restaurant,
        'foods': foods,
    }

    return render(request, 'foodapp/restaurant_detail.html', context)


def offers(request):
    return render(request, 'foodapp/offers.html')

@login_required(login_url='login')
def cart(request):
    cart = Cart.objects.get(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)
    total = 0

    for item in cart_items:
        total += item.food.price * item.quantity
        
    context = {
    'cart_items': cart_items,
    'total': total,
    }
    return render(request, 'foodapp/cart.html', context)

@login_required(login_url='login')
def add_to_cart(request, food_id):

    food = get_object_or_404(FoodItem, id=food_id)

    # ==========================================
    # Check Food Availability
    # ==========================================

    if not food.is_available:
        messages.error(request, "This item is currently out of stock.")

        return redirect('restaurant_detail', id=food.restaurant.id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        food=food
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required(login_url='login')
def increase_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

@login_required(login_url='login')
def decrease_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

@login_required(login_url='login')
def remove_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()

    return redirect('cart')

@login_required(login_url='login')
def place_order(request):

    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total = 0

    for item in cart_items:
        total += item.food.price * item.quantity

    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            food=item.food,
            quantity=item.quantity
        )

    cart_items.delete()

    return redirect('order_success')

@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders,
    }

    return render(request, 'foodapp/order_history.html', context)

def checkout(request):
    return render(request, 'foodapp/checkout.html')
def order_success(request):
    return render(request,'foodapp/order_success.html')
