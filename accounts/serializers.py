from rest_framework import serializers
from .models import User
from questions.serializers import QuestionsListSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



class UserSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active', 'is_staff', 'date_joined', 'questions']

    def get_questions(self, obj):
        qs = obj.questions.all()
        return QuestionsListSerializer(instance=qs, many=True).data


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


class UserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['user_id'] = user.id
        token['email'] = user.email

        return token
