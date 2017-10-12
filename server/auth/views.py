from django.middleware import csrf
from django.contrib import auth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes

from auth.models import User, UserProfile
from auth.forms import LoginForm, AddUserForm
from auth.serializers import UserS
from auth.permissions import IsUserManager


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
        serializer = UserS(user)

        return Response({'success': "true", 'user': serializer.data}, status=status.HTTP_200_OK)


@permission_classes([])
class LogoutView(APIView):

    def post(self, request):
        auth.logout(request)
        return Response(status=status.HTTP_200_OK)


@permission_classes([])
class CSRFView(APIView):

    def get(self, request):
        return Response({'csrfmiddlewaretoken': csrf.get_token(request)}, status=status.HTTP_200_OK)


@permission_classes([IsUserManager])
class UserList(APIView):

    def get(self, request):
        users = User.objects.all().select_related('profile')
        serializer = UserS(users, many=True)
        return Response({
            'users': serializer.data,
        })

    def post(self, request):
        form = AddUserForm(request.data.get('user', {}), user=request.user)
        if not form.is_valid():
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = User(
            username=form.cleaned_data['email'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            is_active=True,
        )
        user.save()  # should trigger profile creation

        user.profile.role = form.cleaned_data['role']
        user.profile.save()

        return Response({}, status=status.HTTP_201_CREATED)


