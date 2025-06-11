from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet # Imported above

router = DefaultRouter()
router.register(r'employee', EmployeeViewSet, basename='employee')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]