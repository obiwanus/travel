from rest_framework import serializers
from auth.models import User, UserProfile


class UserS(serializers.ModelSerializer):

    role = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'role', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}
