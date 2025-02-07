# myapp/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser   
from rest_framework.response import Response
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .models import APIKey
from .serializers import UserSerializer, APIKeySerializer, UserProfileSerializer, ChangePasswordSerializer
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView


from .models import NomecoDelivery, NovonordisDelivery
from .serializers import NomecoDeliverySerializer, NovonordisDeliverySerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    if request.method == 'POST':
        if 'password' not in request.data:
            return Response(
                {'error': 'Password change requires a password field'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ChangePasswordSerializer(data=request.data['password'])
        if serializer.is_valid():
            user = request.user
            
            # Verify current password
            if not user.check_password(serializer.validated_data['current_password']):
                return Response(
                    {'error': 'Current password is incorrect'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Update session to prevent logout
            update_session_auth_hash(request, user)
            
            return Response({
                'message': 'Password changed successfully',
                'status': 'success'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # GET request handling
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_root(request):
    return Response({
        "message": f"Welcome {request.user.username} to the API",
        "endpoints": {
            "profile": "/api/profile/",
            "auth": {
                "login": "/api/auth/login/",
                "get_token": "/api/auth/token/",
                "register": "/api/auth/register/",
                "logout": "/api/auth/logout/",
                "nomeco": "/api/nomeco/",
                "novonordis": "/api/novonordis/",
                "apikeys": "/api/apikeys/"
            }
        }
    })

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register_user(request):
    # If user is already authenticated, redirect to API root
    if request.user.is_authenticated:
        return redirect('api-root')

    if request.method == 'GET':
        return Response({
            "message": "User Registration API",
            "method": "POST",
            "required_fields": {
                "username": "(required) - Choose a unique username",
                "email": "(required) - Provide a valid email address",
                "password": "(required) - Choose a secure password"
            }
        }, status=status.HTTP_200_OK)
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(LoginView):
    template_name = 'rest_framework/login.html'
    success_url = reverse_lazy('api-root')
    
    def get_success_url(self):
        return self.success_url

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('/api/')
    
    return redirect(reverse('rest_framework:login'))

def custom_404(request, exception):
    # return JsonResponse({
    #     "error": "Not Found",
    #     "message": "The requested resource was not found",
    #     "status": 404
    # }, status=404)
    return render(request, 'error_404/index.html', status=404)


class NomecoDeliveryViewSet(viewsets.ModelViewSet):
    queryset = NomecoDelivery.objects.all()
    serializer_class = NomecoDeliverySerializer
    permission_classes = [IsAuthenticated]

class NovonordisDeliveryViewSet(viewsets.ModelViewSet):
    queryset = NovonordisDelivery.objects.all()
    serializer_class = NovonordisDeliverySerializer
    permission_classes = [IsAuthenticated]

class APIKeyViewSet(viewsets.ModelViewSet):
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer
    permission_classes = [IsAdminUser]  # Only admin users can manage API keys
    
    @action(detail=True, methods=['post'])
    def regenerate(self, request, pk=None):
        """Regenerate the API key"""
        api_key = self.get_object()
        api_key.key = APIKey.generate_key()
        api_key.save()
        return Response(self.get_serializer(api_key).data)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle the active status of the API key"""
        api_key = self.get_object()
        api_key.is_active = not api_key.is_active
        api_key.save()
        return Response(self.get_serializer(api_key).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Custom logout view that supports both session and token-based authentication
    """
    from django.contrib.auth import logout
    from rest_framework.response import Response
    from rest_framework import status

    # Perform session logout
    logout(request)
    
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)