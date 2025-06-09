from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User # Imported above
from employees.models import Employee # We'll need this to create an Employee profile on registration
import datetime

class UserSerializer(serializers.ModelSerializer):
    """Serializer for displaying user details."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration. Handles creation of User and Token.
    """
    # Make password write-only for security
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
        # Remove password2 from the data to be passed to User.objects.create_user
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        
        # We can also create a basic employee profile at the same time.
        # This is a good place to link the two models together from the start.
        # The HR admin would then fill in the rest of the details (job_title, joining_date etc.)
        Employee.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            joining_date=datetime.date.today() # Placeholder joining date
        )
        
        Token.objects.create(user=user)
        return user
