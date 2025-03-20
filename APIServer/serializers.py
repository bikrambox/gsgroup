"""
Serializers for API data transformation and validation.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import APIKey, NomecoDelivery, NovonordisDelivery
from .utils.crypto import CryptoUtils

class EncryptedCharField(serializers.CharField):
    """Custom field that encrypts data before saving and decrypts when reading"""
    
    def to_internal_value(self, data):
        # Encrypt data before saving
        return CryptoUtils.encrypt_data(data)

    def to_representation(self, value):
        # Decrypt data when reading
        try:
            return CryptoUtils.decrypt_data(value)
        except ValueError:
            return value  # Return as is if decryption fails

class UserSerializer(serializers.ModelSerializer):
    password = EncryptedCharField(write_only=True)
    email = EncryptedCharField(required=True)
    
    class Meta:
        model = User
        # fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'is_active',      # Include is_active
            'is_staff',      # Include is_staff
            'is_superuser',  # Include is_superuser
            'date_joined',   # Include date_joined
            'last_login',    # Include last_login
        ]
        read_only_fields = ['is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        decrypted_email = CryptoUtils.decrypt_data(value)
        if not decrypted_email:  # Prevent empty emails
            raise serializers.ValidationError("Email cannot be empty.")
        # Check for existing emails in a case-insensitive manner
        if User.objects.filter(email__iexact=decrypted_email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        decrypted_value = CryptoUtils.decrypt_data(value)
        if len(decrypted_value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in decrypted_value):
            raise serializers.ValidationError('Password must contain at least one number')
        if not any(char.isupper() for char in decrypted_value):
            raise serializers.ValidationError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in decrypted_value):
            raise serializers.ValidationError('Password must contain at least one lowercase letter')
        if not any(char in '!@#$%^&*()' for char in decrypted_value):
            raise serializers.ValidationError('Password must contain at least one special character (!@#$%^&*())')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        
        password = CryptoUtils.decrypt_data(password)
        email = CryptoUtils.decrypt_data(email)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=email,
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class DeliveryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = ['id', 'name', 'phone_number', 'customer_name', 'waybill_number', 
                 'address', 'zip_code', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class NomecoDeliverySerializer(DeliveryBaseSerializer):
    class Meta(DeliveryBaseSerializer.Meta):
        model = NomecoDelivery

class NovonordisDeliverySerializer(DeliveryBaseSerializer):
    class Meta(DeliveryBaseSerializer.Meta):
        model = NovonordisDelivery

class APIKeySerializer(serializers.ModelSerializer):
    key = serializers.CharField(read_only=True)
    
    class Meta:
        model = APIKey
        fields = ['id', 'name', 'key', 'created_at', 'is_active']
        read_only_fields = ['created_at']

class APIKeyProfileSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    expires_at = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = APIKey
        fields = ('name', 'key', 'created_at', 'created_at_formatted', 'expires_at', 'is_active', 'status')

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime('%B %d, %Y at %I:%M %p')

    def get_expires_at(self, obj):
        # Example: API keys expire after 1 year
        expires = obj.created_at + timezone.timedelta(days=365)
        days_left = (expires - timezone.now()).days
        return {
            'date': expires.strftime('%B %d, %Y at %I:%M %p'),
            'days_left': max(0, days_left)
        }

    def get_status(self, obj):
        if not obj.is_active:
            return 'inactive'
        expires = obj.created_at + timezone.timedelta(days=365)
        if timezone.now() > expires:
            return 'expired'
        days_left = (expires - timezone.now()).days
        if days_left <= 30:
            return 'expiring_soon'
        return 'active'

class ChangePasswordSerializer(serializers.Serializer):
    current_password = EncryptedCharField(required=True)
    new_password = EncryptedCharField(required=True)
    confirm_password = EncryptedCharField(required=True)

    def validate(self, data):
        # Decrypt passwords for comparison
        new_pass = CryptoUtils.decrypt_data(data['new_password'])
        confirm_pass = CryptoUtils.decrypt_data(data['confirm_password'])
        
        if new_pass != confirm_pass:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match'})
            
        return data

    def validate_new_password(self, value):
        # Add password validation rules
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError('Password must contain at least one number')
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in value):
            raise serializers.ValidationError('Password must contain at least one lowercase letter')
        if not any(char in '!@#$%^&*()' for char in value):
            raise serializers.ValidationError('Password must contain at least one special character (!@#$%^&*())')
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    api_keys = APIKeyProfileSerializer(many=True, read_only=True)
    last_login = serializers.SerializerMethodField()
    active_api_keys_count = serializers.SerializerMethodField()
    account_age = serializers.SerializerMethodField()
    profile_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'last_login', 'account_age', 'profile_summary',
            'active_api_keys_count', 'api_keys'
        )

    def get_last_login(self, obj):
        if not obj.last_login:
            return None
        return {
            'timestamp': obj.last_login.isoformat(),
            'formatted': obj.last_login.strftime('%B %d, %Y at %I:%M %p'),
            'timezone': str(timezone.get_current_timezone())
        }

    def get_active_api_keys_count(self, obj):
        return obj.api_keys.filter(is_active=True).count()

    def get_account_age(self, obj):
        age = timezone.now() - obj.date_joined
        years = age.days // 365
        months = (age.days % 365) // 30
        days = (age.days % 365) % 30
        
        parts = []
        if years > 0:
            parts.append(f"{years} year{'s' if years != 1 else ''}")
        if months > 0:
            parts.append(f"{months} month{'s' if months != 1 else ''}")
        if days > 0 or not parts:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        
        return {
            'days': age.days,
            'formatted': ' '.join(parts),
            'joined_date': obj.date_joined.strftime('%B %d, %Y')
        }

    def get_profile_summary(self, obj):
        return {
            'is_staff': obj.is_staff,
            'is_active': obj.is_active,
            'name': f"{obj.first_name} {obj.last_name}".strip() or None,
            'permissions_count': obj.user_permissions.count(),
            'groups_count': obj.groups.count()
        }