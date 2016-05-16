# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""


class AISError(Exception):
    """Generic AIS Error."""

    pass


class AuthenticationFailed(AISError):
    """Authentication with AIS failed.

    This means that AIS returned
    http://ais.swisscom.ch/1.0/resultminor/AuthenticationFailed
    """

    pass


class UnknownAISError(AISError):
    """Unknown AIS Error."""

    pass


class MissingPreparedSignature(AISError):
    """The PDF file needs to be prepared with an empty signature."""
    pass


minor_to_exception = {
    'http://ais.swisscom.ch/1.0/resultminor/AuthenticationFailed':
    AuthenticationFailed,
}


def error_for(response):
    """Return the correct error for a response."""
    result = response.json()['SignResponse']['Result']

    Exc = minor_to_exception.get(result['ResultMinor'], UnknownAISError)
    return Exc(result)
