# # APIServer/views/token.py
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth import authenticate
# from rest_framework import status
# from rest_framework.response import Response

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         # Get the email and password from the request
#         email = attrs.get("email") or attrs.get("username")  # Accept both email and username
#         password = attrs.get("password")

#         # Authenticate the user
#         user = authenticate(request=self.context["request"], email=email, password=password)

#         if user is None:
#             # Check if the user exists and is inactive
#             from django.contrib.auth import get_user_model
#             User = get_user_model()
#             try:
#                 user = User.objects.get(email=email)
#                 if not user.is_active:
#                     return {
#                         "detail": "Your account is inactive. Please wait for admin approval."
#                     }
#             except User.DoesNotExist:
#                 pass
#             raise self.error_messages["no_active_account"]

#         # If authentication succeeds, proceed with token generation
#         data = super().validate(attrs)
#         return data
#     # def validate(self, attrs):
#     #     # Get the email and password from the request
#     #     email = attrs.get("email")
#     #     password = attrs.get("password")

#     #     # Authenticate the user
#     #     user = authenticate(request=self.context["request"], email=email, password=password)

#     #     if user is None:
#     #         # Check if the user exists and is inactive
#     #         from django.contrib.auth import get_user_model
#     #         User = get_user_model()
#     #         try:
#     #             user = User.objects.get(email=email)
#     #             if not user.is_active:
#     #                 return {
#     #                     "detail": "Your account is inactive. Please wait for admin approval."
#     #                 }
#     #         except User.DoesNotExist:
#     #             pass
#     #         raise self.error_messages["no_active_account"]

#     #     # If authentication succeeds, proceed with token generation
#     #     data = super().validate(attrs)
#     #     return data

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#         except Exception as e:
#             # If validation fails, return the error response
#             return Response(
#                 {"detail": str(e)},
#                 status=status.HTTP_403_FORBIDDEN if "inactive" in str(e).lower() else status.HTTP_401_UNAUTHORIZED
#             )
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)



from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
# from ..authentication import InactiveAccountException
from .authentication import InactiveAccountException

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email") or attrs.get("username")
        password = attrs.get("password")

        try:
            user = authenticate(request=self.context["request"], email=email, password=password)
        except InactiveAccountException as e:
            # Return the custom message as a JSON response
            raise serializers.ValidationError({"detail": str(e)})

        if user is None:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    raise serializers.ValidationError(
                        {"detail": "Your account is inactive. Please wait for admin approval."}
                    )
            except User.DoesNotExist:
                pass
            raise self.error_messages["no_active_account"]

        data = super().validate(attrs)
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            # Handle validation errors (including InactiveAccountException) as JSON
            return Response(
                e.detail,
                status=status.HTTP_403_FORBIDDEN if "inactive" in str(e).lower() else status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            # Handle any other unexpected errors
            return Response(
                {"detail": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)