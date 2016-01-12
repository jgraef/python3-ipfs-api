"""
This module handles the utilities for the mode's blocks
"""
from . import codec


class BlockApi:
    def __init__(self, root):
        self._rpc = root.block


    def stat(self, key):
        """

        :param key:
        :return:
        """
        return self._rpc.stat[key].with_outputenc(codec.JSON)()


    def get(self, key):
        """

        :param key:
        :return:
        """
        return self._rpc.get[key]()


    def put(self, f):
        """

        :param f:
        :return:
        """
        return self._rpc.put.with_outputenc(codec.JSON)(_in = f)
