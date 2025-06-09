# In your users/models.py file

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model where email is the unique identifier for authentication.
    """
    email = models.EmailField(_('email address'), unique=True)
    
    # This is the field causing the error. Add default=False to fix it.
    is_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email