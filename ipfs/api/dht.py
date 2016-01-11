from . import codec


class DhtApi:
    def __init__(self, root):
        self._rpc = root.dht


    def query(self, key):
        return self._rpc.query[key].with_outputenc(codec.JSONV)()


    def find_providers(self, key):
        return self._rpc.findprovs[key].with_outputenc(codec.JSONV)()


    def find_peers(self, peer_id):
        return self._rpc.findpeers[peer_id].with_outputenc(codec.JSONV)()

    
    def get(self, key):
        return self._rpc.get[key].with_outputenc(codec.JSONV)()


    def put(self, key, value):
        return self._rpc.get[key].with_outputenc(codec.JSONV)(value)


__all__ = ["DhtApi"]
