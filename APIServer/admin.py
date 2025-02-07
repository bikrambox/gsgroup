# myapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import APIKey

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_api_keys')
    
    def get_api_keys(self, obj):
        api_keys = obj.api_keys.filter(is_active=True)
        if not api_keys:
            return '-'
        
        key_list = []
        for key in api_keys:
            key_list.append(f'{key.name}')
        
        return format_html('Available')
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        user = self.get_object(request, object_id)
        if user:
            api_keys = user.api_keys.filter(is_active=True)
            api_key_details = [{'name': key.name, 'key': key.key} for key in api_keys]
            extra_context['api_keys'] = api_key_details
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context)
    
    get_api_keys.short_description = 'API Keys'
    get_api_keys.allow_tags = True

# Unregister the default UserAdmin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'key', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'user')
    search_fields = ('name', 'key', 'user__username')
    readonly_fields = ('key', 'created_at')
    ordering = ('-created_at',)
    actions = ['toggle_active']

    def toggle_active(self, request, queryset):
        for api_key in queryset:
            api_key.is_active = not api_key.is_active
            api_key.save()
    toggle_active.short_description = "Toggle active status for selected API keys"