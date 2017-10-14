from rest_framework.permissions import BasePermission
from auth.models import UserProfile


class IsUserManager(BasePermission):

    def has_permission(self, request, view):

        if request.method in ['POST', 'OPTIONS']:
            return True  # Anyone can sign up

        # To PUT and GET user must have permissions
        if not request.user.is_authenticated():
            return False

        try:
            role = request.user.profile.role
        except UserProfile.DoesNotExist:
            return False

        if role in (UserProfile.USER_MANAGER, UserProfile.ADMIN):
            return True

        return False

