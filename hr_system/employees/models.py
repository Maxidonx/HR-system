# employees/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    contact = models.CharField(max_length=15)
    job_title = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
