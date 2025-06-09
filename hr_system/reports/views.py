import csv
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from employees.models import Employee
from leaves.models import LeaveRequest
from attendance.models import Attendance


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class ReportingDashboardView(APIView):
    """
    API View to provide data for the main HR dashboard.
    Accessible only by admin users.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        """
        Return a summary of key HR metrics.
        """
        # --- Employee Metrics ---
        total_employees = Employee.objects.filter(is_active=True).count()
        department_distribution = (
            Employee.objects.filter(is_active=True)
            .values('department')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # --- Leave Metrics ---
        today = timezone.now().date()
        employees_on_leave_today = LeaveRequest.objects.filter(
            start_date__lte=today, 
            end_date__gte=today, 
            status=LeaveRequest.LeaveStatus.APPROVED
        ).count()
        
        pending_leave_requests = LeaveRequest.objects.filter(
            status=LeaveRequest.LeaveStatus.PENDING
        ).count()

        # --- Attendance Metrics ---
        employees_clocked_in_today = Attendance.objects.filter(
            date=today,
            clock_out__isnull=True # They have an open record
        ).count()

        # --- Compile the response data ---
        dashboard_data = {
            'summary_metrics': {
                'total_employees': total_employees,
                'employees_on_leave_today': employees_on_leave_today,
                'pending_leave_requests': pending_leave_requests,
                'employees_clocked_in_today': employees_clocked_in_today,
            },
            'department_distribution': list(department_distribution),
        }
        
        return Response(dashboard_data, status=status.HTTP_200_OK)


class EmployeeReportExportView(APIView):
    """
    API View to export a CSV report of all employees.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        """
        Generate and stream a CSV file of all active employees.
        """
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="employee_report_{timezone.now().date()}.csv"'

        writer = csv.writer(response)
        
        # Define header row
        header = [
            'Employee ID', 'First Name', 'Last Name', 'Email', 
            'Phone Number', 'Job Title', 'Department', 'Joining Date'
        ]
        writer.writerow(header)

        # Get employee data
        employees = Employee.objects.filter(is_active=True)
        
        # Write data rows
        for employee in employees:
            row = [
                employee.employee_id,
                employee.first_name,
                employee.last_name,
                employee.email,
                employee.phone_number,
                employee.job_title,
                employee.department,
                employee.joining_date.strftime('%Y-%m-%d') if employee.joining_date else '',
            ]
            writer.writerow(row)

        return response
