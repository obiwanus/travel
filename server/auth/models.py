from django.db import models
from django.conf import settings
from django.contrib.auth.models import User as DjangoUser


class User(DjangoUser):
    class Meta:
        proxy = True

    USERNAME_FIELD = 'email'

    USER = 0
    USER_MANAGER = 1
    ADMIN = 2

    role = models.SmallIntegerField(default=USER, choices=(
        (USER, 'Normal user'),
        (USER_MANAGER, 'User manager'),
        (ADMIN, 'Administrator'),
    ))




class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile',
                                on_delete=models.CASCADE)
