from django.middleware import csrf
from django.contrib import auth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes

from auth.models import User, UserProfile
from auth.forms import LoginForm
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

    # def post(self, request, org_code):
    #     form = AddUserForm(request.data, initial={'org_code': org_code})
    #     if not form.is_valid():
    #         return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

    #     result = portal_ldap.create_user(**form.cleaned_data)
    #     if 'errors' in result:
    #         return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #     email = request.data['email']

    #     if 'success' in result:
    #         try:
    #             # Get the external portal to send out a welcome email
    #             notify_url = settings.PORTAL_EXTERNAL_API_URL + reverse('api_v1_new_account_created')
    #             requests.post(notify_url, data={'email': encrypt_string(email)})
    #         except Exception:
    #             log.exception("Couldn't send user welcome email")

    #     log.info("User created: %s | By: %s" % (email, request.user.email), request=request)
    #     return Response(result, status=status.HTTP_201_CREATED)


