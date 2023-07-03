from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Transaction(models.Model):
    class TypeOper(models.TextChoices):
        DEPOSIT = "DP", _("deposit")
        TRANSFER = "TR", _("transfer")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transaction_from"
    )
    participant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="participants",
        null=True,
        blank=True,
    )
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    type_oper = models.CharField(choices=TypeOper.choices,
                                 default=TypeOper.DEPOSIT,
                                 max_length=20)

    def __str__(self) -> str:
        return f"{self.amount}"
