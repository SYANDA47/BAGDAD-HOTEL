from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Cart management
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    
    # Checkout and orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/confirmation/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Add order list for staff/admin
    path('', views.order_list, name='order_list'),
]