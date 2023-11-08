from rest_framework import permissions


class IsCreationOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action == 'create':
                return True

            else:
                return False
        else:
            return True


    """
    verificação, se o usuario não estiver logado, mas tentando criar: autoriza, se não, não
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            if view.action == 'create':
                return True

            else:
                return False
        else:
            return True


# Autenticação: JWT
# Autorização: Ou estar logado/autenticado, ou estar criando