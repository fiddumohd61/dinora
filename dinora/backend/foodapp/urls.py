from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    
    path('checkout/', views.checkout, name='checkout'),
    path('restaurants/', views.restaurants, name='restaurants'),

    
    path('offers/', views.offers, name='offers'),


    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:item_id>/', views.remove_item, name='remove_item'),

    path('place-order/', views.place_order, name='place_order'),

    path('checkout/', views.checkout, name='checkout'),
    path('order-success/',views.order_success,name='order_success'),
    path('order-history/', views.order_history, name='order_history'),
   
    path('restaurant/<int:id>/', views.restaurant_detail, name='restaurant_detail'),
]