# -*- coding: utf-8 -*-
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""

import base64
from datetime import datetime
import io

from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import fields
from pyhanko.sign import signers
from pyhanko.sign.signers import cms_embedder


class PDF(object):
    """A container for a PDF file to be signed and the signed version."""

    def __init__(self, input_file):
        """Accepts either a filename or file-like object"""

        if isinstance(input_file, str):
            with open(input_file, 'rb') as fp:
                self.in_stream = io.BytesIO(fp.read())
        else:
            self.in_stream = input_file

        writer = IncrementalPdfFileWriter(self.in_stream)
        self.cms_writer = cms_embedder.PdfCMSEmbedder().write_cms(
            field_name='Signature',
            writer=writer
        )
        """CMS Writer used for embedding the signature"""
        next(self.cms_writer)

        self.out_stream = None
        """Output stream for the signed PDF, is only valid after digest"""

        self.sig_obj = None
        """Signature object used by pyHanko"""

    def prepare(self):
        """Add an empty signature to self.out_filename."""
        self.sig_obj = signers.SignatureObject(
            timestamp=datetime.now(),
            bytes_reserved=64*1024,  # 64KiB
        )

    def digest(self):
        self.cms_writer.send(
            cms_embedder.SigObjSetup(
                sig_placeholder=self.sig_obj,
                mdp_setup=cms_embedder.SigMDPSetup(
                    md_algorithm='sha256',
                    certify=True,
                    docmdp_perms=fields.MDPPerm.NO_CHANGES,
                )
            )
        )
        digest, self.out_stream = self.cms_writer.send(
            cms_embedder.SigIOSetup(md_algorithm='sha256', in_place=True)
        )

        result = base64.b64encode(digest.document_digest)

        return result.decode('ascii')

    def write_signature(self, signature):
        """ Write the signature in the pdf file

        :type signature: Signature
        """
        self.cms_writer.send(signature.contents)
