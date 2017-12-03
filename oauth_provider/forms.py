# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django import forms


class AuthorizeRequestTokenForm(forms.Form):
    oauth_token = forms.CharField(widget=forms.HiddenInput)
    authorize_access = forms.BooleanField(required=False)
