from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.api.views import (
    Check_balanceViewSet,
    TransactionViewSet,
    UserCreateViewSet,
    login_view,
    logout_view
)

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register("transaction", TransactionViewSet)


urlpatterns = [
    path("", include(router_v1.urls)),
    path(
        "balance/",
        Check_balanceViewSet.as_view({"get": "retrieve"}),
        name="balance",
    ),
    path('sign-up/', UserCreateViewSet.as_view(), name="login"),
    path('login/', login_view),
    path('logout/', logout_view),
]
