from django.middleware import csrf
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes

from auth.models import User, UserProfile
from auth.forms import LoginForm, AddUserForm, UserForm, PasswordResetForm, PasswordConfirmForm
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


def reset_password_for(email):
    reset_form = PasswordResetForm({'email': email})
    if reset_form.is_valid():
        reset_form.save(
            use_https=False,
            domain_override='localhost:4200',
            from_email='travel-planner@gmail.com',
            email_template_name='auth/password_email.html',
            subject_template_name='auth/password_subject.txt',
        )
    return reset_form


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

        # Send password set email
        reset_password_for(user.email)

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


@permission_classes([])
class PasswordResetView(APIView):

    def post(self, request):

        form = reset_password_for(request.data.get('email'))
        if not form.is_valid():
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': "Email with a password reset link "
                                    "has been sent to your email address. "
                                    "Please check your email."})


@permission_classes([])
class PasswordResetConfirmView(APIView):

    error_link_is_invalid = ("The password reset link was invalid, possibly because it "
                             "has already been used. Please request a new password reset.")

    def _get_user_from_reset_link(self, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            UserProfile.objects.update_or_create(user=user)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is None or not default_token_generator.check_token(user, token):
            return None
        else:
            return user

    def get(self, request, uidb64, token):
        """
        Allows the frontend app to find out whether the reset link is valid
        """
        if self._get_user_from_reset_link(uidb64, token) is not None:
            return Response({'valid': 'true'}, status=status.HTTP_200_OK)
        else:
            return Response({'valid': 'false', 'error': self.error_link_is_invalid},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uidb64, token):
        """
        Changes user's password provided the uid and token are correct
        """
        user = self._get_user_from_reset_link(uidb64, token)
        if not user:
            return Response({'errors': {'__all__': [self.error_link_is_invalid]}},
                            status=status.HTTP_400_BAD_REQUEST)

        form = PasswordConfirmForm(request.data)
        if not form.is_valid():
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Change password - this will make the link invalid
            user.set_password(form.cleaned_data['password'])
            user.save()
        except Exception:
            return Response({'errors': {'__all__': ['Server error. Please contact system administrator']}},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': ["Password has been set successfully"]},
                        status=status.HTTP_200_OK)
