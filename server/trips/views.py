from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes

from trips.models import Trip
from trips.serializers import TripS
from trips.forms import TripForm


class TripList(APIView):

    def get(self, request):
        trips = Trip.objects.filter(user=request.user)
        if request.query_params.get('all') and request.user.profile.is_admin():
            trips = Trip.objects.all().order_by('user')
        serializer = TripS(trips.order_by('start_date'), many=True)
        return Response({'trips': serializer.data})

    def post(self, request):
        form = TripForm(request.data.get('trip'))
        if not form.is_valid():
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
        new_trip = form.save(commit=False)
        new_trip.user = request.user
        new_trip.save()
        serializer = TripS(new_trip)
        return Response({'trip': serializer.data}, status=status.HTTP_201_CREATED)


class TripDetail(APIView):

    def _check_permissions(self, request, trip):
        if trip.user != request.user and not request.user.profile.is_admin():
            raise Http404  # we don't want them to find valid ids by brute force

    def get(self, request, id):
        trip = get_object_or_404(Trip, id=id)
        self._check_permissions(request, trip)
        serializer = TripS(trip)
        return Response({'trips': serializer.data})

    def put(self, request, id):
        trip = get_object_or_404(Trip, id=id)
        self._check_permissions(request, trip)
        form = TripForm(request.data.get('trip'), instance=trip)
        if not form.is_valid():
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
        trip = form.save()
        serializer = TripS(trip)
        return Response({'trip': serializer.data})

    def delete(self, request, id):
        trip = get_object_or_404(Trip, id=id)
        self._check_permissions(request, trip)
        trip.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

