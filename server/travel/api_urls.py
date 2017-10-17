from django.conf.urls import url

from auth import views as auth_views
from trips import views as trip_views


urlpatterns = [

    # Login
    url(r'login/$', auth_views.LoginView.as_view(), name='api_login'),
    url(r'logout/$', auth_views.LogoutView.as_view(), name='api_logout'),

    # CSRF
    url(r'csrf/token/$', auth_views.CSRFView.as_view(),
        name='api_csrf_token'),

    # Users
    url(r'users/$', auth_views.UserList.as_view(), name='api_users'),
    url(r'users/(?P<id>[0-9]+)/$', auth_views.UserList.as_view(), name='api_users'),

    # Passwords
    url(r'password/reset/$', auth_views.PasswordResetView.as_view()),
    url(r'password/set/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view()),

    # Trips
    url(r'trips/$', trip_views.TripList.as_view(), name='api_trips'),
    url(r'trips/(?P<id>[0-9]+)/$', trip_views.TripDetail.as_view(), name='api_trip'),

]
