from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from .models import APIKey
import logging

logger = logging.getLogger(__name__)

class APIKeyAuthentication(BaseBackend):
    def authenticate(self, request, api_key=None):
        if not api_key:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('ApiKey '):
                api_key = auth_header.split(' ')[1]
            else:
                return None

        try:
            api_key_obj = APIKey.objects.get(key=api_key, is_active=True)
            return api_key_obj.user
        except APIKey.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class DRFAPIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Try to get the API key from various places
        api_key = None
        
        # 1. Check Authorization header with 'ApiKey' prefix
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('ApiKey '):
            api_key = auth_header.split(' ')[1]
            logger.info("API key found in Authorization header with ApiKey prefix")
        
        # 2. Check the direct APIKey header (Postman's APIKey auth type)
        elif 'HTTP_APIKEY' in request.META:
            api_key = request.META['HTTP_APIKEY']
            logger.info("API key found in APIKey header")
            
        # 3. Check query parameters
        if not api_key:
            api_key = request.query_params.get('api_key')
            if api_key:
                logger.info("API key found in query parameters")

        if not api_key:
            logger.warning("No API key found in request")
            return None

        try:
            # Log the API key we're looking for (masked)
            logger.info(f"Looking up API key: {api_key[:8]}...")
            api_key_obj = APIKey.objects.get(key=api_key, is_active=True)
            logger.info(f"API key found and valid for user: {api_key_obj.user.username}")
            return (api_key_obj.user, None)
        except APIKey.DoesNotExist:
            logger.warning(f"Invalid API key attempted: {api_key[:8]}...")
            # Check if the key exists but is inactive
            try:
                inactive_key = APIKey.objects.get(key=api_key, is_active=False)
                raise exceptions.AuthenticationFailed('API key is inactive')
            except APIKey.DoesNotExist:
                raise exceptions.AuthenticationFailed('Invalid API key')
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {str(e)}")
            raise exceptions.AuthenticationFailed('Authentication error')
