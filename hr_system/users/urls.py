from django.urls import path
from .views import UserRegistrationView, CustomAuthTokenView # Imported above

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomAuthTokenView.as_view(), name='user-login'),
    # You could add other endpoints here, like 'profile/', 'change-password/', etc.
]
