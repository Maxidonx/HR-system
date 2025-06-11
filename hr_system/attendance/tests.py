from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from employees.models import Employee
from .models import Attendance
from django.utils import timezone
from datetime import timedelta

class AttendanceAPITests(APITestCase):
    """
    Test suite for the Attendance API endpoints (clock-in/clock-out).
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='attendee', 
            email='attendee@example.com', 
            password='attendeepassword'
        )
        self.employee = Employee.objects.create(
            user=self.user, 
            first_name="Attendee", 
            last_name="User", 
            email=self.user.email,
            joining_date="2025-01-01"
        )
        self.client.force_authenticate(user=self.user)

    def test_clock_in(self):
        """
        Ensure an employee can clock in successfully.
        """
        url = reverse('attendance-clock-in')
        response = self.client.post(url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 1)
        self.assertIsNone(Attendance.objects.get().clock_out)

    def test_cannot_clock_in_twice(self):
        """
        Ensure an employee cannot clock in if they already have an open record.
        """
        # First clock-in
        self.client.post(reverse('attendance-clock-in'), {}, format='json')
        
        # Second attempt
        response = self.client.post(reverse('attendance-clock-in'), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_clock_out(self):
        """
        Ensure an employee can clock out successfully.
        """
        # First, clock in
        self.client.post(reverse('attendance-clock-in'), {}, format='json')
        
        # Then, clock out
        url = reverse('attendance-clock-out')
        response = self.client.post(url, {"notes": "Work completed."}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        record = Attendance.objects.get()
        self.assertIsNotNone(record.clock_out)
        self.assertEqual(record.notes, "Work completed.")
