from django.contrib import admin

from apps.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email',
    )
    search_fields = ('username',)
    list_filter = ('username', 'email')
    ordering = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
