# EmptySigner

EmptySigner is a small wrapper to the iText java library. It is meant to be
used internally by `AIS.py`, not directly.

EmptySigner received a list of pdf filenames as command line arguments and
edits all of them in-place to add an empty signature (i.e. filled with zeros).

This invalid signature is regognized as invalid by Acrobat Reader, which is
normal.

Being a thin wrapper, there is a simple `Makefile` to compile a `class` file.
Run `make` to update it.
