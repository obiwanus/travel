from django.contrib.auth.models import User
from rest_framework import serializers

from auth.models import UserProfile


class UserS(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileS(serializers.ModelSerializer):

    user = UserS()

    class Meta:
        model = UserProfile
        fields = ('user', 'role')
