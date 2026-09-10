from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .serializers import UserSerializer, UserRegisterSerializer, ChangePasswordSerializer
from .selectors import get_user_by_id
from .services import *
from .models import User


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user(username=serializer.validated_data['username'], email=serializer.validated_data['email'],
                           password=serializer.validated_data['password'])
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        username = request.data.get('username')
        user = update_profile(user=request.user, username=username)
        return Response(UserSerializer(user).data)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        change_password(user=request.user, password=serializer.validated_data['password'])
        return Response({'message': 'Password changed successfully'})


class UserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user = get_user_by_id(pk)
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user).data)

    def delete(self, request, pk):
        user = get_user_by_id(pk)
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)


class UserDeactivateView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        user = get_user_by_id(pk)
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        deactivate_user(user=user)
        return Response({"message": "User deactivated successfully"}, status=status.HTTP_200_OK)


class UserActivateView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        user = get_user_by_id(pk)
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        activate_user(user=user)
        return Response({"message": "User activated successfully"}, status=status.HTTP_200_OK)


class UserActivationAccountView(APIView):
    def get(self, request, uidb64, token):
        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=user_id)
        except Exception:
            return Response({"message": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            activate_user(user=user)
            return Response({"message": "Account activated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)
