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
    MissingPreparedSignature,
)

__all__ = ('AIS', 'Signature', 'PDF', 'AISError',
           'AuthenticationFailed', 'UnknownAISError',
           'MissingPreparedSignature')

__version__ = '0.2.0'
