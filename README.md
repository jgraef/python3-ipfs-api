# python3-ipfs-api

python3-ipfs-api is a complete rewrite of [python-ipfs-api](https://github.com/ipfs/python-ipfs-api).
It defines a whole new interface and tries to do more than just wrapping the
HTTP API. python3-ipfs-api will only support Python 3 (hence the name).

python3-ipfs-api uses [requests](http://python-requests.org) to issue API
calls. Also it uses a minimal implementation of a protobuf2 reader/writer (called
[pb2nano](https://github.com/jgraef/python3-pb2nano)) for using protobuf encoding where possible. This makes it
possible to e.g. put/get objects with binary content without a problem.

In ipfs.api you'll find the lowlevel API implementation. The high-level API is still work in progess and only consists
of the `merkledag` and `unixfs` modules at the moment.

If you want to get started take a look at our `examples/` or read the
[documentation](http://python3-ipfs-api.readthedocs.org/en/latest/).


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
