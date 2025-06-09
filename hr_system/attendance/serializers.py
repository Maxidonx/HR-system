from rest_framework import serializers
from .models import Attendance # Imported above
from employees.serializers import EmployeeSerializer # For nested display

class AttendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Attendance model.
    """
    # Use a simplified employee serializer for nested representation
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    duration_hours = serializers.FloatField(source='duration', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 
            'employee', # Write-only, used internally for linking
            'employee_id',
            'employee_name',
            'date', 
            'clock_in', 
            'clock_out', 
            'duration_hours',
            'notes',
        ]
        read_only_fields = ('date', 'clock_in', 'clock_out', 'duration_hours')
        # Make employee field write-only as we display its details in other fields
        extra_kwargs = {
            'employee': {'write_only': True}
        }
