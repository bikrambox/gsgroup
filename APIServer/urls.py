from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

router = DefaultRouter()

router.register(r'nomeco', views.NomecoDeliveryViewSet)
router.register(r'novonordis', views.NovonordisDeliveryViewSet)
router.register(r'apikeys', views.APIKeyViewSet)

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('profile/', views.get_user_profile, name='user-profile'),
    path('', include(router.urls)),
    path('auth/login/', views.CustomLoginView.as_view(), name='custom-login'),
    path('auth/logout/', views.logout_view, name='custom-logout'),
    path('auth/', include('rest_framework.urls')),
    # JWT Token endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/register/', views.register_user, name='register'),
]
