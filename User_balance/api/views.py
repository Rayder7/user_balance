from django.db import transaction
from djoser.views import UserViewSet
from rest_framework import status, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Action, Transfer, User
from .serializers import UserSerializer, ActionSerializer, TransferSerializer


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def get_self_page(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Check_balanceViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        users = request.user
        balance = users.balance
        balance_rub = User.check_balance(balance)
        message = f"Ваш баланс равен {int(balance_rub)} рублей"

        return Response(message)


class ActionViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    serializer_class = ActionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Action.objects.all()

    def get_queryset(self):
        users = User.objects.filter(username=self.request.user)
        return self.queryset.filter(user__in=users)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.filter(
                username=self.request.user).get(pk=self.request.data['user'])
        except Exception:
            content = {'error': 'нет такого юзера'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransferViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin):

    serializer_class = TransferSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Transfer.objects.all()

    def make_transfer(self, from_user, to_user, amount):
        if from_user.balance < amount:
            raise (ValueError('Недостаточно денег на счету'))
        if from_user == to_user:
            raise (ValueError('Нельзя отправить деньги себе'))

        with transaction.atomic():
            from_balance = from_user.balance - amount
            from_user.balance = from_balance
            from_user.save()

            to_balance = to_user.balance + amount
            to_user.balance = to_balance
            to_user.save()

            transfer = Transfer.objects.create(
                from_user=from_user,
                to_user=to_user,
                amount=amount)
        return transfer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.make_transfer(**serializer.validated_data)
        except ValueError:
            content = {'error': 'Недостаточно денег'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = User.objects.filter(username=self.request.user)
        return self.queryset.filter(from_user__in=user)
