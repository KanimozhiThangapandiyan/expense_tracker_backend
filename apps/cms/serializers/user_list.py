from rest_framework import serializers
from apps.access.models import User

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'uuid','created','updated','last_login','first_name', 'last_name', 'email_id', 'phone_number', 'alternative_phone_number', 'date_of_birth','is_staff','is_superuser']
