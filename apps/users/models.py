from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin
import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin')
    ]
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    email = models.EmailField(unique = True)
    phone_number = models.CharField(max_length = 20, blank = True)
    full_name = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length = 10, choices = ROLE_CHOICES, default = 'customer')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    objects = CustomUserManager()
    def __str__(self):
        return self.email