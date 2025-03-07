from rest_framework import viewsets
from rest_framework import generics
from django.contrib.contenttypes.models import ContentType
from apps.access.serializers import ContentTypeSerializer
from apps.access.models import Role, Permission
from apps.access.serializers import RoleSerializer, PermissionSerializer

class RoleViewSet(viewsets.ModelViewSet):
    """View to handle CRUD operations on Role model."""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class PermissionViewSet(viewsets.ModelViewSet):
    """View to handle CRUD operations on Permission model."""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class ContentTypeListView(generics.ListAPIView):
    """View to list all available models in the project."""
    queryset = ContentType.objects.all().order_by('app_label', 'model')
    serializer_class = ContentTypeSerializer