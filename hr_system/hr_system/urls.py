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
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@hrsystem.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('users/', include('users.urls')),
        path('employees/', include('employees.urls')),
        path('', include('users.urls')),
        path('attendance/', include('attendance.urls')),
        path('leaves/', include('leaves.urls')),
        path('reports/', include('reports.urls')),
        path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    ])),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
