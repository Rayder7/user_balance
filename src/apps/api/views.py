from django.db import transaction
from rest_framework import (status, viewsets, mixins,
                            permissions)
from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from apps.api.models import Action, Transfer
from apps.api.serializers import (
    UserSerializer,
    UserCreateSerializer,
    ActionSerializer,
    TransferSerializer,
)

User = get_user_model()


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'})
    else:
        return Response({'message': 'Invalid login credentials'}, status=401)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful'})


class UserCreateViewSet(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)


class Check_balanceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        # TODO: `users` переменная содержит 1 элемент, значит `user`.
        users = request.user
        balance = users.balance
        #  balance_rub = User.check_balance(balance)
        # TODO: так как это API, то нужно возвращать JSON:
        #  {"balance": balance_rub}. Также непонятно зачем ты приводишь
        #  баланс к int внутри форматирования строки.
        message = f"Ваш баланс равен {int(balance)} рублей"

        return Response(message)


class ActionViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = ActionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Action.objects.all()

    def get_queryset(self):
        # TODO: некорретная фильтрация?
        # username имеет тип CharField
        # self.request.user имеет тип User
        users = User.objects.filter(username=self.request.user)
        return self.queryset.filter(user__in=users)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # TODO: у тебя уже есть request.user, зачем еще
            #  фильтровать по username, а потом еще и пл pk?
            user = User.objects.filter(username=self.request.user).get(
                pk=self.request.data["user"]
            )
        except Exception:
            content = {"error": "нет такого юзера"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransferViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = TransferSerializer
    #  authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transfer.objects.all()

    def make_transfer(self, from_user, to_user, amount):
        if from_user.balance < amount:
            raise (ValueError("Недостаточно денег на счету"))
        if from_user == to_user:
            raise (ValueError("Нельзя отправить деньги себе"))

        with transaction.atomic():
            from_balance = from_user.balance - amount
            from_user.balance = from_balance
            from_user.save()

            # TODO: опасный блок. теоретичесски, если в БД у меня будет
            #  None в балансе, то формула упадет. А операций выше с первым
            #  юзером уже прошла устпешно- начислили просто так недег из
            #  ниоткуда.
            to_balance = to_user.balance + amount
            to_user.balance = to_balance
            to_user.save()

            # TODO: если произошла ошибка сети, то запись в историю не попадет,
            #  а деньги уже перевелись.
            transfer = Transfer.objects.create(
                from_user=from_user, to_user=to_user, amount=amount
            )
        return transfer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.make_transfer(**serializer.validated_data)
        except ValueError:
            content = {"error": "Недостаточно денег"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = User.objects.filter(username=self.request.user)
        return self.queryset.filter(from_user__in=user)
