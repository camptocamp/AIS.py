.. :changelog:

Release History
---------------

0.3.0-beta (2021-11-04)
++++++++++++++++++

- Remove Python 2.7, 3.4, 3.5, 3.6 support
- Replace PyPDF2 and itext with pyHanko
- Remove support for signing prepared PDFs

0.2.2 (2018-10-22)
++++++++++++++++++

- Store the last created request_id on the AIS instance
- Use a proper test matrix on Travis to test various Python releases
- Add Python 3.6 to test matrix

0.2.1 (2016-06-16)
++++++++++++++++++

- Return in batch mode timestamp and revocation information with the signature.
- Fix python3 bugs.
- Refactoring.

0.2.0 (2016-05-19)
++++++++++++++++++

**Documentation**

- Added sections for introduction, installation, testing, project status, API
  reference.

0.1 (2016-05-17)
++++++++++++++++

Initial release. It is possible to start with a batch of pdf files that do not
yet have a prepared signature, and sign them.
