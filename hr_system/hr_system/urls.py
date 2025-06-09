"""
URL configuration for hr_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# FILE: hr_system/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="HR System API",
      default_version='v1',
      description="API documentation for the Tunga TIA Dev Challenge HR System",
      terms_of_service="https://www.google.com/policies/terms/", # Replace with your terms
      contact=openapi.Contact(email="contact@hrsystem.local"),   # Replace with your contact
      license=openapi.License(name="BSD License"),             # Replace with your license
   ),

   public=True, # Set to False to make API docs private
   permission_classes=(permissions.AllowAny,), # Or IsAuthenticated for private docs
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # API routes
    path('api/v1/', include([ # Namespace your API versions
        path('users/', include('users.urls')), # Assuming users app has its own urls.py
        path('employees/', include('employees.urls')),
        path('', include('users.urls')),
        path('attendance/', include('attendance.urls')),
        path('leaves/', include('leaves.urls')),
        path('reports/', include('reports.urls')),
        
        # Auth endpoints (if using djoser or similar, or custom ones)
        # For basic token auth provided by DRF:
        path('auth/', include('rest_framework.urls', namespace='rest_framework')), # For login/logout in browsable API
        # You might need a specific endpoint to obtain a token.
        # `rest_framework.authtoken.views.obtain_auth_token` can be used for this.
        # Example: path('auth/token/', obtain_auth_token, name='api_token_auth'),
    ])),

    # Swagger API Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # If you have a frontend served by Django (not common with DRF as API backend)
    # path('', include('frontend.urls')), 
]
