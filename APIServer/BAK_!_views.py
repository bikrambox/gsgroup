# APIServer/views.py
import os
import io
import json
import logging
import ftplib
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash, authenticate
from .models import APIKey
from .serializers import UserSerializer, APIKeySerializer, UserProfileSerializer, ChangePasswordSerializer
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from .ftp_fetch import FTPConnection
from datetime import datetime
from .forms import EmailAuthenticationForm

# Add imports for Simple JWT
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

logger = logging.getLogger(__name__)

from .models import NomecoDelivery, NovonordisDelivery
from .serializers import NomecoDeliverySerializer, NovonordisDeliverySerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Get the email and password from the request
        email = attrs.get("email")
        password = attrs.get("password")

        # First, check if the user exists (case-insensitive email lookup)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(email__iexact=email)  # Case-insensitive lookup
            logger.info(f"Found user with email {email}: {user.username}, is_active={user.is_active}")
        except User.DoesNotExist:
            logger.warning(f"No user found with email {email}")
            raise serializers.ValidationError(
                # "No account found with the given email address.",
                "Your account is inactive. Please wait for admin approval.",
                code="no_account"
            )

        # Check if the user is inactive
        if not user.is_active:
            logger.info(f"User {email} is inactive")
            raise serializers.ValidationError(
                "Your account is inactive. Please wait for admin approval Original.",
                code="inactive_account"
            )

        # Authenticate the user
        user = authenticate(request=self.context["request"], email=email, password=password)
        if user is None:
            logger.warning(f"Authentication failed for email {email}")
            raise serializers.ValidationError(
                "Invalid password.",
                code="invalid_password"
            )

        # If authentication succeeds, proceed with token generation
        data = super().validate(attrs)
        return data


# # Custom Token Obtain Pair View for handling inactive users
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         # Get the email and password from the request
#         email = attrs.get("email")
#         password = attrs.get("password")

#         # First, check if the user exists (case-insensitive email lookup)
#         from django.contrib.auth import get_user_model
#         User = get_user_model()
#         try:
#             user = User.objects.get(email__iexact=email)  # Case-insensitive lookup
#         except User.DoesNotExist:
#             # If the user doesn't exist, raise a generic error
#             raise serializers.ValidationError(
#                 "No account found with the given email address.",
#                 code="no_account"
#             )

#         # Check if the user is inactive
#         if not user.is_active:
#             raise serializers.ValidationError(
#                 "Your account is inactive. Please wait for admin approval.",
#                 code="inactive_account"
#             )

#         # Authenticate the user
#         user = authenticate(request=self.context["request"], email=email, password=password)
#         if user is None:
#             # If authentication fails (e.g., wrong password), raise a generic error
#             raise serializers.ValidationError(
#                 "Invalid password.",
#                 code="invalid_password"
#             )

#         # If authentication succeeds, proceed with token generation
#         data = super().validate(attrs)
#         return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            # If validation fails, return the error response
            status_code = status.HTTP_403_FORBIDDEN if "inactive" in str(e).lower() else status.HTTP_401_UNAUTHORIZED
            return Response(
                {"detail": str(e)},
                status=status_code
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class CustomLoginView(LoginView):
    template_name = 'rest_framework/login.html'
    success_url = reverse_lazy('api-root')
    
    def get_success_url(self):
        return self.success_url

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Change the username field to email
        form.fields['username'].label = 'Email'
        form.fields['username'].help_text = 'Enter your email address'
        return form

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
            
            if not user.check_password(serializer.validated_data['current_password']):
                return Response(
                    {'error': 'Current password is incorrect'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return Response({
                'message': 'Password changed successfully',
                'status': 'success'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        "message": f"Welcome {request.user.email if request.user.is_authenticated else 'Guest'} to the API",
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
    if request.user.is_authenticated:
        return redirect('api-root')

    if request.method == 'GET':
        return Response({
            "message": "User Registration API",
            "method": "POST",
            "required_fields": {
                "username": "(required) - Choose a unique username",
                "email": "(required) - Provide a valid email address (used for login)",
                "password": "(required) - Choose a secure password",
                "first_name": "(optional) - Your first name",
                "last_name": "(optional) - Your last name"
            }
        }, status=status.HTTP_200_OK)
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Create the user with is_active=False
        user = serializer.save()
        user.is_active = False  # Set the user to inactive by default
        user.save()
        return Response({
            "message": "User registered successfully. Awaiting admin approval to activate your account."
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('/api/')
    
    return redirect(reverse('rest_framework:login'))

def custom_404(request, exception):
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
    permission_classes = [IsAdminUser]
    
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
    from django.contrib.auth import logout
    logout(request)
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_json_file(request):
    """
    API endpoint to upload multiple JSON files to an FTPS server.
    Files are checked for .json extension, necessary folders are verified/created, then uploaded.
    """
    logger.debug(f"Received request.FILES: {dict(request.FILES)}")
    logger.debug(f"Request headers: {dict(request.headers)}")
    logger.debug(f"Request data: {request.data}")

    if not request.FILES:
        return Response(
            {'error': 'No files uploaded', 'details': 'request.FILES is empty'},
            status=status.HTTP_400_BAD_REQUEST
        )

    files = request.FILES.getlist('files')
    if not files:
        return Response(
            {'error': 'No files provided in the request (use key "files")'},
            status=status.HTTP_400_BAD_REQUEST
        )

    username = request.user.username
    today_date = datetime.now().strftime('%Y_%m_%d')
    ftp_base_path = f'/Reports/ELON_data/Upload_test/{username}_{today_date}'

    ftp = FTPConnection(authenticated_username=username)
    ftp_connect_result = ftp.connect()
    if ftp_connect_result['status'] != 'success':
        return Response(
            {'error': 'Failed to connect to FTPS server', 'details': ftp_connect_result['message']},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    try:
        mkdir_result = ftp.mkdir(ftp_base_path)
        if mkdir_result['status'] != 'success':
            return Response(
                {'error': f"Failed to create directory {ftp_base_path}", 'details': mkdir_result['message']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            ftp.ftp.cwd(ftp_base_path)
            logger.info(f"Successfully navigated to {ftp_base_path}")
        except ftplib.error_perm as e:
            logger.error(f"Failed to navigate to {ftp_base_path}: {e}")
            return Response(
                {'error': f'Failed to navigate to directory {ftp_base_path}: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        results = []
        all_successful = True
        for uploaded_file in files:
            if not uploaded_file.name.lower().endswith('.json'):
                result = {
                    'filename': uploaded_file.name,
                    'status': 'error',
                    'message': 'Only JSON files are allowed'
                }
                results.append(result)
                all_successful = False
                continue

            file_buffer = io.BytesIO(uploaded_file.read())
            ftp_result = ftp.upload_stream(file_buffer, uploaded_file.name, username)
            if ftp_result['status'] == 'success':
                result = {
                    'filename': uploaded_file.name,
                    'status': 'success',
                    'ftp_path': ftp_result['file_path'],
                    'message': ftp_result['message']
                }
                results.append(result)
            else:
                logger.error(f"FTPS upload failed for {uploaded_file.name}: {ftp_result['message']}")
                result = {
                    'filename': uploaded_file.name,
                    'status': 'error',
                    'message': ftp_result['message']
                }
                results.append(result)
                all_successful = False

        if all_successful:
            return Response({
                'message': 'File upload processing completed',
                'results': results,
                'user': username
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'File upload processing completed with errors',
                'results': results,
                'user': username
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Unexpected error during file upload: {str(e)}")
        return Response(
            {'error': f'Unexpected error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    finally:
        ftp.disconnect()