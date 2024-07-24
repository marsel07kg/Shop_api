from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    email = serializers.EmailField()

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username

    def validate(self, data):
        if data['password'] != data['password']:
            raise ValidationError('Passwords do not match')
        return data


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserConfirmSerializer(serializers.Serializer):
    SMS = serializers.CharField(min_length=6, max_length=6)