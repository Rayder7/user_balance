from django.contrib import admin

from apps.api.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "participant",
        "amount",
        "date",
        "type_oper",
    )
    search_fields = ("user",)
    list_filter = ("type_oper",)
    ordering = ("-id",)
    empty_value_display = "-пусто-"


admin.site.register(Transaction, TransactionAdmin)
