from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet # Imported above

router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet, basename='attendance')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]