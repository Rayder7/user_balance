from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.views import (
    Check_balanceViewSet,
    DepositViewSet,
    TransferViewSet,
    UserCreateViewSet,
    login_view,
    logout_view,
)

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register("transfer", TransferViewSet, basename="transfer")
router_v1.register("deposit", DepositViewSet, basename="deposit")


urlpatterns = [
    path(
        "balance/",
        Check_balanceViewSet.as_view({"get": "retrieve"}),
        name="balance",
    ),
    path("balance/", include(router_v1.urls)),
    path("sign-up/", UserCreateViewSet.as_view(), name="register"),
    path("login/", login_view),
    path("logout/", logout_view),
]
