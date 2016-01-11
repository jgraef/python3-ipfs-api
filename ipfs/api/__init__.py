from .proxy import HttpProxy
from .block import BlockApi
from .dht import DhtApi
from .object import ObjectApi


class IpfsApi:
    def __init__(self, host = "localhost", port = 5001):
        self._proxy = HttpProxy(host, port)
        r = self._proxy.root
        
        self.block = BlockApi(r)
        self.dht = DhtApi(r)
        self.object = ObjectApi(r)
