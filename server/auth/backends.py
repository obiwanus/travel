from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

from auth.models import User


class EmailBackend(ModelBackend):
    """
    Checks user's email instead of username
    """

    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email__iexact=email)
            if check_password(password, user.password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None
