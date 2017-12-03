from __future__ import unicode_literals

from rest_framework import permissions
from .decorators import DoOAuthCheck

class IsOAuth(permissions.BasePermission):
    """
    Allows access only to OAuth authenticated users.
    """

    def has_permission(self, request, view):
        ok, err_view = DoOAuthCheck(request, None, view)
        return ok

