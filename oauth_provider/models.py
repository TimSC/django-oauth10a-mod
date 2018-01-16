# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import sys
import urllib
if sys.version_info.major < 3: 
	import urlparse
	from urllib import urlencode
else:
	import urllib.parse as urlparse
	from urllib.parse import urlencode
from time import time
import warnings
import oauth10a as oauth
from django.db import models

from oauth_provider.compat import AUTH_USER_MODEL
from oauth_provider.managers import TokenManager
from oauth_provider.consts import KEY_SIZE, SECRET_SIZE, CONSUMER_KEY_SIZE, CONSUMER_STATES,\
    PENDING, VERIFIER_SIZE, MAX_URL_LENGTH, OUT_OF_BAND
from oauth_provider.utils import check_valid_callback


class Nonce(models.Model):
    token_key = models.CharField(max_length=KEY_SIZE)
    consumer_key = models.CharField(max_length=CONSUMER_KEY_SIZE)
    key = models.CharField(max_length=255, primary_key=True)
    timestamp = models.PositiveIntegerField(db_index=True)
    
    def __unicode__(self):
        return u"Nonce %s for %s" % (self.key, self.consumer_key)


class Scope(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    url = models.TextField(max_length=MAX_URL_LENGTH)
    is_readonly = models.BooleanField(default=True)

    def __unicode__(self):
        return u"Resource %s with url %s" % (self.name, self.url)


class Resource(Scope):

    def __init__(self, *args, **kwargs):
        warnings.warn("oauth_provider.Resource model is deprecated, use oauth_provider.Scope instead", DeprecationWarning)
        super(Resource, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True


class Consumer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    key = models.CharField(max_length=CONSUMER_KEY_SIZE, primary_key=True)
    secret = models.CharField(max_length=SECRET_SIZE, blank=True)

    status = models.SmallIntegerField(choices=CONSUMER_STATES, default=PENDING)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    xauth_allowed = models.BooleanField("Allow xAuth", default = False)
        
    def __unicode__(self):
        return u"Consumer %s with key %s" % (self.name, self.key)

def default_token_timestamp():
    if sys.version_info.major < 3: 
        return long(time())
    else:
        return int(time())

class Token(models.Model):
    REQUEST = 1
    ACCESS = 2
    TOKEN_TYPES = ((REQUEST, u'Request'), (ACCESS, u'Access'))
    
    key = models.CharField(max_length=KEY_SIZE, primary_key=True, default='')
    secret = models.CharField(max_length=SECRET_SIZE, null=True, blank=True)
    token_type = models.SmallIntegerField(choices=TOKEN_TYPES)
    timestamp = models.IntegerField(default=default_token_timestamp)
    is_approved = models.BooleanField(default=False)
    
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='tokens', db_index=True)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    scope = models.ForeignKey(Scope, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def resource(self):
        return self.scope

    @resource.setter
    def resource(self, value):
        self.scope = value

    ## OAuth 1.0a stuff
    verifier = models.CharField(max_length=VERIFIER_SIZE)
    callback = models.CharField(max_length=MAX_URL_LENGTH, null=True, blank=True)
    callback_confirmed = models.BooleanField(default=False)
    
    objects = TokenManager()
    
    def __unicode__(self):
        return u"%s Token %s for %s" % (self.get_token_type_display(), self.key, self.consumer)

    def to_string(self, only_key=False):
        token_dict = {
            'oauth_token': self.key, 
            'oauth_token_secret': self.secret,
            'oauth_callback_confirmed': self.callback_confirmed and 'true' or 'error'
        }
        if self.verifier:
            token_dict['oauth_verifier'] = self.verifier

        if only_key:
            del token_dict['oauth_token_secret']
            del token_dict['oauth_callback_confirmed']

        return urlencode(token_dict)

    def get_callback_url(self, args=None):
        """
        OAuth 1.0a, append the oauth_verifier.
        """
        if self.callback and self.verifier:
            parts = urlparse.urlparse(self.callback)
            scheme, netloc, path, params, query, fragment = parts[:6]
            if query:
                query = '%s&oauth_verifier=%s' % (query, self.verifier)
            else:
                query = 'oauth_verifier=%s' % self.verifier

            # workaround for non-http scheme urlparse problem in py2.6 (issue #2)
            if "?" in path:
                query = "%s&%s" % (path.split("?")[-1], query)
                path = "?".join(path[:-1])

            if args is not None:
                query += "&%s" % urlencode(args)
            return urlparse.urlunparse((scheme, netloc, path, params,
                query, fragment))
        args = args is not None and "?%s" % urlencode(args) or ""
        return self.callback and self.callback + args

    def set_callback(self, callback):
        if callback not in OUT_OF_BAND: # out of band, says "we can't do this!"
            if check_valid_callback(callback):
                self.callback = callback
                self.callback_confirmed = True
                self.save()
            else:
                raise oauth.Error('Invalid callback URL.')
        
