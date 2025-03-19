from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from .models import APIKey
import logging

logger = logging.getLogger(__name__)

class EmailAuthenticationBackend(BaseBackend):
    """
    Custom authentication backend to authenticate users using email instead of username.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.warning(f"Authentication failed: No user found with email {email}")
            return None

        if user.check_password(password):
            logger.info(f"User with email {email} authenticated successfully")
            return user
        logger.warning(f"Authentication failed: Incorrect password for email {email}")
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class APIKeyAuthentication(BaseBackend):
    """
    Custom authentication backend for API key authentication.
    """
    def authenticate(self, request, api_key=None):
        if not api_key:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('ApiKey '):
                api_key = auth_header.split(' ')[1]
            else:
                return None

        try:
            api_key_obj = APIKey.objects.get(key=api_key, is_active=True)
            logger.info(f"API key authentication successful for user: {api_key_obj.user.email}")
            return api_key_obj.user
        except APIKey.DoesNotExist:
            logger.warning("API key authentication failed: Invalid or inactive API key")
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class DRFAPIKeyAuthentication(authentication.BaseAuthentication):
    """
    DRF authentication class for API key authentication.
    """
    def authenticate(self, request):
        api_key = None
        
        # Check Authorization header with 'ApiKey' prefix
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('ApiKey '):
            api_key = auth_header.split(' ')[1]
            logger.info("API key found in Authorization header with ApiKey prefix")
        
        # Check the direct APIKey header (Postman's APIKey auth type)
        elif 'HTTP_APIKEY' in request.META:
            api_key = request.META['HTTP_APIKEY']
            logger.info("API key found in APIKey header")
            
        # Check query parameters
        if not api_key:
            api_key = request.query_params.get('api_key')
            if api_key:
                logger.info("API key found in query parameters")

        if not api_key:
            logger.warning("No API key found in request")
            return None

        try:
            logger.info(f"Looking up API key: {api_key[:8]}...")
            api_key_obj = APIKey.objects.get(key=api_key, is_active=True)
            logger.info(f"API key found and valid for user: {api_key_obj.user.email}")
            return (api_key_obj.user, None)
        except APIKey.DoesNotExist:
            logger.warning(f"Invalid API key attempted: {api_key[:8]}...")
            try:
                inactive_key = APIKey.objects.get(key=api_key, is_active=False)
                raise exceptions.AuthenticationFailed('API key is inactive')
            except APIKey.DoesNotExist:
                raise exceptions.AuthenticationFailed('Invalid API key')
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {str(e)}")
            raise exceptions.AuthenticationFailed('Authentication error')