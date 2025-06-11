from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from employees.models import Employee

class ReportingAPITests(APITestCase):
    """
    Test suite for the Reporting API endpoints.
    """

    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass')
        self.employee_user = User.objects.create_user('employee', 'employee@test.com', 'emppass')
        Employee.objects.create(user=self.employee_user, first_name="Emp", last_name="One", email='e1@test.com', department="Engineering", joining_date="2025-01-01")
        Employee.objects.create(user=self.admin_user, first_name="Admin", last_name="User", email='a1@test.com', department="Management", joining_date="2025-01-01")

    def test_admin_can_access_dashboard_summary(self):
        """
        Ensure an admin user can get the dashboard summary report.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('report-dashboard-summary')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('summary_metrics', response.data)
        self.assertIn('department_distribution', response.data)
        self.assertEqual(response.data['summary_metrics']['total_employees'], 2)

    def test_employee_cannot_access_dashboard_summary(self):
        """
        Ensure a regular employee cannot access the dashboard summary.
        """
        self.client.force_authenticate(user=self.employee_user)
        url = reverse('report-dashboard-summary')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_export_employee_csv(self):
        """
        Ensure an admin can download the employee CSV report.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('report-export-employees')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        # Check that the content contains the header and employee data
        content = response.content.decode('utf-8')
        self.assertIn('Employee ID,First Name,Last Name', content)
        self.assertIn('Emp,One', content)
