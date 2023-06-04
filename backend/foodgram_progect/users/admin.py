from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from .models import User

# admin.site.register(User, UserAdmin)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    list_filter = (
        'username',
        'email',
    )
