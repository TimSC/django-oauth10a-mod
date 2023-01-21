# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from oauth_provider.compat import gettext_lazy as _
from django.http import HttpResponseBadRequest

import oauth10a as oauth

from oauth_provider.utils import send_oauth_error

#INVALID_PARAMS_RESPONSE = send_oauth_error(oauth.Error(_('Invalid request parameters.')))
#INVALID_CONSUMER_RESPONSE = HttpResponseBadRequest('Invalid Consumer.')
#INVALID_SCOPE_RESPONSE = send_oauth_error(oauth.Error(_('You are not allowed to access this resource.')))
#COULD_NOT_VERIFY_OAUTH_REQUEST_RESPONSE = send_oauth_error(oauth.Error(_('Could not verify OAuth request.')))

def GetInvalidParamsResponse():
	return send_oauth_error(oauth.Error(_('Invalid request parameters.')))
def GetInvalidConsumerResponse():
	return HttpResponseBadRequest('Invalid Consumer.')
def GetInvalidScopeResponse():
	return send_oauth_error(oauth.Error(_('You are not allowed to access this resource.')))
def GetCouldNotVerifyOAuthRequestResponse():
	return send_oauth_error(oauth.Error(_('Could not verify OAuth request.')))

