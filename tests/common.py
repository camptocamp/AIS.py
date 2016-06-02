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
from vcr.serializers import jsonserializer

from AIS import helpers


class JSONSerializer(object):
    """ Override default json serializer to fix PY3 vcr encoding mistake.
    """

    @staticmethod
    def fix_value_encoding(value):
        if isinstance(value, dict):
            return JSONSerializer.fix_dict_encoding(value)
        elif isinstance(value, list):
            return [JSONSerializer.fix_value_encoding(val) for val in value]
        elif isinstance(value, bytes):
            return value.decode('utf8')
        else:
            return value

    @staticmethod
    def fix_dict_encoding(dict_to_fix):
        """ Return a copy of *dict_to_fix* with bytes transform to str.

        :type dict_to_fix: dict
        :rtype: dict
        """
        return {
            key: JSONSerializer.fix_value_encoding(value)
            for key, value in dict_to_fix.items()
        }

    @staticmethod
    def serialize(cassette_dict):
        cassette_dict = JSONSerializer.fix_dict_encoding(cassette_dict)
        return jsonserializer.serialize(cassette_dict)

    @staticmethod
    def deserialize(cassette_string):
        return jsonserializer.deserialize(cassette_string)


def before_record_callback(request):
    """Replace confidential information in the recorded cassettes.

    - customer:key are replaced with 'X:Y'
    """
    body = request.body
    if helpers.PY3:
        body = request.body.decode('utf-8')

    payload = json.loads(body)
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

if helpers.PY3:
    my_vcr.register_serializer('json', JSONSerializer)


def fixture_path(filename):
    """Build the full path of a fixture file."""
    return join(dirname(__file__), 'fixtures', filename)


class BaseCase(unittest.TestCase):
    pass
