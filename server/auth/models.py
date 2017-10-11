from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    USER = 0
    USER_MANAGER = 1
    ADMIN = 2

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile',
                                on_delete=models.CASCADE)
    role = models.SmallIntegerField(default=USER, choices=(
        (USER, 'Normal user'),
        (USER_MANAGER, 'User manager'),
        (ADMIN, 'Administrator'),
    ))

    @property
    def role_display(self):
        return self.get_role_display()


