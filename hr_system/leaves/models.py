from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from employees.models import Employee

class LeaveRequest(models.Model):
    """
    Model to store employee leave requests.
    """
    class LeaveStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        CANCELLED = 'CANCELLED', 'Cancelled'

    class LeaveType(models.TextChoices):
        ANNUAL = 'ANNUAL', 'Annual Leave'
        SICK = 'SICK', 'Sick Leave'
        UNPAID = 'UNPAID', 'Unpaid Leave'
        MATERNITY = 'MATERNITY', 'Maternity Leave'
        PATERNITY = 'PATERNITY', 'Paternity Leave'
        OTHER = 'OTHER', 'Other'

    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='leave_requests'
    )
    leave_type = models.CharField(
        max_length=20, 
        choices=LeaveType.choices, 
        default=LeaveType.ANNUAL
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(help_text="Reason for the leave request.")
    status = models.CharField(
        max_length=20, 
        choices=LeaveStatus.choices, 
        default=LeaveStatus.PENDING
    )
    # The user who reviewed the request (e.g., manager or HR admin)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviewed_leave_requests'
    )
    reviewer_comments = models.TextField(blank=True, null=True, help_text="Comments from the reviewer.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def duration_days(self):
        """Calculates the total number of days for the leave request."""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0

    def clean(self):
        """
        Custom model validation.
        """
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError("Leave end date cannot be before the start date.")
        super().clean()

    def __str__(self):
        return f"Leave request for {self.employee.full_name} from {self.start_date} to {self.end_date}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Leave Request"
        verbose_name_plural = "Leave Requests"