# coding=utf-8

from distutils.core import setup


setup(name = "python3-ipfs-api",
      version = "0.3.11-dev",

      description = "Python API for the IPFS HTTP API",

      author = u"Janosch Gräf",

      author_email = "janosch.graef@gmx.net",

      url = "https://github.com/jgraef/python3-ipfs-api",
      
      packages = ["ipfs", "ipfs.api", "ipfs.pb2hack", "ipfs.proto"],

      license = "MIT",

      long_description = """
This is a complete rewrite of python-ipfs-api. It defines a whole new interface
and tries to do more than just wrapping the HTTP API. python3-ipfs-api will
only support Python 3 (hence the name).

python3-ipfs-api uses requests to issue API calls. Also it has a minimal
implementation of a protobuf reader/writer for using protobuf encoding where
possible. This makes it possible to e.g. put/get objects with binary content
without a problem.

In ipfs.api you'll find the lowlevel API implementation. Block, DHT and parts
of Object commands already work.

There will be high-level APIs. Currently only ipfs.merkledag is available. An
API for interfacing unixfs in a pythonic way will come soon.

This software is still work in progress. Use the original python-ipfs-api
(https://github.com/ipfs/python-ipfs-api) where possible.
""")
