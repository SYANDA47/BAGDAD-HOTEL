from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total_price']
    
    def get_total_price(self, obj):
        return f"KSh {obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_phone', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_phone', 'customer_email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'user')
        }),
        ('Order Details', {
            'fields': ('status', 'table_number', 'total_amount', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'get_item_name', 'quantity', 'weight_kg', 'unit_price', 'get_total_price']
    list_filter = ['order__status', 'order__created_at']
    
    def get_item_name(self, obj):
        return obj.get_item_name()
    get_item_name.short_description = 'Item'
    
    def get_total_price(self, obj):
        return f"KSh {obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'get_total_items', 'get_total_price', 'created_at']
    list_filter = ['created_at']
    inlines = [CartItemInline]
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'
    
    def get_total_price(self, obj):
        return f"KSh {obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'get_item_name', 'quantity', 'weight_kg', 'get_total_price']
    list_filter = ['created_at']
    
    def get_item_name(self, obj):
        return obj.get_item_name()
    get_item_name.short_description = 'Item'
    
    def get_total_price(self, obj):
        return f"KSh {obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'
