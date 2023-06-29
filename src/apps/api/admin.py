from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "balance", "email")
    search_fields = ("username",)
    list_filter = ("username", "email")
    ordering = ("username",)
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
