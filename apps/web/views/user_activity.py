from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.cms.models import SystemLog
from apps.web.serializers import SystemLogSerializer
from rest_framework.pagination import PageNumberPagination

class UserSystemLogListView(generics.ListAPIView):
    serializer_class = SystemLogSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return SystemLog.objects.filter(user=user)
