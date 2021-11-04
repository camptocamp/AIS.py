# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""
from .ais import AIS, Signature
from .pdf import PDF
from .exceptions import (
    AISError,
    AuthenticationFailed,
    UnknownAISError,
)

__all__ = ('AIS', 'Signature', 'PDF', 'AISError',
           'AuthenticationFailed', 'UnknownAISError')

__version__ = '0.3.0-beta'
