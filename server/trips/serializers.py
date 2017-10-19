from rest_framework import serializers
from trips.models import Trip


class TripS(serializers.ModelSerializer):

    user_id = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = '__all__'
        depth = 0

    def get_user_id(self, obj):
        return obj.user_id

    def get_user_email(self, obj):
        return obj.user.email
