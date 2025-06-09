from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import date
from .models import Attendance # Imported above
from .serializers import AttendanceSerializer # Imported above
from employees.models import Employee # Imported above

class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for handling employee attendance records.
    Provides `clock_in` and `clock_out` actions.
    """
    queryset = Attendance.objects.all().select_related('employee')
    serializer_class = AttendanceSerializer
    # More specific permissions could be: IsAdminUser for list/destroy, IsAuthenticated for own records.
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the attendance records
        for the currently authenticated user.
        HR Admins should be able to see all records.
        """
        user = self.request.user
        
        # FIX: First, check if the user is authenticated. If not (e.g. during
        # schema generation by drf-yasg), return an empty queryset to prevent errors.
        if not user.is_authenticated:
            return Attendance.objects.none()

        if user.is_staff or user.is_superuser: # Admins see all
            return Attendance.objects.all().select_related('employee')
        
        # Regular employees see only their own records
        try:
            # We can now safely assume user is authenticated and has an email.
            employee = Employee.objects.get(email=user.email)
            return Attendance.objects.filter(employee=employee).select_related('employee')
        except Employee.DoesNotExist:
            # If no employee profile is linked to the user, return no records
            return Attendance.objects.none()

    @action(detail=False, methods=['post'], url_path='clock-in')
    def clock_in(self, request):
        """
        Creates a new attendance record with the current time as clock_in.
        """
        user = request.user
        try:
            employee = Employee.objects.get(email=user.email)
        except Employee.DoesNotExist:
            return Response({'error': 'No employee profile found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if there's already an open attendance record for today
        today = date.today()
        open_record = Attendance.objects.filter(employee=employee, date=today, clock_out__isnull=True).first()

        if open_record:
            return Response({'error': 'You have already clocked in today.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create new record
        record = Attendance.objects.create(employee=employee, clock_in=timezone.now())
        serializer = self.get_serializer(record)
        return Response({'status': 'Successfully clocked in.', 'record': serializer.data}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='clock-out')
    def clock_out(self, request):
        """
        Finds the open attendance record for the day and sets the clock_out time.
        """
        user = request.user
        try:
            employee = Employee.objects.get(email=user.email)
        except Employee.DoesNotExist:
            return Response({'error': 'No employee profile found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Find the open attendance record for today
        today = date.today()
        record_to_close = Attendance.objects.filter(employee=employee, date=today, clock_out__isnull=True).first()

        if not record_to_close:
            return Response({'error': 'No open clock-in record found for today.'}, status=status.HTTP_400_BAD_REQUEST)

        record_to_close.clock_out = timezone.now()
        record_to_close.save()
        
        serializer = self.get_serializer(record_to_close)
        return Response({'status': 'Successfully clocked out.', 'record': serializer.data}, status=status.HTTP_200_OK)
