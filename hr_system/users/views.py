from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserSerializer
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
        
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            {
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'message': 'User registered successfully. Please login to get your tokens.'
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )