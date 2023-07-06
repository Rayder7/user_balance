from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularRedocView, 
                                   SpectacularSwaggerView)

from services.api.api.urls import urlpatterns as api_urls

app_name = "api"

urlpatterns = [
    path("api/", include((api_urls, "api"), namespace="api")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='api:schema'),
         name='swagger-ui'),
    path('api/redoc/',
         SpectacularRedocView.as_view(url_name='api:schema'),
         name='redoc'),
]
