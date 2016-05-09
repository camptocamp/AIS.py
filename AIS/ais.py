# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""


class AIS():
    def __init__(self, customer, key_static):
        self.customer = customer
        self.key_static = key_static

    def sign(self, filename):
        return Signature()


class Signature():
    pass
