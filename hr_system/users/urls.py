from django.urls import path
from .views import UserRegistrationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # The registration view remains the same
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    
    # New endpoints for JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Get tokens
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Refresh access token
]
