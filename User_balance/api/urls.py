from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'


urlpatterns = [
    #  path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]