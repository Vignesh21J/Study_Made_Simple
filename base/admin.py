from django.contrib import admin

from .models import User

from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ['email', 'name', 'is_staff', 'is_active', 'date_joined']
    ordering = ('email',)
    search_fields = ('email', 'name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'bio')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )

