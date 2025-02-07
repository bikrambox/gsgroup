from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Import settings!
from django.conf.urls.static import static  # Import static

# from django.conf.urls import handler404  # Important: Import handler404
# from APIServer.views import custom_404


# handler404 = custom_404  # Add this line



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('APIServer.urls')),  # Add this line to include your app URLs
]





# if settings.DEBUG: # Only in development
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
