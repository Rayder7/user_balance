from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        'api/auth/', include('rest_framework.urls', namespace='rest_framework')
    ),
    path("", include("services.api.urls")),
]
