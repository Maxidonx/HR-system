from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date # <-- Import date
from employees.models import Employee # Assumes the Employee model from the previous artifact

class Attendance(models.Model):
    """
    Model to store employee clock-in and clock-out records.
    """
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='attendance_records'
    )
    date = models.DateField(default=date.today) # <-- FIX: Changed default from timezone.now to date.today
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True, help_text="Optional notes, e.g., 'Forgot to clock out'.")

    @property
    def duration(self):
        """Calculates the duration of the work session in hours if clocked out."""
        if self.clock_in and self.clock_out:
            delta = self.clock_out - self.clock_in
            return round(delta.total_seconds() / 3600, 2) # Returns duration in hours
        return None

    def __str__(self):
        return f"{self.employee.full_name} on {self.date}"

    class Meta:
        ordering = ['-date', '-clock_in']
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"
        # Ensures an employee can only have one "open" (not clocked-out) record at a time
        unique_together = ('employee', 'date', 'clock_out')
