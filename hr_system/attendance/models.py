# FILE: attendance/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clock_in = models.DateTimeField(auto_now_add=True)
    clock_out = models.DateTimeField(null=True, blank=True)
