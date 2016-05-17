# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""
from common import fixture_path, BaseCase

from AIS import PDF


class TestPDF(BaseCase):

    def test_get_digest_of_prepared_file(self):
        pdf = PDF(fixture_path('prepared.pdf'))

        with open(fixture_path('expected_digest')) as fp:
            self.assertEqual(fp.read(), pdf.digest())
