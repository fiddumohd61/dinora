from django.urls import path
from . import views

urlpatterns = [
                path('dashboard/', views.dashboard, name='restaurant_dashboard'),
                path('add-food/', views.add_food, name='add_food'),
                path('view-foods/', views.view_foods, name='view_foods'),
                path('edit-food/<int:id>/', views.edit_food, name='edit_food'),
                path('delete-food/<int:id>/', views.delete_food, name='delete_food'),
                path('toggle-stock/<int:id>/', views.toggle_stock, name='toggle_stock'),
                path('customer-orders/',views.customer_orders,name='customer_orders'),
                path('update-order-status/<int:id>/',views.update_order_status,name='update_order_status'),
]