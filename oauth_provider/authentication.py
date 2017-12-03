# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from rest_framework import authentication
from rest_framework import exceptions
from .decorators import DoOAuthCheck

class OAuthAuthentication(authentication.BaseAuthentication):
    """
    Allows access only to OAuth authenticated users.
    """

    def authenticate(self, request):
        if 'Authorization' not in request.META and 'HTTP_AUTHORIZATION' not in request.META:
            return None

        ok, err_view, token_user = DoOAuthCheck(request, None)
        if not ok:
            raise exceptions.AuthenticationFailed()

        return (token_user, None)

