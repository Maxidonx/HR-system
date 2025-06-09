from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserSerializer # Imported above

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for users to register.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny] # Anyone can register

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            {
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'token': token.key,
                'message': 'User registered successfully. An employee profile has been created.'
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class CustomAuthTokenView(ObtainAuthToken):
    """

    API endpoint for users to obtain an auth token (login).
    We customize it to return user data along with the token.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'first_name': user.first_name
        })
