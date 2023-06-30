from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# TODO: Название модели звучик как "Действие", но ничего о перемещении денег.
class Action(models.Model):
    """Модель отслеживания пополнения баланса."""

    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="actions"
    )


# TODO: тут лучше, но для того чтобы отобразить список действий  сбалансом,
#  у тебя идет явное деление на две сущности "пополлнение мной" и "перевод"
#  - возможно имело смысл сделать одну моделт и добавить тип операции.
class Transfer(models.Model):
    """Модель перевода денег."""

    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="from_user"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="to_user"
    )
    amount = models.PositiveIntegerField()
    # TODO: а вот тут нет даты и времени операции, как есть у модели Action.
