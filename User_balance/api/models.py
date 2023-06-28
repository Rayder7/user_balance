from django.db import models
from django.contrib.auth.models import AbstractUser


# TODO: данная модель находитсяс в моделу API,
#  хотя относится к бизнес-логике "Пользователи системы",
#  а не в "AIP ссервис"
class User(AbstractUser):
    # TODO: docstring выглядит излишним, всё понятно из имени модели.
    #  Согласился бы, если бы ты отписал спецификку какую-то,
    #  а не просто перевод на русский.
    """Модель пользователя."""

    # TODO: регистрозависимая уникальность, школьники-хакеры будут рады.
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    # TODO: регистрозависимая уникальность
    email = models.EmailField('Почта', unique=True, max_length=150)
    balance = models.PositiveIntegerField(
        # TODO: взял в скобки строку, непонятна цель
        ("Баланс"), default=0, editable=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username

    # TODO: модели должны просто описывать таблицы БД,
    #  логику надо выносить отдельно. А еще нет типизации,
    #  раз задал планку выше в __str__(self) -> str:, то используй везде.
    @classmethod
    def check_balance(cls, balance):
        if balance == 0:
            return balance
        reverse_to_rub = balance / 100
        return reverse_to_rub


# TODO: Название модели звучик как "Действие", но ничего о перемещении денег.
class Action(models.Model):
    """Модель отслеживания пополнения баланса."""
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='actions'
    )


# TODO: тут лучше, но для того чтобы отобразить список действий  сбалансом,
#  у тебя идет явное деление на две сущности "пополлнение мной" и "перевод"
#  - возможно имело смысл сделать одну моделт и добавить тип операции.
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
    # TODO: а вот тут нет даты и времени операции, как есть у модели Action.
