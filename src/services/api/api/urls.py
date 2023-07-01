from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.api.views import (
    ActionViewSet,
    Check_balanceViewSet,
    TransferViewSet,
    UserCreateViewSet,
    login_view,
    logout_view
)

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register("action", ActionViewSet)
router_v1.register("transfer", TransferViewSet)


urlpatterns = [
    path("", include(router_v1.urls)),
    path(
        "check_balance/",
        Check_balanceViewSet.as_view({"get": "list"}),
        name="check_balance",
    ),
    path('sign-up/', UserCreateViewSet.as_view(), name="login"),
    path('login/', login_view),
    path('logout/', logout_view),
]
