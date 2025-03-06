from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..utils.crypto import CryptoUtils
from django.views.decorators.csrf import ensure_csrf_cookie
import json

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    # Handle GET request to set CSRF cookie
    if request.method == 'GET':
        return Response({'detail': 'CSRF cookie set'})
    """
    Custom login view that handles encrypted credentials
    """
    try:
        # Get encrypted credentials
        encrypted_username = request.data.get('username', '')
        encrypted_password = request.data.get('password', '')
        
        # Decrypt credentials
        username = CryptoUtils.decrypt_data(encrypted_username)
        password = CryptoUtils.decrypt_data(encrypted_password)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({
                'detail': 'Successfully logged in',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
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
    """
    Logout view
    """
    logout(request)
    return Response({'detail': 'Successfully logged out'})
