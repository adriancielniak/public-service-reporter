# auth/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


def validate_role(value):
    if value not in ['standard', 'worker', 'admin']:
        raise serializers.ValidationError("Invalid user's role.")
    return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role', 'data', 'reports']

