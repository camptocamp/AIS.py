# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""
import json
from os.path import dirname, join
import unittest

from vcr import VCR


def before_record_callback(request):
    """Replace confidential information in the recorded cassettes.

    - customer:key are replaced with 'X:Y'

    """
    payload = json.loads(request.body)
    payload['SignRequest']['OptionalInputs']['ClaimedIdentity']['Name'] = 'X:Y'
    request.body = json.dumps(payload)
    return request


my_vcr = VCR(
    serializer='json',
    record_mode='once',
    cassette_library_dir=join(dirname(__file__), 'cassettes'),
    path_transformer=VCR.ensure_suffix('.json'),
    before_record=before_record_callback
)


def fixture_path(filename):
    """Build the full path of a fixture file."""
    return join(dirname(__file__), 'fixtures', filename)


class BaseCase(unittest.TestCase):
    pass
