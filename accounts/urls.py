from django.urls import path
from . import api_views

app_name = "accounts"

urlpatterns = [
    path('register/', api_views.UserRegisterView.as_view()),
    path('profile/', api_views.UserProfileView.as_view()),
    path('change-password/', api_views.UserChangePasswordView.as_view()),
    path('admin/<int:pk>/', api_views.UserDetailView.as_view()),
    path('admin/<int:pk>/deactivate/', api_views.UserDeactivateView.as_view()),
    path('admin/<int:pk>/activate/', api_views.UserActivateView.as_view()),
    path('activate/<uidb64>/<token>/', api_views.UserActivationAccountView.as_view()),
    path('forgot-password/', api_views.ForgotPasswordView.as_view()),
    path('reset-password/<uidb64>/<token>/', api_views.ResetPasswordView.as_view()),
]
