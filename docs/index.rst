.. AIS.py documentation master file, created by
   sphinx-quickstart on Wed May 18 11:35:35 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

AIS.py
======

AIS.py: a Python interface for the Swisscom All-in Signing Service (aka AIS).

Release v\ |version|.

Introduction
------------

AIS is a webservice for electronic signatures offered by Swisscom. You can
check out the `corporate page`_ and the `reference guide`_ of the
service.

To use the webservice you have to send an appropriate digest of the file. The
service returns a PKCS#7 detached signature that can be send alongside the
original file.

To validate a detached signature, the digest of the original file can be
computed again.

In the case of PDF files, the signature is integrated in the PDF itself and
it needs to be extracted to be verified.

A complication in that case is that during verification you must be able to
compute the same digest that was used to generate the signature with the
original file, but the original file is not available anymore, and the signed
file has clearly a different digest.

Thus, the procedure is the following:

1. The original PDF file is prepared by adding an empty signature block. This
   includes a ``ByteRange`` object.
2. The digest is computed only in the part specified by the ``ByteRange``, so
   it excludes the empty signature.
3. The digest is sent to the AIS webservice.
4. The detached signature is included in the placeholder.

``AIS.py`` takes care of all this, delegating point 1 to `iText`_

.. _corporate page:  https://www.swisscom.ch/en/business/enterprise/offer/security/identity-access-security/signing-service.html
.. _reference guide: http://documents.swisscom.com/product/1000255-Digital_Signing_Service/Documents/Reference_Guide/Reference_Guide-All-in-Signing-Service-en.pdf
.. _iText: itextpdf.com

API Reference
-------------

This section describes classes and exceptions.

.. toctree::
   :maxdepth: 2

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

