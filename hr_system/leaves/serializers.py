from rest_framework import serializers
from .models import LeaveRequest
from employees.serializers import EmployeeSerializer # For nested info

class LeaveRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and viewing leave requests.
    """
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.get_full_name', read_only=True, default=None)
    duration_days = serializers.IntegerField(source='duration_days', read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 
            'employee',
            'employee_id', 
            'employee_name', 
            'leave_type',
            'start_date', 
            'end_date',
            'duration_days',
            'reason', 
            'status', 
            'reviewed_by_name',
            'reviewer_comments',
            'created_at',
        ]
        # Employee is set automatically from the logged-in user, status is read-only on creation
        read_only_fields = ('status', 'reviewer_comments', 'reviewed_by_name')
        extra_kwargs = {
            'employee': {'write_only': True}
        }

    def validate(self, data):
        """
        Check that the start_date is before the end_date.
        """
        if 'start_date' in data and 'end_date' in data and data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Leave end date cannot be before the start date.")
        return data

class LeaveStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for updating the status of a leave request.
    """
    class Meta:
        model = LeaveRequest
        fields = ['status', 'reviewer_comments']
        
    def validate_status(self, value):
        if value not in [LeaveRequest.LeaveStatus.APPROVED, LeaveRequest.LeaveStatus.REJECTED]:
            raise serializers.ValidationError("Status can only be updated to 'Approved' or 'Rejected'.")
        return value
