# # FILE: leaves/tests.py

# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.urls import reverse
# from users.models import User
# from employees.models import Employee
# from leaves.models import LeaveRequest

# class LeaveRequestAPITests(APITestCase):
#     """
#     Test suite for the Leave Request API endpoints.
#     """

#     def setUp(self):
#         self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass')
#         self.employee_user = User.objects.create_user('employee', 'employee@test.com', 'emppass')
#         self.employee_profile = Employee.objects.create(
#             user=self.employee_user,
#             email=self.employee_user.email,
#             first_name="Test",
#             last_name="Employee",
#             joining_date="2025-01-01"
#         )

#     def test_employee_can_create_leave_request(self):
#         """
#         Ensure a logged-in employee can submit a leave request.
#         """
#         self.client.force_authenticate(user=self.employee_user)
#         url = reverse('leave-list')
#         data = {
#             "leave_type": "ANNUAL",
#             "start_date": "2025-10-20",
#             "end_date": "2025-10-22",
#             "reason": "Family event"
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(LeaveRequest.objects.count(), 1)
#         self.assertEqual(LeaveRequest.objects.get().status, 'PENDING')

#     def test_admin_can_approve_leave_request(self):
#         """
#         Ensure an admin can approve a pending leave request.
#         """
#         leave_request = LeaveRequest.objects.create(
#             employee=self.employee_profile,
#             leave_type="ANNUAL",
#             start_date="2025-11-01",
#             end_date="2025-11-02",
#             reason="Vacation"
#         )

#         self.client.force_authenticate(user=self.admin_user)
#         url = reverse('leave-approve', kwargs={'pk': leave_request.pk})
#         response = self.client.post(url, {}, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         leave_request.refresh_from_db()
#         self.assertEqual(leave_request.status, 'APPROVED')
#         self.assertEqual(leave_request.reviewed_by, self.admin_user)

#     def test_admin_can_reject_leave_request(self):
#         """
#         Ensure an admin can reject a pending leave request.
#         """
#         leave_request = LeaveRequest.objects.create(
#             employee=self.employee_profile,
#             leave_type="SICK",
#             start_date="2025-12-01",
#             end_date="2025-12-03",
#             reason="Medical"
#         )

#         self.client.force_authenticate(user=self.admin_user)
#         url = reverse('leave-reject', kwargs={'pk': leave_request.pk})
#         response = self.client.post(url, {'reviewer_comments': 'Insufficient documentation'}, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         leave_request.refresh_from_db()
#         self.assertEqual(leave_request.status, 'REJECTED')
#         self.assertEqual(leave_request.reviewed_by, self.admin_user)
#         self.assertEqual(leave_request.reviewer_comments, 'Insufficient documentation')
