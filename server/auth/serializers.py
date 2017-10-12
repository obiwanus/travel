from rest_framework import serializers
from auth.models import User, UserProfile


class UserS(serializers.ModelSerializer):

    role = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'role')
        extra_kwargs = {'password': {'write_only': True}}
