from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from decimal import Decimal
from .models import Order, OrderItem, Cart, CartItem
from bar_app.models import Beer, NyamaChoma, Table
import json

def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

@require_POST
def add_to_cart(request):
    """Add item to cart via AJAX"""
    try:
        data = json.loads(request.body)
        item_type = data.get('type')  # 'beer' or 'nyama'
        item_id = data.get('id')
        quantity = int(data.get('quantity', 1))
        weight_kg = data.get('weight_kg')
        notes = data.get('notes', '')
        
        cart = get_or_create_cart(request)
        
        if item_type == 'beer':
            beer = get_object_or_404(Beer, id=item_id, in_stock=True)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                beer=beer,
                defaults={'quantity': quantity, 'notes': notes}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
        elif item_type == 'nyama':
            nyama = get_object_or_404(NyamaChoma, id=item_id, available=True)
            if not weight_kg:
                return JsonResponse({'success': False, 'message': 'Weight is required for nyama choma'})
            
            weight_kg = Decimal(str(weight_kg))  # Convert to Decimal
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                nyama_choma=nyama,
                defaults={'quantity': 1, 'weight_kg': weight_kg, 'notes': notes}
            )
            if not created:
                cart_item.weight_kg += weight_kg
                cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Item added to cart!',
            'cart_total': cart.get_total_items()
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def view_cart(request):
    """Display cart contents"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    subtotal = cart.get_total_price()
    service_charge = subtotal * Decimal('0.1')  # 10% service charge using Decimal
    total_price = subtotal + service_charge
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'service_charge': service_charge,
        'total_price': total_price,
        'total_items': cart.get_total_items(),
    }
    return render(request, 'orders/cart.html', context)

@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity/weight"""
    try:
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        action = request.POST.get('action')
        
        if action == 'increase':
            if cart_item.beer:
                cart_item.quantity += 1
            elif cart_item.nyama_choma:
                cart_item.weight_kg += Decimal('0.5')  # Use Decimal
        elif action == 'decrease':
            if cart_item.beer:
                cart_item.quantity = max(1, cart_item.quantity - 1)
            elif cart_item.nyama_choma:
                cart_item.weight_kg = max(Decimal('0.5'), cart_item.weight_kg - Decimal('0.5'))  # Use Decimal
        elif action == 'remove':
            cart_item.delete()
            messages.success(request, 'Item removed from cart')
            return redirect('orders:view_cart')
        
        cart_item.save()
        messages.success(request, 'Cart updated successfully')
        
    except Exception as e:
        messages.error(request, f'Error updating cart: {str(e)}')
    
    return redirect('orders:view_cart')

def checkout(request):
    """Checkout process"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty')
        return redirect('orders:view_cart')
    
    subtotal = cart.get_total_price()
    service_charge = subtotal * Decimal('0.1')  # Use Decimal
    total_price = subtotal + service_charge
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    customer_name=request.POST.get('customer_name'),
                    customer_phone=request.POST.get('customer_phone'),
                    customer_email=request.POST.get('customer_email'),
                    table_number=request.POST.get('table_number') or None,
                    notes=request.POST.get('notes', ''),
                    user=request.user if request.user.is_authenticated else None,
                    total_amount=total_price
                )
                
                # Create order items from cart
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        beer=cart_item.beer,
                        nyama_choma=cart_item.nyama_choma,
                        quantity=cart_item.quantity,
                        weight_kg=cart_item.weight_kg,
                        unit_price=cart_item.get_unit_price(),
                        notes=cart_item.notes
                    )
                
                # Clear cart
                cart_items.delete()
                
                messages.success(request, f'Order #{order.id} placed successfully!')
                return redirect('orders:order_confirmation', order_id=order.id)
                
        except Exception as e:
            messages.error(request, f'Error placing order: {str(e)}')
    
    # Get available tables
    available_tables = Table.objects.filter(is_reserved=False)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'service_charge': service_charge,
        'total_price': total_price,
        'available_tables': available_tables,
    }
    return render(request, 'orders/checkout.html', context)

def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id)
    
    # Only allow access to order owner or staff
    if request.user.is_authenticated:
        if order.user != request.user and not request.user.is_staff:
            messages.error(request, 'You can only view your own orders')
            return redirect('bar_app:home')
    
    context = {'order': order}
    return render(request, 'orders/order_confirmation.html', context)

@login_required
def my_orders(request):
    """User's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'orders/my_orders.html', context)

def order_list(request):
    """List all orders - for staff/admin dashboard"""
    orders = Order.objects.all().order_by('-created_at')
    
    # Add pagination for better performance
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': orders,
        'page_obj': page_obj
    }
    return render(request, 'orders/order_list.html', context)

def order_detail(request, order_id):
    """Detailed view of a specific order"""
    order = get_object_or_404(Order, id=order_id)
    
    # Allow access to order owner or staff
    # Remove login_required to allow staff access without forcing login
    if request.user.is_authenticated:
        if order.user != request.user and not request.user.is_staff:
            messages.error(request, 'You can only view your own orders')
            return redirect('orders:my_orders')
    
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)

def clear_cart(request):
    """Clear all items from cart"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared successfully')
    return redirect('orders:view_cart')