from rest_framework import serializers
from apps.web.models import User
from django.contrib.auth.hashers import make_password

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
        validated_data['password'] = make_password(password)
        user = User(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)