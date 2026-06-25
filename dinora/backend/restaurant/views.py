from django.shortcuts import render, redirect,get_object_or_404
from .forms import FoodForm,FoodItem
from foodapp.models import Order,FoodItem
from django.db.models import Sum
def dashboard(request):

    total_foods = FoodItem.objects.count()

    total_orders = Order.objects.count()

    total_revenue = Order.objects.aggregate(
        Sum('total_amount')
    )['total_amount__sum'] or 0

    pending_orders = Order.objects.filter(
        status='Pending'
    ).count()

    context = {

        'total_foods': total_foods,

        'total_orders': total_orders,

        'total_revenue': total_revenue,

        'pending_orders': pending_orders,

    }

    return render(
        request,
        'restaurant/dashboard.html',
        context
    )
def add_food(request):

    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('restaurant_dashboard')

    else:
        form = FoodForm()

    context = {
        'form': form
    }

    return render(request, 'restaurant/add_food.html', context)


def view_foods(request):

    foods = FoodItem.objects.all()

    context = {
        'foods': foods
    }

    return render(request, 'restaurant/view_foods.html', context)

def edit_food(request, id):

    food = get_object_or_404(FoodItem, id=id)

    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES, instance=food)

        if form.is_valid():
            form.save()
            return redirect('view_foods')

    else:
        form = FoodForm(instance=food)

    context = {
        'form': form
    }

    return render(request, 'restaurant/edit_food.html', context)

def delete_food(request, id):

    food = get_object_or_404(FoodItem, id=id)

    food.delete()

    return redirect('view_foods')

def toggle_stock(request, id):

    food = get_object_or_404(FoodItem, id=id)

    food.is_available = not food.is_available

    food.save()

    return redirect('view_foods')

def customer_orders(request):

    orders = Order.objects.all().order_by('-created_at')

    context = {
        'orders': orders
    }

    return render(
        request,
        'restaurant/customer_orders.html',
        context
    )

def update_order_status(request, id):

    order = get_object_or_404(Order, id=id)

    if request.method == "POST":

        order.status = request.POST.get('status')

        order.save()

    return redirect('customer_orders')