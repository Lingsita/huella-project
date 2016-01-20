from rest_framework import permissions
from django.contrib.auth.models import User
from Empresas.models import Empleado


class IsBusinessAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        print('entro a has perm')
        try:
            if request.user:
                print(request.user)
                try:
                    empleado=Empleado.objects.get(usuario__user=request.user, is_admin=True, active=True)
                    print(empleado)
                    return True
                except Empleado.DoesNotExist:
                    return False
        except User.DoesNotExist:
            return False

        return False

class IsAdminOrBusinessAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        print('entro a has perm admin or badmin')
        try:
            if request.user:
                print(request.user)
                if request.user.is_superuser:
                    print('is superuser')

                    return True
                else:
                    try:
                        empleado=Empleado.objects.get(usuario__user=request.user, is_admin=True, active=True)

                        return True
                    except Empleado.DoesNotExist:
                        return False
        except User.DoesNotExist:
            return False

        return False