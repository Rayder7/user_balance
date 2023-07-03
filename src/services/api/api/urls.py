from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.views import (
    CheckBalanceViewSet,
    DepositViewSet,
    TransferViewSet,
    UserCreateViewSet,
    LoginApiView,
    logout_view,
)

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register("transfer", TransferViewSet, basename="transfer")
router_v1.register("deposit", DepositViewSet, basename="deposit")


urlpatterns = [
    path(
        "balance/",
        CheckBalanceViewSet.as_view(),
        name="balance",
    ),
    path("balance/", include(router_v1.urls)),
    path("sign-up/", UserCreateViewSet.as_view(), name="register"),
    path("login/", LoginApiView.as_view()),
    path("logout/", logout_view),
]
