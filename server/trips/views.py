from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes

from auth.models import UserProfile
from trips.models import Trip
from trips.serializers import TripS
from trips.forms import TripForm


class TripList(APIView):

    def get(self, request):
        trips = Trip.objects.order_by('start_date')
        if request.user.profile.role != UserProfile.ADMIN:
            trips = trips.filter(user=request.user)
        serializer = TripS(trips, many=True)
        return Response({'trips': serializer.data})

    def post(self, request):
        form = TripForm(request.data)
        if not form.is_valid():
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
        new_trip = form.save(commit=False)
        new_trip.user = request.user
        new_trip.save()
        serializer = TripS(new_trip)
        return Response({'trip': serializer.data}, status=status.HTTP_201_CREATED)