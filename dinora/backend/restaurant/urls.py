from django.urls import path
from . import views

urlpatterns = [

    # ==========================================
    # Authentication
    # ==========================================

    path('login/', views.restaurant_login, name='restaurant_login'),

    # ==========================================
    # Dashboard
    # ==========================================

    path('dashboard/', views.dashboard, name='restaurant_dashboard'),

    # ==========================================
    # Food Management
    # ==========================================

    path('add-food/', views.add_food, name='add_food'),
    path('view-foods/', views.view_foods, name='view_foods'),
    path('edit-food/<int:id>/', views.edit_food, name='edit_food'),
    path('delete-food/<int:id>/', views.delete_food, name='delete_food'),
    path('toggle-stock/<int:id>/', views.toggle_stock, name='toggle_stock'),

    # ==========================================
    # Order Management
    # ==========================================

    path('customer-orders/', views.customer_orders, name='customer_orders'),
    path('update-order-status/<int:id>/', views.update_order_status, name='update_order_status'),

    # ==========================================
    # Restaurant Management
    # ==========================================

    path('restaurant-status/', views.restaurant_status, name='restaurant_status'),
    path('toggle-restaurant-status/', views.toggle_restaurant_status, name='toggle_restaurant_status'),
    path('restaurant-profile/', views.restaurant_profile, name='restaurant_profile'),

]