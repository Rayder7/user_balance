# Generated by Django 4.2.1 on 2023-07-06 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0002_alter_transaction_type_oper"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="participant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="participants",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
