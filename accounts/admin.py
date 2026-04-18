from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'date_joined']
    list_filter = ['role']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('role', 'phone', 'bio')}),
    )
