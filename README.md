# python3-ipfs-api

This is a complete rewrite of python-ipfs-api. It defines a whole new interface
and tries to do more than just wrapping the HTTP API. python3-ipfs-api will
only support Python 3 (hence the name).

Documentation is available here: http://python3-ipfs-api.readthedocs.org/en/latest/

python3-ipfs-api uses requests to issue API calls. Also it has a minimal
implementation of a protobuf reader/writer for using protobuf encoding where
possible. This makes it possible to e.g. put/get objects with binary content
without a problem.

In ipfs.api you'll find the lowlevel API implementation. The high-level API is
still work in progess and only consists of the ifps.merkledag module. An
API for interfacing unixfs in a pythonic way will come soon.

This software is still work in progress. Use the original python-ipfs-api
(https://github.com/ipfs/python-ipfs-api) where possible.

See testing/tests_* on how to use the parts that already work.


## TODO

 * Implemented lowlevel APIs: swarm, bitswap, bootstrap
 * Implement high-level unixfs API
 * Fix ipfs.object.patch
 * Finish ipfs.config
 * Fix ipfs.file.cat. It seems to only work on plain hashes
 
 * Documentation (work in progress)
 * Examples (work in progess)

 * @mec-is: Split the testing/test_ipfsapi.py in different files for each API
 * See todos in line in the files
