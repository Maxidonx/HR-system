from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer, LeaveStatusUpdateSerializer
from employees.models import Employee

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_staff

class LeaveRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint for handling leave requests.
    - Employees can create and view their own requests.
    - Admins can view all requests and approve/reject them.
    """
    queryset = LeaveRequest.objects.all().select_related('employee', 'reviewed_by')
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Admins see all leave requests.
        Employees see only their own leave requests.
        """
        user = self.request.user
        if not user.is_authenticated:
            return LeaveRequest.objects.none()
        
        if user.is_staff:
            return LeaveRequest.objects.all()
        
        try:
            employee = Employee.objects.get(user=user)
            return LeaveRequest.objects.filter(employee=employee)
        except Employee.DoesNotExist:
            return LeaveRequest.objects.none()

    def perform_create(self, serializer):
        """
        Automatically associate the leave request with the logged-in user's employee profile.
        """
        try:
            employee = Employee.objects.get(user=self.request.user)
            serializer.save(employee=employee)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("A valid employee profile for the current user could not be found.")

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrReadOnly], url_path='approve')
    def approve(self, request, pk=None):
        """
        Custom action for an admin to approve a leave request.
        """
        leave_request = self.get_object()
        leave_request.status = LeaveRequest.LeaveStatus.APPROVED
        leave_request.reviewed_by = request.user
        leave_request.reviewer_comments = request.data.get('reviewer_comments', 'Approved.')
        leave_request.save()
        serializer = self.get_serializer(leave_request)
        return Response({'status': 'Leave request approved.', 'request': serializer.data})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrReadOnly], url_path='reject')
    def reject(self, request, pk=None):
        """
        Custom action for an admin to reject a leave request.
        """
        leave_request = self.get_object()
        leave_request.status = LeaveRequest.LeaveStatus.REJECTED
        leave_request.reviewed_by = request.user
        leave_request.reviewer_comments = request.data.get('reviewer_comments', 'Rejected.')
        leave_request.save()
        serializer = self.get_serializer(leave_request)
        return Response({'status': 'Leave request rejected.', 'request': serializer.data})