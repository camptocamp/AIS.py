# -*- coding: utf-8 -*-

from codecs import open
import re
from setuptools import setup

with open('AIS/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name="AIS2.py",
    version=version,
    description=("Python interface for the Swisscom All-in Signing Service"),
    long_description=readme + '\n\n' + history,
    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    author="Camptocamp",
    author_email="info@camptocamp.com",
    maintainer="Seantis GmbH",
    maintainer_email="info@seantis.ch",
    url="https://pypi.python.org/pypi/AIS2.py",
    packages=['AIS'],
    install_requires=["requests >= 2.0",
                      "pyHanko >= 0.9.0"],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved',
        'License :: OSI Approved :: '
        'GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
