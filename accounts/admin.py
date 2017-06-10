from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import RdxUser
from .forms import *


# Register your models here.
class UserAdmin(BaseUserAdmin):
    """
    User Model for Sarvam
    This is use only for Django admin
    """
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'mobile')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'is_admin', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (
             None, {
                 'classes': ('wide',),
                 'fields': ('email', 'username', 'mobile', 'password')
             }
        ),
    )

    form = RdxUserChangeForm
    add_form = RegisterUserForm

    list_display = ('id', 'email', 'mobile_number', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'id',)
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)
