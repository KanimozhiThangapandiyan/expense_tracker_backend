from rest_framework import serializers
from apps.web.models import User

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'first_name', 'last_name', 'email_id', 'phone_number', 'alternative_phone_number', 'date_of_birth']
        fields='__all__'
