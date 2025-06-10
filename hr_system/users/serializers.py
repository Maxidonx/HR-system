from rest_framework import serializers
from .models import User
from employees.models import Employee
from django.utils.timezone import now

class UserSerializer(serializers.ModelSerializer):
    """Serializer for displaying user details."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_manager')

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration. Handles creation of User.
    The JWTs will be created by a different endpoint, not during registration.
    """
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, label="Confirm password")

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        """Check that the two password entries match."""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        """
        Create a new user and a corresponding, empty employee profile.
        """
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        
        # Create a basic employee profile at the same time.
        Employee.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            joining_date=now().date() # Use a date object
        )
        
        # We NO LONGER create a Token here.
        # Token.objects.create(user=user) # <-- REMOVE this line
        
        return user