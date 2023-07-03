from django.contrib.auth import get_user_model, login, logout
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
)
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.models import Transaction
from apps.api.serializers import (
    DepositSerializer,
    TransferSerializer,
    LoginSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from apps.api.services import make_deposit, make_transfer

User = get_user_model()


class LoginApiView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        login(request, user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"message": "Logout successful"})


class UserCreateViewSet(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)


class CheckBalanceViewSet(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        balance = request.user.balance
        return Response({"balance": balance})


class TransferViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = TransferSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            make_transfer(**serializer.validated_data)
        except ValueError:
            content = {"error": "Операция невыполнена, ОШИБКА в запросе"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = User.objects.filter(username=self.request.user.username)
        return self.queryset.filter(user__in=user, type_oper="transfer")


class DepositViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = DepositSerializer

    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            make_deposit(**serializer.validated_data)
        except ValueError:
            content = {"error": "Сумма пополнения должна быть больше 0"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = User.objects.filter(username=self.request.user.username)
        return self.queryset.filter(user__in=user, type_oper="deposit")
