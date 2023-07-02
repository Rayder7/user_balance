from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField("Почта", unique=True, max_length=150)
    balance = models.PositiveIntegerField(
        "Баланс",
        default=0,
        editable=False,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                Lower("username"), name="unique_lowered_username"
            ),
            models.UniqueConstraint(
                Lower("email"), name="unique_lowered_email"
            )
        ]

    def __str__(self) -> str:
        return self.username
