# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""
import uuid

import requests

from . import exceptions

url = "https://ais.swisscom.com/AIS-Server/rs/v1.0/sign"


class AIS():
    def __init__(self, customer, key_static):
        self.customer = customer
        self.key_static = key_static

    def _request_id(self):
        return uuid.uuid4().hex

    def sign(self, filename):
        file_hash = ""

        payload = {
            "SignRequest": {
                "@RequestID": self._request_id(),
                "@Profile": "http://ais.swisscom.ch/1.0",
                "OptionalInputs": {
                    "ClaimedIdentity": {
                        "Name": self.customer,
                    },
                    "SignatureType": "urn:ietf:rfc:3161",
                    "sc.AddRevocationInformation": {"@Type": "BOTH"},
                    "AdditionalProfile":
                    "urn:oasis:names:tc:dss:1.0:profiles:timestamping",
                },
                "InputDocuments": {
                    "DocumentHash": {
                        "dsig.DigestMethod": {
                            "@Algorithm":
                            "http://www.w3.org/2001/04/xmlenc#sha256"
                        },
                        "dsig.DigestValue": file_hash
                    },
                }
            }
        }

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
        }
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()['SignResponse']['Result']

        if 'Error' in result['ResultMajor']:
            raise exceptions.error_for(response)

        return Signature()


class Signature():
    pass
