# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""

import base64
import hashlib
import shutil
import subprocess
import tempfile

import PyPDF2
from pkg_resources import resource_filename

from . import exceptions
from . import helpers


class PDF():
    def __init__(self, in_filename):
        self.in_filename = in_filename
        self.out_fp, self.out_filename = tempfile.mkstemp()
        shutil.copy(self.in_filename, self.out_filename)

    def prepare(self):
        """Add an empty signature to self.out_filename."""
        java_dir = resource_filename(__name__, 'empty_signer')

        subprocess.check_call([
            'java',
            '-cp', '.:vendor/itextpdf-5.5.9.jar',
            '-Duser.dir={}'.format(java_dir),
            'EmptySigner',
            self.out_filename,
        ])

    def digest(self):
        reader = PyPDF2.PdfFileReader(self.out_filename)
        sig_obj = None

        for generation, idnums in reader.xref.items():
            for idnum in idnums:
                if idnum == 0:
                    break
                pdf_obj = PyPDF2.generic.IndirectObject(idnum, generation,
                                                        reader).getObject()
                if (
                    isinstance(pdf_obj, PyPDF2.generic.DictionaryObject) and
                    pdf_obj.get('/Type') == '/Sig'
                ):
                    sig_obj = pdf_obj
                    break

        if sig_obj is None:
            raise exceptions.MissingPreparedSignature

        self.byte_range = sig_obj['/ByteRange']

        h = hashlib.sha256()
        with open(self.out_filename, 'rb') as fp:
            for start, length in (self.byte_range[:2], self.byte_range[2:]):
                fp.seek(start)
                h.update(fp.read(length))

        result = base64.b64encode(h.digest())

        if helpers.PY3:
            result = result.decode('ascii')

        return result