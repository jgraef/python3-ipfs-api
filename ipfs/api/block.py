"""
This module handles the utilities for the node's blocks.
"""

from .. import codec


class BlockApi:
    """
    Manipulate raw IPFS blocks.
    """

    def __init__(self, root):
        self._rpc = root.block


    def stat(self, key):
        """
        Print information of a raw IPFS block.

        :param key: The base58 multihash of an existing block
        :return:    A dict with:
           ``Key``:  The key of that block
           ``Size``: The size of that block in bytes
        """
        return self._rpc.stat[key].with_outputenc(codec.JSON)()


    def get(self, key):
        """
        Get a raw IPFS block.

        :param key: The base58 multihash of an existing block
        :return:    A byte stream with the raw contents of that block

        Example::

           >>> key = "QmZTR5bcpQD7cFgTorqxZDYaew1Wqgfbd2ud9QqGPAkK2V"
           >>> IpfsApi().block.get(key).read()[27:62].decode()
           'IPFS -- Inter-Planetary File system'

        
        """
        return self._rpc.get[key]()


    def put(self, f):
        """
        Store data as an IPFS block.

        :param f: A byte stream that is used as contents of that block
        :return:  A dict with:
           ``Key``:  The key of the new block
           ``Size``: The size of the new block

        Example::

           >>> from io import BytesIO
           >>> IpfsApi().block.put(BytesIO(b"foobar"))
           {'Key': 'QmbWTwYGcmdyK9CYfNBcfs9nhZs17a6FQ4Y8oea278xx41', 'Size': 6}

        """
        return self._rpc.put.with_outputenc(codec.JSON)(_in = f)


__all__ = ["BlockApi"]
	
