from django.middleware import csrf
from django.contrib import auth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from auth.models import UserProfile
from auth.forms import LoginForm
from auth.serializers import UserS, UserProfileS


@permission_classes([])
class LoginView(APIView):

    def post(self, request):
        form = LoginForm(request.data)
        if not form.is_valid():
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user = auth.authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        if user is None:
            return Response({'errors': {'email': ["Wrong email or password"]}},
                            status=status.HTTP_401_UNAUTHORIZED)

        # User found
        auth.login(request, user)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileS(profile)

        return Response({'success': "true", 'user': serializer.data}, status=status.HTTP_200_OK)


@authentication_classes([])
@permission_classes([])
class LogoutView(APIView):

    def post(self, request):
        auth.logout(request)
        return Response(status=status.HTTP_200_OK)


@permission_classes([])
class CSRFView(APIView):

    def get(self, request):
        return Response({'csrfmiddlewaretoken': csrf.get_token(request)}, status=status.HTTP_200_OK)
