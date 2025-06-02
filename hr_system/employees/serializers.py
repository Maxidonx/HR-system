from rest_framework import serializers
from .models import EmployeeProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = ['id', 'username', 'employee_id', 'contact', 'job_title', 'department']
