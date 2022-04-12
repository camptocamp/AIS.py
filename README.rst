AIS2.py
======

.. image:: https://img.shields.io/pypi/v/AIS2.py.svg
    :target: https://pypi.org/project/AIS2.py
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/AIS2.py.svg
    :target: https://pypi.org/project/AIS2.py
    :alt: Python versions

.. image:: https://github.com/seantis/AIS2.py/actions/workflows/python-tox.yaml/badge.svg
    :target: https://github.com/seantis/AIS2.py/actions
    :alt: Tests

.. image:: https://codecov.io/gh/seantis/AIS2.py/branch/master/graph/badge.svg?token=NRPFO5L0PG
    :target: https://codecov.io/gh/seantis/AIS2.py
    :alt: Codecov.io

AIS.py: a Python interface for the Swisscom All-in Signing Service (aka AIS).

AIS2.py is a fork created to get rid of the licensing woes affected itext dependency and replace it with pyHanko. Furthermore the API was slightly adjusted to be more flexible, so buffers can be passed around rather than files that need to exist on the filesystem.

AIS2.py works like this:

.. code-block:: python

    >>> from AIS import AIS, PDF
    >>> client = AIS('alice', 'a_secret', 'a.crt', 'a.key')
    >>> with open('source.pdf', 'rb') as fp:
    ...     pdf = PDF(fp)
    ...     with open('target.pdf', 'wb') as fp:
    ...         fp.write(pdf.out_stream.getbuffer())
    ... 

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
