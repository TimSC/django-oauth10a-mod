# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
from oauth_provider.compat import get_random_string
from oauth_provider.consts import SECRET_SIZE
import uuid

class TokenManager(models.Manager):
    def create_token(self, consumer, token_type, timestamp, scope,
            user=None, callback=None, callback_confirmed=False):
        """Shortcut to create a token with random key/secret."""
        token = self.create(consumer=consumer, 
                                            token_type=token_type, 
                                            timestamp=timestamp,
                                            scope=scope,
                                            user=user,
                                            callback=callback,
                                            callback_confirmed=callback_confirmed,
                                            key=uuid.uuid4().hex,
                                            secret=get_random_string(length=SECRET_SIZE))

        return token
