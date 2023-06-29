from django.urls import include, path

from services.api.api.urls import urlpatterns as api_urls

app_name = "api"

urlpatterns = [
    path("api/", include((api_urls, "api"), namespace="api")),
]
