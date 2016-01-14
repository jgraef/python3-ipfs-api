"""
This module exposes the IPFS file API.
"""

from .. import codec


class FileApi:
    """
    Interact with IPFS objects that represent Unix files.
    """
    
    def __init__(self, root):
        self._rpc = root


    def ls(self, path):
        """
        List directory contents for unixfs objects.

        :param path: The path to the IPFS object to list links from
        :return:     Retrieves the object named by the path and lists its
                     contents.
        """
        return self._rpc.file.ls[path].with_outputenc(codec.JSON)()


    def add(self, f):
        """
        Add a file to IPFS.

        :param f: A file-like object that will be added to IPFS
        :return:  A dict containing the ``Hash`` of the file.
        """
        return self._rpc.add.with_outputenc(codec.JSON)(_in = f)


    def cat(self, path):
        """
        Read a file from IPFS.

        :param path: The path to the IPFS object to read
        :return:     A file-like object with the contents of the file.
        """
        return self._rpc.cat[path]()


__all__ = ["FileApi"]
