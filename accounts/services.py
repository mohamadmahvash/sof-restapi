from .models import User
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def create_user(*, username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    user.is_active = False
    user.save()
    send_activation_email(user=user)
    return user


def update_profile(*, user, username):
    user.username = username
    user.save(update_fields=['username'])
    return user


def change_password(*, user, password):
    user.set_password(password)
    user.save(update_fields=['password'])
    return user


def activate_user(*, user):
    user.is_active = True
    user.save(update_fields=['is_active'])
    return user


def deactivate_user(*, user):
    user.is_active = False
    user.save(update_fields=['is_active'])
    return user


def send_activation_email(*, user):
    user_id = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"http://127.0.0.1:8000/accounts/activate/{user_id}/{token}"
    send_mail(subject='activate your account', message=activation_link, from_email=settings.EMAIL_HOST_USER,
              recipient_list=[user.email])
