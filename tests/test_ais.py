# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""
from os import environ
import unittest

from AIS import AIS, AuthenticationFailed


class TestAIS(unittest.TestCase):

    def test_constructor(self):
        alice_instance = AIS(customer='alice', key_static='alice_secret')
        self.assertEqual('alice', alice_instance.customer)
        self.assertEqual('alice_secret', alice_instance.key_static)

    def test_wrong_customer_auth_error(self):
        bad_instance = AIS(customer="wrong_name", key_static="wrong_key")

        with self.assertRaises(AuthenticationFailed):
            bad_instance.sign(filename='one.txt')

    def setUp(self):
        self.customer = environ.get('AIS_CUSTOMER', 'mike')
        self.key_static = environ.get('AIS_KEY_STATIC', 'the_secret')

        self.instance = AIS(customer=self.customer, key_static=self.key_static)
