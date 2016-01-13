# coding=utf-8

from distutils.core import setup


setup(name = "python3-ipfs-api",
      version = "0.3.11-dev",

      description = "Python API for the IPFS HTTP API",

      author = u"Janosch Gräf",

      author_email = "janosch.graef@gmx.net",

      url = "https://github.com/jgraef/python3-ipfs-api",
      
      packages = ["ipfs", "ipfs.api", "ipfs.proto"],

      license = "MIT",

      platforms = ['Any'],

      keywords = ["ipfs"],

      requires = ["requests (>=2.9.1)", "base58 (>=0.2.2)", "python3-pb2nano"],

      long_description = """
python3-ipfs-api is a complete rewrite of [python-ipfs-api](https://github.com/ipfs/python-ipfs-api).
It defines a whole new interface and tries to do more than just wrapping the
HTTP API. python3-ipfs-api will only support Python 3 (hence the name).

python3-ipfs-api uses [requests](http://python-requests.org) to issue API
calls. Also it has a minimal implementation of a protobuf reader/writer for
using protobuf encoding where possible. This makes it possible to e.g. put/get
objects with binary content without a problem.

In ipfs.api you'll find the lowlevel API implementation. The high-level API is
still work in progess and only consists of the ifps.merkledag module at the moment. An
API for interfacing unixfs in a pythonic way will come soon.
""")
