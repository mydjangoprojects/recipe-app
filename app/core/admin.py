from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from .forms import CustomUserChangeForm, CustomUserCreationForm


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name']
    model = User
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)
