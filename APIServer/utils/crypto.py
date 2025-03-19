from django.conf import settings
from django.utils.encoding import force_bytes
from base64 import b64encode, b64decode
from django.utils.crypto import salted_hmac

class CryptoUtils:
    @staticmethod
    def encrypt_data(data: str) -> str:
        """
        Encrypts data using Django's secret key as salt and returns base64 encoded string
        """
        if not data:
            return data
            
        # Convert data to bytes and add salt
        data_bytes = force_bytes(data)
        salt = force_bytes(settings.SECRET_KEY[:16])  # Use first 16 chars of secret key as salt
        
        # Create salted signature
        signature = salted_hmac(
            salt,
            data,
            secret=settings.SECRET_KEY,
            algorithm='sha256'  # Change to string 'sha256'
        ).hexdigest()
        
        # Combine signature with data and encode
        final_data = f"{signature}:{data}"
        encoded_data = b64encode(force_bytes(final_data)).decode('utf-8')
        
        return encoded_data

    @staticmethod
    def decrypt_data(encrypted_data: str) -> str:
        """
        Decrypts base64 encoded data and verifies signature
        """
        if not encrypted_data:
            return encrypted_data
            
        try:
            # Decode base64
            decoded_data = b64decode(encrypted_data).decode('utf-8')
            
            # Split signature and data
            signature, data = decoded_data.split(':', 1)
            
            # Verify signature
            salt = force_bytes(settings.SECRET_KEY[:16])
            expected_signature = salted_hmac(
                salt,
                data,
                secret=settings.SECRET_KEY,
                algorithm='sha256'  # Use string 'sha256'
            ).hexdigest()
            
            if signature != expected_signature:
                raise ValueError("Invalid signature")
                
            return data
            
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
