from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from apps.common.models import Base,MAX_LENGTH,MAX_LENGTH_PHONE,DEFAULT_NULLABLE
from .managers import UserManager
from auditlog.registry import auditlog

class User(Base,AbstractBaseUser,PermissionsMixin):
    """User model with email as the unique identifier"""

    first_name = models.CharField(max_length=MAX_LENGTH)
    last_name = models.CharField(max_length=MAX_LENGTH)
    email_id = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=MAX_LENGTH_PHONE, unique=True)
    alternative_phone_number = models.CharField(max_length=MAX_LENGTH_PHONE, **DEFAULT_NULLABLE)
    date_of_birth = models.DateField()
    password = models.CharField(max_length=120)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email_id'
    REQUIRED_FIELDS = ['first_name','last_name','password']

    username = None

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
auditlog.register(User)
