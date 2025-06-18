from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone_number', 'get_loyalty_points')
    list_filter = UserAdmin.list_filter + ('userprofile__newsletter_subscription',)
    
    def get_phone_number(self, obj):
        return obj.userprofile.phone_number if hasattr(obj, 'userprofile') else ''
    get_phone_number.short_description = 'Phone Number'
    
    def get_loyalty_points(self, obj):
        return obj.userprofile.loyalty_points if hasattr(obj, 'userprofile') else 0
    get_loyalty_points.short_description = 'Loyalty Points'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'preferred_contact', 'loyalty_points', 'newsletter_subscription']
    list_filter = ['preferred_contact', 'newsletter_subscription', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
