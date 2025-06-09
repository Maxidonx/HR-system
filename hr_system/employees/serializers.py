from rest_framework import serializers
from .models import Employee


class DateFromDateTimeField(serializers.ReadOnlyField):
    def to_representation(self, value):
        if value is None:
            return None
        

    

class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    date_of_birth = DateFromDateTimeField()
    joining_date = DateFromDateTimeField()

    class Meta:
        model = Employee
        fields = [
            'id', 
            'employee_id', 
            'first_name', 
            'last_name', 
            'full_name',
            'email', 
            'phone_number', 
            'job_title', 
            'department', 
            'date_of_birth', 
            'joining_date', 
            'address',
            'is_active',
            'created_at', 
            'updated_at',
        ]
        read_only_fields = ('employee_id', 'created_at', 'updated_at')
    def validate_email(self, value):
        """
        Check if the email is unique, ignoring the current instance if updating.
        """
        query = Employee.objects.filter(email__iexact=value)
        if self.instance:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise serializers.ValidationError("An employee with this email already exists.")
        return value


