from django.contrib import admin
from .models import (
    Restaurant,
    Category,
    FoodItem,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Review,
    Offer,
    Food
)




# ==========================================
# Restaurant
# ==========================================

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'owner',
        'rating',
        'is_open'
    )

    search_fields = (
        'name',
        'owner__username'
    )

    list_filter = (
        'is_open',
    )


# ==========================================
# Category
# ==========================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
    )

    search_fields = (
        'name',
    )


# ==========================================
# Food Item
# ==========================================

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'restaurant',
        'category',
        'price',
        'is_available'
    )

    list_filter = (
        'restaurant',
        'category',
        'is_available'
    )

    search_fields = (
        'name',
        'restaurant__name'
    )


# ==========================================
# Cart
# ==========================================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
    )

    search_fields = (
        'user__username',
    )


# ==========================================
# Cart Item
# ==========================================

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        'cart',
        'food',
        'quantity',
    )

    list_filter = (
        'food',
    )


# ==========================================
# Order
# ==========================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'total_amount',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'created_at'
    )

    search_fields = (
        'user__username',
    )


# ==========================================
# Order Item
# ==========================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'order',
        'food',
        'quantity',
    )


# ==========================================
# Review
# ==========================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'restaurant',
        'rating',
        'created_at'
    )

    list_filter = (
        'rating',
    )

    search_fields = (
        'user__username',
        'restaurant__name'
    )


# ==========================================
# Offer
# ==========================================

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'description',
        'coupon_code',
        'is_active'
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'title',
        'coupon_code',
    )

# ==========================================
# Food
# ==========================================

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'price',
        'is_popular'
    ]

    list_filter = [
        'is_popular'
    ]