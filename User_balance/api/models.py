from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField('Почта', unique=True, max_length=150)
    balance = models.PositiveIntegerField(
        ("Баланс"), default=0, editable=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username

    @classmethod
    def check_balance(cls, balance):
        if balance == 0:
            return balance
        reverse_to_rub = balance / 100
        return reverse_to_rub


class Action(models.Model):
    """Модель отслеживания пополнения баланса."""
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='actions'
    )


class Transfer(models.Model):
    """Модель перевода денег."""
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='from_user'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='to_user'
    )
    amount = models.PositiveIntegerField()
