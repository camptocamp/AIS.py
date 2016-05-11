# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""

import base64
import hashlib
import sys
import uuid

import requests

from . import exceptions

url = "https://ais.swisscom.com/AIS-Server/rs/v1.0/sign"

PY3 = sys.version_info[0] == 3


class AIS():
    """Client object holding connection information to the AIS service."""

    def __init__(self, customer, key_static, cert_file, cert_key):
        """Initialize an AIS client with authentication information."""
        self.customer = customer
        self.key_static = key_static
        self.cert_file = cert_file
        self.cert_key = cert_key

    def _request_id(self):
        return uuid.uuid4().hex

    def _hash(self, filename):
        """Return the hash of a file as a str."""
        with open(filename, 'rb') as fp:
            contents = fp.read()
        h = hashlib.new('sha256', contents)
        result = base64.b64encode(h.digest())
        if PY3:
            result = result.decode('ascii')
        return result

    def sign(self, filename):
        """Sign the given file, return a Signature instance."""
        file_hash = self._hash(filename)

        payload = {
            "SignRequest": {
                "@RequestID": self._request_id(),
                "@Profile": "http://ais.swisscom.ch/1.0",
                "OptionalInputs": {
                    "ClaimedIdentity": {
                        "Name": ':'.join((self.customer, self.key_static)),
                    },
                    "SignatureType": "urn:ietf:rfc:3369",
                    "AddTimestamp": {"@Type": "urn:ietf:rfc:3161"},
                    "sc.AddRevocationInformation": {"@Type": "BOTH"},
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
        cert = (self.cert_file, self.cert_key)
        response = requests.post(url, json=payload, headers=headers, cert=cert)
        sign_response = response.json()['SignResponse']
        result = sign_response['Result']

        if 'Error' in result['ResultMajor']:
            raise exceptions.error_for(response)

        signature = Signature(base64.b64decode(
            sign_response['SignatureObject']['Base64Signature']['$']
        ))
        return signature


class Signature():
    """A cryptographic signature returned from the AIS webservice."""

    def __init__(self, contents):
        """Build a Signature."""
        self.contents = contents
