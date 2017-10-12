from django.conf.urls import url

from auth import views as auth_views


urlpatterns = [

    # Login
    url(r'login/$', auth_views.LoginView.as_view(), name='api_login'),
    url(r'logout/$', auth_views.LogoutView.as_view(), name='api_logout'),

    # CSRF
    url(r'csrf/token/$', auth_views.CSRFView.as_view(),
        name='api_csrf_token'),

    # Users
    url(r'users/$', auth_views.UserList.as_view(), name='api_users'),

]
