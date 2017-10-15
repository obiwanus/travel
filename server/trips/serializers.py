from rest_framework import serializers
from trips.models import Trip


class TripS(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = '__all__'
        depth = 0
