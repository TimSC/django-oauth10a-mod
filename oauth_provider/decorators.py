# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import oauth10a as oauth

try:
    from functools import update_wrapper
except ImportError:
    from django.utils.functional import update_wrapper  # Python 2.3, 2.4 fallback.

from oauth_provider.compat import gettext_lazy as _

from .responses import *
from .utils import initialize_server_request, send_oauth_error, get_oauth_request, verify_oauth_request
from .consts import OAUTH_PARAMETERS_NAMES
from .store import get_store_singleton, InvalidTokenError, InvalidConsumerError
from functools import wraps

def DoOAuthCheck(request, scope_name, *args, **kwargs):
    oauth_request = get_oauth_request(request)
    if oauth_request is None:
        return False, GetInvalidParamsResponse(), None

    try:
        consumer = get_store_singleton().get_consumer(request, oauth_request, oauth_request['oauth_consumer_key'])
    except InvalidConsumerError:
        return False, GetInvalidConsumerResponse(), None

    try:
        token = get_store_singleton().get_access_token(request, oauth_request, consumer, oauth_request.get_parameter('oauth_token'))
    except InvalidTokenError:
        return False, send_oauth_error(oauth.Error(_('Invalid access token: %s') % oauth_request.get_parameter('oauth_token'))), None

    if not verify_oauth_request(request, oauth_request, consumer, token):
        return False, GetCouldNotVerifyOAuthRequestResponse(), None

    if bool(scope_name) and (not token.scope
                            or token.scope.name != scope_name):
        return False, GetInvalidScopeResponse(), None

    return True, None, token.user

class CheckOauth(object):
    """
    Decorator that checks that the OAuth parameters passes the given test, raising
    an OAuth error otherwise. If the test is passed, the view function
    is invoked.

    We use a class here so that we can define __get__. This way, when a
    CheckOAuth object is used as a method decorator, the view function
    is properly bound to its instance.
    """
    def __init__(self, scope_name=None):
        self.scope_name = scope_name

    def __new__(cls, arg=None):
        if not callable(arg):
            return super(CheckOauth, cls).__new__(cls)
        else:
            obj =  super(CheckOauth, cls).__new__(cls)
            obj.__init__()
            return obj(arg)

    def __call__(self, view_func):

        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            ok, err_view, token_user = DoOAuthCheck(request, self.scope_name, *args, **kwargs)
            if not ok:
                return err_view
            if token_user:
                request.user = token_user
            return view_func(request, *args, **kwargs)

        return wrapped_view


oauth_required = CheckOauth
