.. python3-ipfs-api documentation master file, created by
   sphinx-quickstart on Tue Jan 12 12:34:13 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to python3-ipfs-api's documentation!
============================================

python3-ipfs-api is a complete rewrite of `python-ipfs-api
<https://github.com/ipfs/python-ipfs-api>`_. It defines a whole new interface
and tries to do more than just wrapping the HTTP API. python3-ipfs-api will
only support Python 3 (hence the name).

python3-ipfs-api uses `requests <http://python-requests.org>`_ to issue API calls. Also it uses a minimal implementation
of a protobuf2 reader/writer (called `pb2nano <https://github.com/jgraef/python3-pb2nano>`_) for using protobuf encoding
where possible. This makes it possible to e.g. put/get objects with binary content without a problem.

In :py:mod:`ipfs.api` you'll find the lowlevel API implementation. The high-level API is
still work in progess and only consists of the :py:mod:`ipfs.merkledag` module at the moment. An
API for interfacing unixfs in a pythonic way will come soon.

If you want to get started take a look at our ``examples/`` or read the documentation.


.. Contents:  .. toctree::  :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

