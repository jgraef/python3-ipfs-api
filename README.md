## python3-ipfs-api

This is a complete rewrite of python-ipfs-api. It defines a whole new interface and tries to do more than just wrapping
the HTTP API. python3-ipfs-api will only support Python 3 (hence the name).

python3-ipfs-api uses requests to issue API calls. Also it has a minimal implementation of a protobuf reader/writer
for using protobuf encoding where possible. This makes it possible to e.g. put/get objects with binary content without
a problem.

In ipfs.api you'll find the lowlevel API implementation. Block, DHT and parts of Object commands already work.

Soon I'll also include my abstraction of the merkledag and an abstraction layer for unixfs is also planned.

This software is still work in progress. Use the original python-ipfs-api (https://github.com/ipfs/python-ipfs-api)
where possible.

See test.py on how to use the parts that already work.

