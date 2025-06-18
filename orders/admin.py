from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem, Cart, CartItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'customer_name', 
        'table_number', 
        'total_amount', 
        'status_badge', 
        'created_at',
        'view_details_link'
    ]
    list_filter = [
        'status', 
        'created_at', 
        'table_number',
        'user'
    ]
    search_fields = [
        'customer_name', 
        'customer_phone', 
        'customer_email',
        'id'
    ]
    readonly_fields = [
        'created_at', 
        'updated_at',
        'total_amount_display',
        'order_items_display'
    ]
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_phone', 'customer_email', 'user')
        }),
        ('Order Details', {
            'fields': ('table_number', 'status', 'notes', 'total_amount_display')
        }),
        ('Order Items', {
            'fields': ('order_items_display',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'preparing': '#17a2b8',
            'ready': '#28a745',
            'completed': '#6f42c1',
            'cancelled': '#dc3545'
        }
        status = getattr(obj, 'status', 'pending')
        color = colors.get(status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display() if hasattr(obj, 'get_status_display') else status.title()
        )
    status_badge.short_description = 'Status'
    
    def total_amount_display(self, obj):
        return f"${obj.total_amount}"
    total_amount_display.short_description = 'Total Amount'
    
    def view_details_link(self, obj):
        url = reverse('orders:order_detail', args=[obj.id])
        return format_html('<a href="{}" target="_blank">View Details</a>', url)
    view_details_link.short_description = 'Actions'
    
    def order_items_display(self, obj):
        items = obj.items.all()
        if not items:
            return "No items"
        
        html = "<table style='width: 100%; border-collapse: collapse;'>"
        html += "<tr style='background-color: #f8f9fa;'><th style='padding: 8px; border: 1px solid #ddd;'>Item</th><th style='padding: 8px; border: 1px solid #ddd;'>Quantity/Weight</th><th style='padding: 8px; border: 1px solid #ddd;'>Price</th><th style='padding: 8px; border: 1px solid #ddd;'>Total</th></tr>"
        
        for item in items:
            item_name = ""
            quantity_info = ""
            
            if item.beer:
                item_name = f"🍺 {item.beer.name}"
                quantity_info = f"{item.quantity} bottles"
            elif item.nyama_choma:
                item_name = f"🥩 {item.nyama_choma.name}"
                quantity_info = f"{item.weight_kg}kg"
            
            total_price = getattr(item, 'get_total_price', lambda: item.unit_price * (item.quantity or 1))()
            
            html += f"<tr><td style='padding: 8px; border: 1px solid #ddd;'>{item_name}</td>"
            html += f"<td style='padding: 8px; border: 1px solid #ddd;'>{quantity_info}</td>"
            html += f"<td style='padding: 8px; border: 1px solid #ddd;'>${item.unit_price}</td>"
            html += f"<td style='padding: 8px; border: 1px solid #ddd;'>${total_price}</td></tr>"
        
        html += "</table>"
        return mark_safe(html)
    order_items_display.short_description = 'Order Items'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'order', 
        'get_item_name', 
        'quantity', 
        'weight_kg', 
        'unit_price', 
        'get_total_price'
    ]
    list_filter = ['order__status', 'beer', 'nyama_choma']
    search_fields = ['order__id', 'beer__name', 'nyama_choma__name']
    
    def get_item_name(self, obj):
        if obj.beer:
            return f"🍺 {obj.beer.name}"
        elif obj.nyama_choma:
            return f"🥩 {obj.nyama_choma.name}"
        return "Unknown Item"
    get_item_name.short_description = 'Item'
    
    def get_total_price(self, obj):
        if hasattr(obj, 'get_total_price'):
            return f"${obj.get_total_price()}"
        return f"${obj.unit_price * (obj.quantity or 1)}"
    get_total_price.short_description = 'Total Price'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'user', 
        'session_key', 
        'get_total_items', 
        'get_total_price', 
        'created_at'
    ]
    list_filter = ['created_at', 'user']
    search_fields = ['user__username', 'session_key']
    readonly_fields = ['created_at', 'updated_at', 'cart_items_display']
    
    def cart_items_display(self, obj):
        items = obj.items.all()
        if not items:
            return "Empty cart"
        
        html = "<ul>"
        for item in items:
            if item.beer:
                html += f"<li>🍺 {item.beer.name} - {item.quantity} bottles</li>"
            elif item.nyama_choma:
                html += f"<li>🥩 {item.nyama_choma.name} - {item.weight_kg}kg</li>"
        html += "</ul>"
        return mark_safe(html)
    cart_items_display.short_description = 'Cart Items'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        'cart', 
        'get_item_name', 
        'quantity', 
        'weight_kg', 
        'get_unit_price'
    ]
    list_filter = ['beer', 'nyama_choma', 'cart__user']
    search_fields = ['cart__user__username', 'beer__name', 'nyama_choma__name']
    
    def get_item_name(self, obj):
        if obj.beer:
            return f"🍺 {obj.beer.name}"
        elif obj.nyama_choma:
            return f"🥩 {obj.nyama_choma.name}"
        return "Unknown Item"
    get_item_name.short_description = 'Item'
    
    def get_unit_price(self, obj):
        if hasattr(obj, 'get_unit_price'):
            return f"${obj.get_unit_price()}"
        return "N/A"
    get_unit_price.short_description = 'Unit Price'

# Customize admin site headers
admin.site.site_header = "🍺 Bar Management System"
admin.site.site_title = "Bar Admin"
admin.site.index_title = "Welcome to Bar Management Dashboard"