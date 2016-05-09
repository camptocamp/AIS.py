# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""
import unittest
from AIS import AIS, Signature


class TestAIS(unittest.TestCase):

    def test_constructor(self):
        ais = AIS(customer='mike', key_static='the_secret')

        self.assertTrue(ais)
        self.assertEqual('mike', ais.customer)
        self.assertEqual('the_secret', ais.key_static)

    def test_sign_filename_returns_signature(self):
        ais = AIS(customer='mike', key_static='the_secret')

        result = ais.sign(filename='one.txt')

        self.assertIsInstance(result, Signature)
