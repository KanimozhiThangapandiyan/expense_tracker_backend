from rest_framework import serializers
from apps.cms.models import SystemLog

class SystemLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemLog
        fields = ['id', 'login_time']
