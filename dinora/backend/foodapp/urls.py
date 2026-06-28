from django.urls import path
from . import views

urlpatterns = [

    # ==========================================
    # Home Pages
    # ==========================================

    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('offers/', views.offers, name='offers'),

    # ==========================================
    # Restaurant
    # ==========================================

    path('restaurants/', views.restaurants, name='restaurants'),
    path('restaurant/<int:id>/', views.restaurant_detail, name='restaurant_detail'),

    # ==========================================
    # Cart
    # ==========================================

    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:item_id>/', views.remove_item, name='remove_item'),

    # ==========================================
    # Orders
    # ==========================================

    path('checkout/', views.checkout, name='checkout'),
    path("clear-cart/",views.clear_cart,name="clear_cart"),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('order-history/', views.order_history, name='order_history'),
    path('order-details/<int:order_id>/',views.order_details,name='order_details'),

    # ==========================================
    # Reviews
    # ==========================================

    path('write-review/<int:order_id>/', views.write_review, name='write_review'),
    
    
    path("partner/",views.partner,name="partner"),

]