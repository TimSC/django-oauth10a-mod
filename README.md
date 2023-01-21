[![Build Status](https://travis-ci.org/TimSC/django-oauth10a-mod.svg?branch=master)](https://travis-ci.org/TimSC/django-oauth10a-mod)

django-oauth10a-mod
===================

The [OAuth 1.0a](https://oauth.net/core/1.0a/) protocol enables websites or applications (Consumers) to access Protected Resources from a web service (Service Provider) via an API, without requiring Users to disclose their Service Provider credentials to the Consumers. More generally, OAuth 1.0a creates a freely-implementable and generic methodology for API authentication.

django-oauth-plus-mod features two authentication flows:

* three-legged OAuth
* xAuth (twitter xAuth)

Depends on: 

* [python-oauth10a](https://github.com/TimSC/python-oauth10a)
* django 1.8-4
* Python 3

This project was forked from [django-oauth-plus](https://bitbucket.org/david/django-oauth-plus) by David Larlet et al.

# Installing

From pypi:

    $ pip install django-oauth10a-mod

From source:

    $ python setup.py install
    
We recommend using [virtualenv](https://virtualenv.pypa.io/en/latest/).

# Running tests
You can run tests using the following at the command line:

    $ tox


