from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


TYPE_OPER_CHOICES = (
    ("deposit", "DEPOSIT"),
    ("transfer", "TRANSFER"),
)


class Transaction(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transaction_from"
    )
    participant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transaction_to",
        null=True,
        blank=True,
    )
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    type_oper = models.CharField(choices=TYPE_OPER_CHOICES, default="deposit")

    def __str__(self) -> str:
        return (
            f"Пользователь {self.user} сделал {self.type_oper}"
            f"на {self.amount} {self.participant}"
        )
