# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""
from os import environ
from os.path import dirname, join
import unittest

from AIS import AIS, Signature, AuthenticationFailed


def fixture_path(filename):
    return join(dirname(__file__), 'fixtures', filename)


class TestAIS(unittest.TestCase):

    def test_constructor(self):
        alice_instance = AIS(customer='alice', key_static='alice_secret',
                             cert_file='alice.crt', cert_key='alice.key')
        self.assertEqual('alice', alice_instance.customer)
        self.assertEqual('alice_secret', alice_instance.key_static)

    def test_sign_filename_returns_signature(self):
        result = self.instance.sign(filename=fixture_path('one.pdf'))

        self.assertIsInstance(result, Signature)
        self.assertIsInstance(result.contents, bytes)

    def test_wrong_customer_auth_error(self):
        bad_instance = AIS(customer="wrong_name", key_static="wrong_key",
                           cert_file=self.cert_file,
                           cert_key=self.cert_key)

        with self.assertRaises(AuthenticationFailed):
            bad_instance.sign(filename=fixture_path('one.pdf'))

    def setUp(self):
        self.customer = environ.get('AIS_CUSTOMER', 'bonnie')
        self.key_static = environ.get('AIS_KEY_STATIC', 'the_secret')
        self.cert_file = environ.get('AIS_CERT_FILE', fixture_path('test.crt'))
        self.cert_key = environ.get('AIS_CERT_KEY', fixture_path('test.key'))

        self.instance = AIS(self.customer, self.key_static,
                            self.cert_file, self.cert_key)
