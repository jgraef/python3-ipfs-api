from . import codec
from .proxy import HttpProxy
from .block import BlockApi
from .dht import DhtApi
from .object import ObjectApi
from .config import ConfigApi
from .name import NameApi
from .pin import PinApi
from .file import FileApi



class IpfsApi:
    def __init__(self, host = "localhost", port = 5001):
        self._proxy = HttpProxy(host, port)
        self._rpc = r = self._proxy.root
        
        self.block = BlockApi(r)
        self.dht = DhtApi(r)
        self.object = ObjectApi(r)
        self.config = ConfigApi(r)
        self.name = NameApi(r)
        self.pin = PinApi(r)
        self.file = FileApi(r)


    def id(self):
        return self._rpc.id.with_outputenc(codec.JSON)()


    def version(self):
        return self._rpc.version.with_outputenc(codec.JSON)()


    def resolve(self, ref, recursive = True):
        return self._rpc.resolve.with_outputenc(codec.JSON)(ref, recursive = recursive)


    def repo_gc(self):
        return self._rpc.repo.gc.with_outputenc(codec.JSONV)()


