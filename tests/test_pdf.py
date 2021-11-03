# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""
from common import fixture_path, BaseCase

from AIS import PDF


class TestPDF(BaseCase):

    def test_prepare_then_get_digest(self):
        pdf = PDF(fixture_path('one.pdf'))

        pdf.prepare()
        self.assertEqual(44, len(pdf.digest()))   # digest changes every time
