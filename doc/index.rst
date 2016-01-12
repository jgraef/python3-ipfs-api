.. python3-ipfs-api documentation master file, created by
   sphinx-quickstart on Tue Jan 12 12:34:13 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to python3-ipfs-api's documentation!
============================================

python3-ipfs-api is a complete rewrite of python-ipfs-api. It defines a whole new interface
and tries to do more than just wrapping the HTTP API. python3-ipfs-api will
only support Python 3 (hence the name).

python3-ipfs-api uses requests to issue API calls. Also it has a minimal
implementation of a protobuf reader/writer for using protobuf encoding where
possible. This makes it possible to e.g. put/get objects with binary content
without a problem.

In :py:mod:`ipfs.api` you'll find the lowlevel API implementation. The high-level API is
still work in progess and only consists of the :py:mod:`ifps.merkledag` module. An
API for interfacing unixfs in a pythonic way will come soon.

This software is still work in progress. Use the original python-ipfs-api
(https://github.com/ipfs/python-ipfs-api) where possible.

See testing/tests_* on how to use the parts that already work.


.. Contents:  .. toctree::  :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

