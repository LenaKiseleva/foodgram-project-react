from django.contrib import admin

from users.models import Subscribe, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'password')


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
