from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin


urlpatterns = [
    url(r'^django-admin/', admin.site.urls),  # admin shouldn't be on the default url

    url(r'^api/', include('travel.api_urls')),
]

