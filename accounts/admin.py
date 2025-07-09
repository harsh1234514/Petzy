from django.contrib import admin
from .models import UserProfile, Address


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'country', 'created_at']
    list_filter = ['country', 'email_notifications', 'newsletter_subscription']
    search_fields = ['user__username', 'user__email', 'phone']
    ordering = ['-created_at']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'city', 'state', 'country', 'is_default']
    list_filter = ['country', 'state', 'is_default']
    search_fields = ['user__username', 'title', 'city']
    ordering = ['-created_at']
