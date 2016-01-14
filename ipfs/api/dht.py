"""
This module handles the Distributed Hash Table
"""

from .. import codec


class DhtApi:
    """
    Issue commands directly through the DHT.
    """
    
    def __init__(self, root):
        self._rpc = root.dht


    def query(self, peer_id):
        """
        Run a 'FindClosestPeers' query through the DHT.

        :param peer_id: The peer ID to run the query against
        :return: TODO
        """
        return self._rpc.query[peer_id].with_outputenc(codec.JSONV)()


    def find_providers(self, key):
        """
        Run a 'FindProviders' query through the DHT.

        :param key: The key to find providers for
        :return: TODO
        """
        return self._rpc.findprovs[key].with_outputenc(codec.JSONV)()


    def find_peer(self, peer_id):
        """
        Run a 'FindPeer' query through the DHT.

        :param peer_id: The peer to search for
        :return: TODO
        """
        return self._rpc.findpeers[peer_id].with_outputenc(codec.JSONV)()

    
    def get(self, key):
        """
        Run a 'GetValue' query through the DHT.

        :param key: The key to find a value for
        :return: TODO
        """
        return self._rpc.get[key].with_outputenc(codec.JSONV)()


    def put(self, key, value):
        """
        Run a 'PutValue' query through the DHT.
        
        :param key:   The key to store the value at
        :param value: The value to store
        :return: TODO
        """
        return self._rpc.get[key].with_outputenc(codec.JSONV)(value)


__all__ = ["DhtApi"]
