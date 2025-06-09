from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Employee # Imported above
from django.db import models
from .serializers import EmployeeSerializer # Imported above

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employees to be viewed or edited.
    """
    queryset = Employee.objects.all().order_by('-created_at') # Default ordering
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated] # Or more specific permissions

    # You can add custom actions here if needed
    # For example, to deactivate an employee
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser]) # Example: only admin can deactivate
    def deactivate(self, request, pk=None):
        employee = self.get_object()
        employee.is_active = False
        employee.save()
        return Response({'status': 'employee deactivated'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def activate(self, request, pk=None):
        employee = self.get_object()
        employee.is_active = True
        employee.save()
        return Response({'status': 'employee activated'}, status=status.HTTP_200_OK)
    
    # To perform search, you can use django-filter or override get_queryset
    # Example of simple search:
    def get_queryset(self):
        queryset = Employee.objects.all()
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(
                models.Q(first_name__icontains=search_term) |
                models.Q(last_name__icontains=search_term) |
                models.Q(email__icontains=search_term) |
                models.Q(employee_id__icontains=search_term) |
                models.Q(job_title__icontains=search_term) |
                models.Q(department__icontains=search_term)
            )
        
        # Example sorting
        sort_by = self.request.query_params.get('sort_by', '-created_at') # Default sort
        if sort_by in [f.name for f in Employee._meta.get_fields()]: # Check if valid field
             queryset = queryset.order_by(sort_by)
        else: # Default if invalid sort_by param
            queryset = queryset.order_by('-created_at')

        return queryset