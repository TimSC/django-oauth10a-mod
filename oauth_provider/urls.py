# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from oauth_provider.compat import url

from .views import request_token, user_authorization, access_token

urlpatterns = [
    url(r'^request_token/$',    request_token,      name='oauth_request_token'),
    url(r'^authorize/$',        user_authorization, name='oauth_user_authorization'),
    url(r'^access_token/$',     access_token,       name='oauth_access_token'),
]
