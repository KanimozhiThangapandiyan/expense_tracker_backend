from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from apps.access.models import Role, Permission

class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model."""
    class Meta:
        model = Role
        fields = '__all__'

class ContentTypeSerializer(serializers.ModelSerializer):
    """Serializer for ContentType model."""
    class Meta:
        model = ContentType
        fields = ['id', 'app_label', 'model']

class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for Permission model."""
    model = ContentTypeSerializer(read_only=True)  # Display content type details
    model_id = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(), write_only=True, source='model'
    )
    create = serializers.BooleanField(required=True)
    retrieve = serializers.BooleanField(required=True)
    update = serializers.BooleanField(required=True)
    destroy = serializers.BooleanField(required=True)

    class Meta:
        model = Permission
        fields = ['id', 'role', 'model', 'model_id', 'create', 'retrieve', 'update', 'destroy']
