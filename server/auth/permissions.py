from rest_framework.permissions import BasePermission
from auth.models import UserProfile


class IsUserManager(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated():
            return False

        try:
            role = request.user.profile.role
        except UserProfile.DoesNotExist:
            return False

        if role in (UserProfile.USER_MANAGER, UserProfile.ADMIN):
            return True

        return False

