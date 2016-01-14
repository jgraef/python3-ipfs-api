"""
Module containing the PinApi
"""

from .. import codec


class PinApi:
    """ Pin and unpin objects to local storage. """
    
    def __init__(self, root):
        self._rpc = root.pin


    def add(self, path):
        """
        Pin object to local storage.

        :param path: Path of object to pin
        :return:     A dict with:
           ``Pinned``: List of hashes that have been pinned.
        """
        return self._rpc.add.with_outputenc(codec.JSON)(path)


    def rm(self, path):
        """
        Unpin object from local storage.

        :param path: Path of object to unpin
        :return:     A dict with:
           ``Pinned``: List of hashes that have been unpinned.
        """
        return self._rpc.rm.with_outputenc(codec.JSON)(path)


    def ls(self):
        """
        List all pinned objects.

        :return: See example

        TODO: Example
        """
        return self._rpc.ls.with_outputenc(codec.JSON)()


__all__ = ["PinApi"]
