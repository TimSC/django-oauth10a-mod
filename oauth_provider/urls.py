# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from oauth_provider.compat import re_path

from .views import request_token, user_authorization, access_token

urlpatterns = [
    re_path(r'^request_token/$',    request_token,      name='oauth_request_token'),
    re_path(r'^authorize/$',        user_authorization, name='oauth_user_authorization'),
    re_path(r'^access_token/$',     access_token,       name='oauth_access_token'),
]
