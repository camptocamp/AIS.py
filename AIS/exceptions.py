# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""


class AISError(Exception):
    pass


class AuthenticationFailed(AISError):
    pass


class UnknownAISError(AISError):
    pass


minor_to_exception = {
    'http://ais.swisscom.ch/1.0/resultminor/AuthenticationFailed':
    AuthenticationFailed,
}


def error_for(response):
    result = response.json()['SignResponse']['Result']

    Exc = minor_to_exception.get(result['ResultMinor'], UnknownAISError)
    return Exc(response)
