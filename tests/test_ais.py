# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""
import unittest
from AIS import AIS


class TestAIS(unittest.TestCase):

    def test_constructor(self):
        ais = AIS()
        self.assertTrue(ais)
