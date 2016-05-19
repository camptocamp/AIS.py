AIS.py
======

.. image:: https://travis-ci.org/camptocamp/AIS.py.svg?branch=master
    :target: https://travis-ci.org/camptocamp/AIS.py

.. image:: https://readthedocs.org/projects/aispy/badge/?version=latest
    :target: http://aispy.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

AIS.py: a Python interface for the Swisscom All-in Signing Service (aka AIS).

AIS.py works like this:

.. code-block:: python

    >>> from AIS import AIS, PDF
    >>> client = AIS.AIS('alice', 'a_secret', 'a.crt', 'a.key')
    >>> pdf = PDF('source.pdf')
    >>> client.sign_one_pdf(pdf)
    >>> print(pdf.out_filename)
    /tmp/.../T/tmpexkdrlkm.pdf

For more information, check out the `Documentation`_.

.. _Documentation: http://aispy.readthedocs.io

.. include:: AUTHORS.rst

License
-------

Copyright (C) 2016 Camptocamp SA

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
