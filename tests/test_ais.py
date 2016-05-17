# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""
from os import environ

from common import my_vcr, fixture_path, BaseCase

from AIS import AIS, Signature, AuthenticationFailed, PDF


class TestAIS(BaseCase):

    def test_constructor_builds_instance(self):
        alice_instance = AIS(customer='alice', key_static='alice_secret',
                             cert_file='alice.crt', cert_key='alice.key')
        self.assertEqual('alice', alice_instance.customer)
        self.assertEqual('alice_secret', alice_instance.key_static)

    def test_sign_filename_returns_signature(self):
        with my_vcr.use_cassette('sign_one') as cassette:
            result = self.instance.sign(filename=fixture_path('one.pdf'))

        self.assertEqual(1, len(cassette))
        self.assertIsInstance(result, Signature)
        self.assertIsInstance(result.contents, bytes)

    def test_sign_single_prepared_pdf(self):
        with my_vcr.use_cassette('sign_prepared_pdf'):
            self.instance.sign_one_pdf(PDF(fixture_path('prepared.pdf')))

    # def test_sign_prepared_batch(self):
    #     """Test signature of a single unprepared pdf."""
    #     filenames = ["prep1.pdf", "prep2.pdf", "prep3.pdf"]
    #     with my_vcr.use_cassette('sign_prepared_batch'):
    #         self.instance.sign_batch([
    #             PDF(fixture_path(f)) for f in filenames
    #         ])

    def test_wrong_customer_authentication_failed(self):
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
