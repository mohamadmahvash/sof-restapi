from rest_framework import serializers
from .models import User
from questions.serializers import QuestionsListSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active', 'is_staff', 'date_joined', 'questions']

    def get_questions(self, obj):
        qs = obj.questions.all()
        return QuestionsListSerializer(instance=qs, many=True).data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    # field-level validation
    def validate_username(self, value):
        value = value.strip()
        if value.lower() == 'admin':
            raise serializers.ValidationError('username can not be `admin`')
        user = User.objects.filter(username__iexact=value).exists()
        if user:
            raise serializers.ValidationError("username already exist")
        return value

    def validate_email(self, value):
        value = value.strip()
        if "admin" in value.lower():
            raise serializers.ValidationError("Email should not contain `admin`")
        user = User.objects.filter(email__iexact=value).exists()
        if user:
            raise serializers.ValidationError("Email already registered")
        return value.lower()

    # object-level validation
    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError('passwords must match')
        return data


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['user_id'] = user.id
        token['email'] = user.email

        return token


class UserLogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
