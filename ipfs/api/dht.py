"""
This module handles the Distributed Hash Table
"""

from . import codec


class DhtApi:
    def __init__(self, root):
        self._rpc = root.dht


    def query(self, key):
        """

        :param key:
        :return:
        """
        return self._rpc.query[key].with_outputenc(codec.JSONV)()


    def find_providers(self, key):
        """

        :param key:
        :return:
        """
        return self._rpc.findprovs[key].with_outputenc(codec.JSONV)()


    def find_peers(self, peer_id):
        """

        :param peer_id:
        :return:
        """
        return self._rpc.findpeers[peer_id].with_outputenc(codec.JSONV)()

    
    def get(self, key):
        """

        :param key:
        :return:
        """
        return self._rpc.get[key].with_outputenc(codec.JSONV)()


    def put(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        return self._rpc.get[key].with_outputenc(codec.JSONV)(value)


__all__ = ["DhtApi"]
