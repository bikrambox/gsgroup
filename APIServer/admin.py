# APIServer/admin.py
from django import forms
from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.contrib.auth.forms import AuthenticationForm
from .models import APIKey, UploadedFile, NomecoDelivery, NovonordisDelivery

class EmailAuthenticationForm(AuthenticationForm):
    """
    Custom admin login form to use email instead of username.
    """
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean(self):
        email = self.cleaned_data.get('username')  # 'username' field is now email
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': 'email'},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class UserAdminForm(forms.ModelForm):
    """
    Custom form for User admin to enforce case-insensitive email uniqueness.
    """
    class Meta:
        model = User
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check for existing emails in a case-insensitive manner
            qs = User.objects.filter(email__iexact=email)
            if self.instance.pk:  # If editing an existing user, exclude the current user
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("A user with this email already exists.")
        return email

class CustomUserAdmin(UserAdmin):
    form = UserAdminForm  # Use the custom form to enforce email uniqueness
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'get_api_keys')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')

    # Define fieldsets for the change form (includes "Change password" and other details)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Define add_fieldsets for the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

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

class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_email', 'key', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'user')
    search_fields = ('name', 'key', 'user__email')
    readonly_fields = ('key', 'created_at')
    ordering = ('-created_at',)
    actions = ['toggle_active']

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def toggle_active(self, request, queryset):
        for api_key in queryset:
            api_key.is_active = not api_key.is_active
            api_key.save()
    toggle_active.short_description = "Toggle active status for selected API keys"

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'user', 'uploaded_at', 'file_size')
    list_filter = ('uploaded_at',)
    search_fields = ('filename', 'user__email')

class NomecoDeliveryAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer_name', 'waybill_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'customer_name', 'waybill_number')

class NovonordisDeliveryAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer_name', 'waybill_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'customer_name', 'waybill_number')

# Unregister the default UserAdmin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register other models
admin.site.register(APIKey, APIKeyAdmin)
admin.site.register(UploadedFile, UploadedFileAdmin)
admin.site.register(NomecoDelivery, NomecoDeliveryAdmin)
admin.site.register(NovonordisDelivery, NovonordisDeliveryAdmin)

# Set the custom authentication form for admin login
admin.site.login_form = EmailAuthenticationForm
admin.site.login_template = 'admin/login.html'