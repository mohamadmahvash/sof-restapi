from rest_framework.views import APIView
from .serializers import UserSerializer, UserRegisterSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User(email=serializer.validated_data['email'], username=serializer.validated_data['username'])
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        username = request.data.get('username')
        request.user.username = username
        request.user.save(update_fields=['username'])
        return Response(UserSerializer(request.user).data)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save(update_fields=['password'])
        return Response({'message': 'Password changed successfully'})


class UserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user).data)

    def delete(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)


class UserDeactivateView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.is_active = False
        user.save(update_fields=['is_active'])
        return Response({"message": "User deactivated successfully"}, status=status.HTTP_200_OK)


class UserActivateView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.is_active = True
        user.save(update_fields=['is_active'])
        return Response({"message": "User activated successfully"}, status=status.HTTP_200_OK)
