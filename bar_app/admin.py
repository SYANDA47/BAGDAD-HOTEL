from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Beer, NyamaChoma, Table, Reservation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'beer_type', 'price', 'in_stock', 'image_preview']
    list_filter = ['beer_type', 'in_stock', 'category']
    search_fields = ['name', 'brand', 'description']
    list_editable = ['price', 'in_stock']
    readonly_fields = ['image_preview', 'created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'brand', 'beer_type', 'category')
        }),
        ('Details', {
            'fields': ('description', 'alcohol_content', 'price', 'in_stock')
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload a high-quality image of the beer (recommended size: 800x600px)'
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"

@admin.register(NyamaChoma)
class NyamaChomaAdmin(admin.ModelAdmin):
    list_display = ['name', 'meat_type', 'price_per_kg', 'spice_level', 'available', 'image_preview']
    list_filter = ['meat_type', 'available', 'spice_level']
    search_fields = ['name', 'description']
    list_editable = ['price_per_kg', 'available']
    readonly_fields = ['image_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'meat_type', 'spice_level')
        }),
        ('Details', {
            'fields': ('description', 'price_per_kg', 'available')
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload a high-quality image of the nyama choma (recommended size: 800x600px)'
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number', 'capacity', 'location', 'is_reserved']
    list_filter = ['location', 'is_reserved']
    list_editable = ['is_reserved']
    ordering = ['table_number']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'table', 'date', 'time', 'party_size', 'created_at']
    list_filter = ['date', 'table__location', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Reservation Details', {
            'fields': ('table', 'date', 'time', 'party_size')
        }),
        ('Additional Information', {
            'fields': ('special_requests', 'created_at'),
            'classes': ('collapse',)
        }),
    )
