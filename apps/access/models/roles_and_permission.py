from django.db import models
from apps.common.models import Base,MAX_LENGTH
from django.contrib.contenttypes.models import ContentType


class Role(Base):
    """Model to store user roles"""
    name = models.CharField(max_length=MAX_LENGTH, unique=True)

    def save(self, *args, **kwargs):
        """Overriden to save role in lowercase"""
        self.name = self.name.lower()
        super().save(*args, **kwargs)
    
    def has_permission(self, model_name, permission_type):
        """Check if this role has a specific permission on a given model."""
        if permission_type not in ["create", "retrieve", "update", "destroy"]:
            raise ValueError(f"Invalid permission type: {permission_type}")
        model_name = model_name.lower()
        try:
            content_type = ContentType.objects.get(model=model_name)
        except ContentType.DoesNotExist:
            return False
        
        return Permission.objects.filter(role=self, model=content_type, **{permission_type: True}).exists()

    def __str__(self):
        return self.name

class Permission(Base):
    """Model to store permissions for each role"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    model = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    create = models.BooleanField(default=False)
    retrieve = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    destroy = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'model') # Ensure unique permissions per role and model
        default_related_name = "permissions"

    def __str__(self):
        return f"{self.role.name} - {self.model_name} (C:{self.create}, R:{self.retrieve}, U:{self.update}, D:{self.destroy})"