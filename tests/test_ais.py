# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""
import json
from os import environ
from os.path import dirname, join
import unittest

from vcr import VCR

from AIS import AIS, Signature, AuthenticationFailed


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


class TestAIS(unittest.TestCase):
    """Generic tests of the AIS client."""

    def test_constructor(self):
        """The constructor builds a client instance."""
        alice_instance = AIS(customer='alice', key_static='alice_secret',
                             cert_file='alice.crt', cert_key='alice.key')
        self.assertEqual('alice', alice_instance.customer)
        self.assertEqual('alice_secret', alice_instance.key_static)

    def test_sign_filename_returns_signature(self):
        """Test signature of a single file.

        Given I am authenticated
        When a sign an existing file
        Then I receive a signature
        """
        with my_vcr.use_cassette('sign_one') as cassette:
            result = self.instance.sign(filename=fixture_path('one.pdf'))

        self.assertEqual(1, len(cassette))
        self.assertIsInstance(result, Signature)
        self.assertIsInstance(result.contents, bytes)

    def test_wrong_customer_auth_error(self):
        """Test an AuthenticationFailed."""
        bad_instance = AIS(customer="wrong_name", key_static="wrong_key",
                           cert_file=self.cert_file,
                           cert_key=self.cert_key)

        with self.assertRaises(AuthenticationFailed):
            with my_vcr.use_cassette('wrong_customer'):
                bad_instance.sign(filename=fixture_path('one.pdf'))

    def setUp(self):
        """Setup an AIS instance to be used in the tests.

        If you have real credentials to AIS and wish to use them to run tests,
        you can set the AIS_CUSTOMER, AIS_KEY_STATIC, AIS_CERT_FILE and
        AIS_CERT_KEY environment variables.

        Tests should still pass without them, including on CI and offline,
        because the interaction to the webservice are mocked and stored as
        cassettes. Delete the cassettes and set those variables to test with
        real interactions.

        """
        self.customer = environ.get('AIS_CUSTOMER', 'bonnie')
        self.key_static = environ.get('AIS_KEY_STATIC', 'the_secret')
        self.cert_file = environ.get('AIS_CERT_FILE', fixture_path('test.crt'))
        self.cert_key = environ.get('AIS_CERT_KEY', fixture_path('test.key'))

        self.instance = AIS(self.customer, self.key_static,
                            self.cert_file, self.cert_key)
