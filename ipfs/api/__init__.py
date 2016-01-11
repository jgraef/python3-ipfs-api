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


    def id(self, peer_id = None):
        """
        Return information about the specified IPFS peer. If no peer is
        specified, own peer information will be returned.

        ``peer_id``: Peer ID of node to look up (optional)

        returns: A dict with:
                   ``ID``:              The peer's ID
                   ``PublicKey``:       The peer's public key encoded as base64
                   ``Addresses``:       A list of the peer's addresses,
                   ``AgentVersion``:    The peer's agent version
                   ``ProtocolVersion``: The peer's protocol version
                   
        """

        args = (peer_id,) if peer_id else ()
        return self._rpc.id.with_outputenc(codec.JSON)(*args)


    def version(self):
        """
        Return IPFS version information.

        returns: A dict with:
                   ``Version``: Version number,
                   ``Commit``:  Commit hash,
                   ``Repo``:    Repo version
        """

        return self._rpc.version.with_outputenc(codec.JSON)()


    def resolve(self, ref, recursive = True):
        """
        Resolve a name.

        ``name``:      The name to resolve
        ``recursive``: Resolve until the name is an IPFS name

        returns: The resolved IPFS name
        """
        
        return self._rpc.resolve.with_outputenc(codec.JSON)(ref, recursive = recursive)


    def repo_gc(self):
        """ Perform a garbage collection sweep on the repo. """
        return self._rpc.repo.gc.with_outputenc(codec.JSONV)()



__all__ = [
    "block",
    "codec",
    "config",
    "dht",
    "file",
    "name",
    "object",
    "pin",
    "proxy",
    "swarm",
    "IpfsApi"
]
