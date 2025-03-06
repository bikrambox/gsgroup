"""
Models for handling deliveries and API key authentication.
"""

from django.db import models
from django.utils import timezone


from django.core.validators import RegexValidator, MinLengthValidator

class DeliveryBase(models.Model):
    """Base model for all delivery types with common fields and validation."""
    name = models.CharField(max_length=50, db_index=True)
    phone_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be 10 digits'
            )
        ]
    )
    customer_name = models.CharField(max_length=50, db_index=True)
    waybill_number = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9]{8}$',
                message='Waybill number must be 8 alphanumeric characters'
            )
        ],
        unique=True,
        db_index=True
    )
    address = models.CharField(max_length=100)
    zip_code = models.CharField(
        max_length=5,
        validators=[
            RegexValidator(
                regex=r'^\d{5}$',
                message='Zip code must be 5 digits'
            )
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['created_at', 'customer_name']),
            models.Index(fields=['phone_number', 'zip_code'])
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} - {self.waybill_number}"

class NomecoDelivery(DeliveryBase):
    """Nomeco-specific delivery model."""
    
    class Meta:
        verbose_name = 'Nomeco Delivery'
        verbose_name_plural = 'Nomeco Deliveries'

class NovonordisDelivery(DeliveryBase):
    """Novonordis-specific delivery model."""
    
    class Meta:
        verbose_name = 'Novonordis Delivery'
        verbose_name_plural = 'Novonordis Deliveries'

class APIKey(models.Model):
    """API key model for authentication."""
    
    key = models.CharField(
        max_length=40,
        unique=True,
        validators=[MinLengthValidator(40)],
        db_index=True
    )
    name = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='api_keys',
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active'])
        ]

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        import secrets
        return secrets.token_hex(20)  # 40 characters hex string



class UploadedFile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)  # Store the relative path
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.PositiveIntegerField()  # Size in bytes

    def __str__(self):
        return f"{self.filename} by {self.user.username}"

    class Meta:
        indexes = [models.Index(fields=['user', 'uploaded_at'])]

