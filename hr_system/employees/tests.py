from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from employees.models import Employee

class EmployeeAPITests(APITestCase):
    """
    Test suite for the Employee API endpoints.
    """

    def setUp(self):
        """
        Set up admin and regular users for testing.
        """
        self.admin_user = User.objects.create_superuser(
            username='admin', 
            email='admin@example.com', 
            password='adminpassword123'
        )
        # Manually create an Employee profile for the admin user,
        # because create_superuser does not trigger the registration serializer.
        Employee.objects.create(
            user=self.admin_user, 
            first_name="Admin", 
            last_name="Istrator", 
            email=self.admin_user.email,
            job_title="Admin",
            joining_date="2025-01-01"
        )
        
        self.regular_user = User.objects.create_user(
            username='employee', 
            email='employee@example.com', 
            password='employeepassword123'
        )
        # Link regular user to an employee profile
        self.employee_profile = Employee.objects.create(
            user=self.regular_user, 
            first_name="Regular", 
            last_name="Employee", 
            email=self.regular_user.email,
            job_title="Tester",
            joining_date="2025-01-01"
        )
        
        # Authenticate the client as the admin user for tests that need it
        self.client.force_authenticate(user=self.admin_user)

    def test_admin_can_list_employees(self):
        """
        Ensure admin user can list all employees.
        """
        url = reverse('employee-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_regular_user_cannot_create_employee(self):
        """
        Ensure a regular user cannot create a new employee profile via the main endpoint.
        """
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('employee-list')
        data = {"first_name": "New", "last_name": "Hire", "email": "new@hire.com", "joining_date": "2025-06-01"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)