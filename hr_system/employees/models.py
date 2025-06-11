from django.db import models
from django.conf import settings # Import settings to get the AUTH_USER_MODEL
import uuid

class Employee(models.Model):
    """
    Model to store employee information.
    Now linked to a User account.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # If the user is deleted, the employee profile is also deleted.
        related_name='employee_profile',
        null=True, # Can be temporarily null until the user account is created/linked
        blank=True
    )

    # The rest of the model remains the same...
    employee_id = models.CharField(max_length=20, unique=True, blank=True, help_text="Unique Employee ID (e.g., EMP001). Auto-generated if blank.")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    job_title = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    joining_date = models.DateField()
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Designates whether this employee is currently active.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            # Same ID generation logic as before
            last_employee = Employee.objects.all().order_by('id').last()
            if last_employee and last_employee.employee_id and last_employee.employee_id.startswith('EMP'):
                try:
                    last_id_num = int(last_employee.employee_id[3:])
                    new_id_num = last_id_num + 1
                    self.employee_id = f'EMP{new_id_num:03d}'
                except ValueError:
                    self.employee_id = f'EMP{uuid.uuid4().hex[:6].upper()}'
            else:
                self.employee_id = f'EMP{uuid.uuid4().hex[:3].upper()}{Employee.objects.count() + 1:03d}'
        super().save(*args, **kwargs)
    
    # When an Employee is created or updated, sync basic info from the associated User account
    def sync_from_user(self):
        if self.user:
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
            self.email = self.user.email
            self.save()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
