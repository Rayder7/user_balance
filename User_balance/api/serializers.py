import djoser.serializers
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Action, Transfer, User


class UserSerializer(djoser.serializers.UserSerializer):
    """ Сериализатор пользователя """
    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'balance')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class UserCreateSerializer(djoser.serializers.UserCreateSerializer):
    """ Сериализатор создания пользователя """

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password', 'balance')


class ActionSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        # TODO: для pytho 3 просто super()....
        super(ActionSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['user'].queryset = (
                self.fields['user'].queryset.filter(
                    username=self.context['view'].request.user)
            )

    class Meta:
        model = Action
        fields = ('id', 'user', 'amount', 'date')
        # TODO: если не ошибаюсь, id итак read_only.
        read_only_fields = ('id', 'date')

    def create(self, validated_data):
        if validated_data['user'].balance + validated_data['amount'] > 0:
            validated_data['user'].balance += validated_data['amount']
            validated_data['user'].save()
        else:
            raise serializers.ValidationError(
                ('отсутствует сумма пополнения')
            )

        return super(ActionSerializer, self).create(validated_data)


class TransferSerializer(serializers.ModelSerializer):
    # TODO: не очень понимаю, почему to_user / from_userr имеют разные имплементации.
    to_user = serializers.CharField()
    from_user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    # TODO: где это используется?
    def get_from_user(self, obj):
        return obj.from_user.username

    def __init__(self, *args, **kwargs):
        super(TransferSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['from_user'].queryset = (
                self.fields['from_user'].queryset.filter(
                    username=self.context['request'].user.username)
            )

    def validate(self, data):
        try:
            data['to_user'] = User.objects.get(username=data['to_user'])
        except Exception:
            raise serializers.ValidationError(
                "Нет такого пользователя")
        return data

    class Meta:
        model = Transfer
        fields = ('id', 'from_user', 'to_user', 'amount')
        read_only_fields = ('id', )
