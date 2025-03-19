from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..utils.crypto import CryptoUtils
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import logging

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    if request.method == 'GET':
        return Response({'detail': 'CSRF cookie set'})
    
    try:
        encrypted_email = request.data.get('email', '')
        encrypted_password = request.data.get('password', '')
        
        email = CryptoUtils.decrypt_data(encrypted_email)
        password = CryptoUtils.decrypt_data(encrypted_password)
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            logger.info(f"User '{user.email}' successfully logged in from {request.META.get('REMOTE_ADDR')}")
            return Response({
                'detail': 'Successfully logged in',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'token': 'your-jwt-token-here'
            })
        else:
            return Response({
                'detail': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except ValueError as e:
        return Response({
            'detail': 'Invalid encrypted data'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'detail': 'Successfully logged out'})