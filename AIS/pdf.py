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


class PDF(object):
    """A container for a PDF file to be signed and the signed version."""

    def __init__(self, in_filename, prepared=False):
        self.in_filename = in_filename
        """Filename of the PDF to be treated."""

        _out_fp, _out_filename = tempfile.mkstemp(suffix=".pdf")
        self.out_filename = _out_filename
        """Filename of the output, signed PDF."""

        shutil.copy(self.in_filename, self.out_filename)

        self.prepared = prepared
        """Is the PDF prepared with an empty signature?"""

    @staticmethod
    def _java_command():
        java_dir = resource_filename(__name__, 'empty_signer')
        return [
            'java',
            '-cp', '.:vendor/itextpdf-5.5.9.jar',
            '-Duser.dir={}'.format(java_dir),
            'EmptySigner',
        ]

    @classmethod
    def prepare_batch(cls, pdfs):
        """Add an empty signature to each of pdfs with only one java call."""
        pdfs_to_prepare = filter(lambda p: not p.prepared, pdfs)
        subprocess.check_call(
            cls._java_command() +
            [pdf.out_filename for pdf in pdfs_to_prepare]
        )
        for pdf in pdfs_to_prepare:
            pdf.prepared = True

    def prepare(self):
        """Add an empty signature to self.out_filename."""
        if not self.prepared:
            subprocess.check_call(
                self._java_command() + [self.out_filename],
            )
            self.prepared = True

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
