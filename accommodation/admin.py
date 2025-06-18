from django.contrib import admin
from django.utils.html import format_html
from .models import RoomType, Room, Booking

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price', 'max_occupancy']
    search_fields = ['name', 'description']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'is_available', 'image_preview']
    list_filter = ['room_type', 'is_available']
    search_fields = ['room_number', 'amenities']
    list_editable = ['is_available']
    readonly_fields = ['image_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('room_number', 'room_type', 'is_available')
        }),
        ('Details', {
            'fields': ('amenities',),
            'description': 'List the amenities available in this room (e.g., WiFi, TV, AC, etc.)'
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload a high-quality image of the room (recommended size: 1200x800px)'
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 150px; height: 100px; object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'guest_name', 'room', 'check_in_date', 'check_out_date', 'status', 'total_price']
    list_filter = ['status', 'check_in_date', 'room__room_type']
    search_fields = ['guest_name', 'guest_email', 'guest_phone']
    list_editable = ['status']
    readonly_fields = ['created_at', 'total_price']
    date_hierarchy = 'check_in_date'
    
    fieldsets = (
        ('Guest Information', {
            'fields': ('guest_name', 'guest_email', 'guest_phone')
        }),
        ('Booking Details', {
            'fields': ('room', 'check_in_date', 'check_out_date', 'guests_count', 'status')
        }),
        ('Pricing', {
            'fields': ('total_price',),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('special_requests', 'created_at'),
            'classes': ('collapse',)
        }),
    )
