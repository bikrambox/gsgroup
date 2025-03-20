# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
# from . import views

# router = DefaultRouter()

# router.register(r'nomeco', views.NomecoDeliveryViewSet)
# router.register(r'novonordis', views.NovonordisDeliveryViewSet)
# router.register(r'apikeys', views.APIKeyViewSet)

# urlpatterns = [
#     path('', views.api_root, name='api-root'),
#     path('profile/', views.get_user_profile, name='user-profile'),
#     path('', include(router.urls)),
#     path('auth/login/', views.CustomLoginView.as_view(), name='custom-login'),
#     path('auth/logout/', views.logout_view, name='custom-logout'),
#     path('auth/', include('rest_framework.urls')),
#     path('auth/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Use the custom view
#     path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
#     path('auth/register/', views.register_user, name='register'),
#     path('upload/', views.upload_json_file, name='upload-json'),  # Add this line
# ]


    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

# from .view.auth import login_view, logout_view  # Import both login_view and logout_view
    # path('auth/login/', login_view, name='custom-login'),  # Use login_view from views/auth.py
    # path('auth/logout/', logout_view, name='custom-logout'),  # Use the imported logout_view



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views
from .views import CustomLoginView  # Explicitly import CustomLoginView
from .token import CustomTokenObtainPairView  # Import CustomTokenObtainPairView

router = DefaultRouter()

router.register(r'nomeco', views.NomecoDeliveryViewSet)
router.register(r'novonordis', views.NovonordisDeliveryViewSet)
router.register(r'apikeys', views.APIKeyViewSet)

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('profile/', views.get_user_profile, name='user-profile'),
    path('', include(router.urls)),
    # path('api/auth/login/', CustomLoginView.as_view(), name='api_login'),
    # path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/', CustomLoginView.as_view(), name='custom-login'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/logout/', views.logout_view, name='custom-logout'),
    path('auth/', include('rest_framework.urls')),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/register/', views.register_user, name='register'),
    path('upload/', views.upload_json_file, name='upload-json'),  # Add this line
    path('adminfront/', views.AdminFrontView.as_view(), name='admin_front'),  # New endpoint
]