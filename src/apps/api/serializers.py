from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from apps.api.models import Transaction
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'balance')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("id", "user", "participant", "amount", "date",
                  "type_oper")
        read_only_fields = ("date",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "request" in self.context:
            self.fields["user"].queryset = self.fields["user"].queryset.filter(
                username=self.context["view"].request.user.username
            )

    def validate(self, data):
        try:
            data["user"] = User.objects.get(username=data["user"])
        except Exception:
            raise serializers.ValidationError("Нет такого пользователя")
        return data
