
from django.contrib.auth.base_user import BaseUserManager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        # changes google.COM to google.com
        email = self.normalize_email(email)

        # build user object , model is customuser Model
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        # using specifies save to whichever db this manager is currently configured to use
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)
