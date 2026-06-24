from django.contrib import admin
from .models import Restaurant,Category,FoodItem,Cart,CartItem, Order, OrderItem
# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(FoodItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)