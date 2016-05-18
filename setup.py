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
    name="AIS.py",
    version=version,
    description=("Python interface for the Swisscom All-in Signing Service"),
    long_description=readme + '\n\n' + history,
    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    author="Camptocamp SA",
    author_email="info@camptocamp.com",
    url="https://pypi.python.org/pypi/AIS.py",
    packages=['AIS'],
    install_requires=["requests >= 2.0",
                      "PyPDF2"],
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved',
        'License :: OSI Approved :: '
        'GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
