from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from datetime import date

class UserManager(BaseUserManager):
    """Manager for User model with email-based authentication."""

    def _create_user(self, email_id, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email_id:
            raise ValueError("The given email ID must be set")
        email_id = self.normalize_email(email_id)
        user = self.model(email_id=email_id, **extra_fields)
        user.password = password
        user.save(using=self._db)
        return user

    def create_user(self, email_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email_id, password, **extra_fields)

    def create_superuser(self, email_id, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("date_of_birth", date(2003, 1, 1))
        extra_fields.setdefault("phone_number", "0000000000")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email_id, password, **extra_fields)

    def get_or_none(self, *args, **kwargs):
        """
        Get the object based on the given **kwargs. If not present returns None.
        Note: Expects a single instance.
        """
        try:
            return self.get(*args, **kwargs)
        except (ObjectDoesNotExist, AttributeError, ValueError, MultipleObjectsReturned, ValidationError):
            return None