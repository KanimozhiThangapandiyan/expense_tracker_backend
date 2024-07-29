from rest_framework import serializers
from apps.web.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email_id', 'phone_number', 'alternative_phone_number', 'date_of_birth','password']
        extra_kwargs = {
            'password': {'write_only': True},
            'alternative_phone_number': {'required': False},
        }
        def create(self, validated_data):
            password = validated_data.pop('password')
            user = User(**validated_data)
            user.password = password
            user.save()
            return user
