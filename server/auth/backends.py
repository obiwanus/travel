from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from django.conf import settings


class EmailBackend(ModelBackend):

    def authenticate(self, email=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email__iexact=email)
            if check_password(password, user.password):
                return user
            else:
                return None
        except UserModel.DoesNotExist:
            return None
