from . import codec
from .proxy import HttpProxy
from .block import BlockApi
from .dht import DhtApi
from .object import ObjectApi
from .config import ConfigApi



class IpfsApi:
    def __init__(self, host = "localhost", port = 5001):
        self._proxy = HttpProxy(host, port)
        self._rpc = r = self._proxy.root
        
        self.block = BlockApi(r)
        self.dht = DhtApi(r)
        self.object = ObjectApi(r)
        self.config = ConfigApi(r)


    def id(self):
        return self._rpc.id.with_outputenc(codec.JSON)()


    def version(self):
        return self._rpc.version.with_outputenc(codec.JSON)()