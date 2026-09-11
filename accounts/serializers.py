from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active', 'is_staff', 'date_joined']


def clean_email(value):
    if "admin" in value:
        raise serializers.ValidationError("Email should not contain `admin`")


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, validators=[clean_email])
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    # field-level validation
    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError('username can not be `admin`')
        return value

    def validate_email(self, value):
        user = User.objects.filter(email=value).exists()
        if user:
            raise serializers.ValidationError("Email already registered")
        return value

    # object-level validation
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('passwords must match')
        return data


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
