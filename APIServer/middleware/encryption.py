from django.http import HttpResponse
from django.urls import resolve
import json
from ..utils.crypto import CryptoUtils

class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # List of paths that require encryption
        self.secure_paths = [
            '/api/auth/login/',
            '/api/auth/register/',
            '/api/auth/change-password/',
            '/api/profile/'
        ]
        # Fields that should be encrypted
        self.sensitive_fields = ['password', 'email', 'current_password', 'new_password', 'confirm_password']

    def __call__(self, request):
        path = request.path.rstrip('/')
        
        # Only process if it's a secure path and has a body
        if path in self.secure_paths and request.body:
            try:
                # Handle form data
                if request.content_type == 'application/x-www-form-urlencoded':
                    post_data = request.POST.copy()
                    for field in self.sensitive_fields:
                        if field in post_data:
                            # Encrypt the field if it's not already encrypted
                            try:
                                # Try to decrypt to check if it's already encrypted
                                CryptoUtils.decrypt_data(post_data[field])
                            except ValueError:
                                # If decryption fails, it means it's not encrypted yet
                                post_data[field] = CryptoUtils.encrypt_data(post_data[field])
                    request.POST = post_data

                # Handle JSON data
                elif request.content_type == 'application/json':
                    body = json.loads(request.body)
                    for field in self.sensitive_fields:
                        if field in body:
                            try:
                                CryptoUtils.decrypt_data(body[field])
                            except ValueError:
                                body[field] = CryptoUtils.encrypt_data(body[field])
                    request._body = json.dumps(body).encode('utf-8')

            except Exception as e:
                return HttpResponse(
                    json.dumps({'error': 'Invalid request data'}),
                    status=400,
                    content_type='application/json'
                )

        response = self.get_response(request)
        return response
