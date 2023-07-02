from apps.api.models import Transaction
from django.db import transaction


def make_transfer(user, participant, amount, type_oper):
    if type_oper == 'deposit':
        if amount <= 0:
            raise (ValueError("Платеж должен быть больше 0"))
        print(participant)
        if participant is not None:
            raise (ValueError("Выберите тип операции 'transfer'"))

        with transaction.atomic():
            balance = user.balance + amount
            user.balance = balance
            user.save()

            transfer = Transaction.objects.create(
                user=user, participant=None, amount=amount,
                type_oper=type_oper
            )

        return transfer

    if type_oper == "transfer":
        if user.balance < amount:
            raise (ValueError("Недостаточно денег на счету"))
        if amount <= 0:
            raise (ValueError("Платеж должен быть больше 0"))
        if user == participant:
            raise (ValueError("Выберите тип операции 'deposit'"))
        if participant is None:
            raise (ValueError("Выбери кому вы хотите отправить деньги"))

        with transaction.atomic():
            from_balance = user.balance - amount
            user.balance = from_balance
            user.save()

            to_balance = participant.balance + amount
            participant.balance = to_balance
            participant.save()

            transfer = Transaction.objects.create(
                user=user, participant=participant, amount=amount,
                type_oper=type_oper
            )
            transfer = Transaction.objects.create(
                user=participant, participant=user, amount=-amount,
                type_oper=type_oper
            )

        return transfer
