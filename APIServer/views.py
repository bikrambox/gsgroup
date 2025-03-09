# APIServer/views.py
import os
import io
import json
import logging
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
from .ftp_fetch import FTPConnection

logger = logging.getLogger(__name__)

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
        "message": f"Welcome {request.user.username if request.user.is_authenticated else 'Guest'} to the API",
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

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def upload_json_file(request):
#     """
#     API endpoint to upload multiple JSON files to an FTPS server.
#     Files are validated in RAM, then uploaded to /Reports/ELON_data/Upload_test/<username>_<today's_date>/.
#     """
#     if not request.FILES:
#         return Response(
#             {'error': 'No files uploaded'},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     files = request.FILES.getlist('files')
#     if not files:
#         return Response(
#             {'error': 'No files provided in the request (use key "files")'},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     username = request.user.username
#     ftp = FTPConnection(authenticated_username=username)
#     ftp_connect_result = ftp.connect()
#     if ftp_connect_result['status'] != 'success':
#         return Response(
#             {'error': 'Failed to connect to FTPS server', 'details': ftp_connect_result['message']},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )

#     try:
#         results = []
#         for uploaded_file in files:
#             if not uploaded_file.name.lower().endswith('.json'):
#                 results.append({
#                     'filename': uploaded_file.name,
#                     'status': 'error',
#                     'message': 'Only JSON files are allowed'
#                 })
#                 continue

#             try:
#                 file_content = uploaded_file.read()
#                 json_data = file_content.decode('utf-8-sig')  # Use utf-8-sig to handle BOM
#                 json.loads(json_data)  # Validate JSON
#                 file_buffer = io.BytesIO(file_content)
#             except json.JSONDecodeError as e:
#                 logger.error(f"Invalid JSON in {uploaded_file.name}: {str(e)}")
#                 results.append({
#                     'filename': uploaded_file.name,
#                     'status': 'error',
#                     'message': f'Invalid JSON file: {str(e)}'
#                 })
#                 continue
#             except UnicodeDecodeError as e:
#                 logger.error(f"Encoding error in {uploaded_file.name}: {str(e)}")
#                 results.append({
#                     'filename': uploaded_file.name,
#                     'status': 'error',
#                     'message': f'Encoding error: {str(e)}'
#                 })
#                 continue
#             except Exception as e:
#                 logger.error(f"Error processing {uploaded_file.name}: {str(e)}")
#                 results.append({
#                     'filename': uploaded_file.name,
#                     'status': 'error',
#                     'message': f'Error processing file: {str(e)}'
#                 })
#                 continue

#             ftp_result = ftp.upload_stream(file_buffer, uploaded_file.name)
#             if ftp_result['status'] == 'success':
#                 results.append({
#                     'filename': uploaded_file.name,
#                     'status': 'success',
#                     'ftp_path': ftp_result['file_path'],
#                     'message': ftp_result['message']
#                 })
#             else:
#                 logger.error(f"FTPS upload failed for {uploaded_file.name}: {ftp_result['message']}")
#                 results.append({
#                     'filename': uploaded_file.name,
#                     'status': 'error',
#                     'message': ftp_result['message']
#                 })

#         return Response({
#             'message': 'File upload processing completed',
#             'results': results,
#             'user': username
#         }, status=status.HTTP_200_OK)

#     except Exception as e:
#         logger.error(f"Unexpected error during file upload: {str(e)}")
#         return Response(
#             {'error': f'Unexpected error: {str(e)}'},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
#     finally:
#         ftp.disconnect()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_json_file(request):
    """
    API endpoint to upload multiple JSON files to an FTPS server.
    Files are validated in RAM, necessary folders are verified/created, then uploaded.
    """
    if not request.FILES:
        return Response(
            {'error': 'No files uploaded'},
            status=status.HTTP_400_BAD_REQUEST
        )

    files = request.FILES.getlist('files')
    if not files:
        return Response(
            {'error': 'No files provided in the request (use key "files")'},
            status=status.HTTP_400_BAD_REQUEST
        )

    username = request.user.username
    today_date = datetime.now().strftime('%Y%m%d')
    ftp_base_path = f'/Reports/ELON_data/Upload_test/{username}_{today_date}/'

    ftp = FTPConnection(authenticated_username=username)
    ftp_connect_result = ftp.connect()
    if ftp_connect_result['status'] != 'success':
        return Response(
            {'error': 'Failed to connect to FTPS server', 'details': ftp_connect_result['message']},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    try:
        # Verify and create FTP folders
        ftp_dirs = ftp_base_path.split('/')
        current_path = ''
        for directory in ftp_dirs:
            if directory:  # Skip empty strings
                current_path = os.path.join(current_path, directory).replace('\\', '/')
                ftp.mkdir(current_path)

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

            try:
                file_content = uploaded_file.read()
                json_data = file_content.decode('utf-8-sig')  # Handle BOM
                json.loads(json_data)  # Validate JSON
                file_buffer = io.BytesIO(file_content)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in {uploaded_file.name}: {str(e)}")
                result = {
                    'filename': uploaded_file.name,
                    'status': 'error',
                    'message': f'Invalid JSON file: {str(e)}'
                }
                results.append(result)
                all_successful = False
                continue
            except UnicodeDecodeError as e:
                logger.error(f"Encoding error in {uploaded_file.name}: {str(e)}")
                result = {
                    'filename': uploaded_file.name,
                    'status': 'error',
                    'message': f'Encoding error: {str(e)}'
                }
                results.append(result)
                all_successful = False
                continue
            except Exception as e:
                logger.error(f"Error processing {uploaded_file.name}: {str(e)}")
                result = {
                    'filename': uploaded_file.name,
                    'status': 'error',
                    'message': f'Error processing file: {str(e)}'
                }
                results.append(result)
                all_successful = False
                continue

            # Attempt FTP upload
            ftp_result = ftp.upload_stream(file_buffer, os.path.join(ftp_base_path, uploaded_file.name))
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