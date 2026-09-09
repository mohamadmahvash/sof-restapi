from .models import User


def create_user(*, username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
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


def deactivate_user(user):
    user.is_active = False
    user.save(update_fields=['is_active'])
    return user
