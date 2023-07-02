from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
)
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.models import Transaction
from apps.api.serializers import (
    DepositSerializer,
    TransferSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from apps.api.services import make_deposit, make_transfer

User = get_user_model()


@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Login successful"})
    else:
        return Response({"message": "Invalid login credentials"}, status=401)


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"message": "Logout successful"})


class UserCreateViewSet(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)


class Check_balanceViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=request.user.id)
        serializer = UserSerializer(user)
        data = serializer.data
        username = data["username"]
        balance = data["balance"]
        message = f"Баланс пользователя {username} равен {balance} рублей"

        return Response({"message": message})


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
