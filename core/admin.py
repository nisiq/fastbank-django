"""
File admin django
"""

from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """ Define the admin pages for user """
    # Ordenar nossos usuários
    ordering = ['id']
    list_display = ['id', 'first_name', 'last_name', 'cpf']
    fieldsets = (
        # Paginas de Usuario
        (None, {'fields': ('email', 'password,')})
        (__('Personal info'), {'fields': ('first_name', 'last_name', 'cpf',)}),
        (
            ('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', 'created_at',)})
    )


    #Apenas leitura
    readonly_fields = ['last_login', 'created_at']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                # verificação de senha
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        })
    )


admin.site.register(models.User, UserAdmin)