from django.middleware import csrf
from django.contrib import auth
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes

from auth.models import User, UserProfile
from auth.forms import LoginForm, AddUserForm, UserForm
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

    def get(self, request, id=None):
        if id is None:
            users = User.objects.all().select_related('profile').order_by('id')
            serializer = UserS(users, many=True)
            return Response({
                'users': serializer.data,
            })
        else:
            user = get_object_or_404(User, id=id)
            serializer = UserS(user)
            return Response({
                'user': serializer.data,
            })

    def post(self, request, id=None):
        if id is not None:
            raise Http404
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

        serializer = UserS(user)
        return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        user = get_object_or_404(User, id=id)

        initial = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.profile.role,
        }
        form = UserForm(request.data.get('user', {}), initial=initial, user=request.user)
        if not form.is_valid():
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        user.profile.role = form.cleaned_data.pop('role')
        user.profile.save()
        user.__dict__.update(form.cleaned_data)
        user.save()

        serializer = UserS(user)
        return Response({'user': serializer.data})

    def delete(self, request, id):
        user = get_object_or_404(User, id=id)

        if user.role == UserProfile.ADMIN and request.user.profile.role != UserProfile.ADMIN:
            return Response({'errors': ['Insufficient permissions to delete user']},
                            status=status.HTTP_403_FORBIDDEN)

        if user.pk == request.user.pk:
            return Response({'errors': ['You cannot delete yourself']},
                            status=status.HTTP_403_FORBIDDEN)

        user.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

