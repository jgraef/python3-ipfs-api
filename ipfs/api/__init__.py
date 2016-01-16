"""
This modules exposes the IPFS HTTP API to Python.

To get started create an instance of :py:class:`IpfsApi`::

   >>> from ipfs.api import IpfsApi
   >>> ipfs = IpfsApi()

"""


from .. import codec
from .proxy import HttpProxy
from .block import BlockApi
from .dht import DhtApi
from .object import ObjectApi
from .config import ConfigApi
from .name import NameApi
from .pin import PinApi
from .file import FileApi



class IpfsApi:
    """
    An wrapper for the IPFS HTTP API. It exposes sub-commands and top-level
    commands and wraps them with the appropiate encodings.

    Example::

       >>> key = "QmPZ9gcCEpqKTo6aq61g2nXGUhM4iCL3ewB6LDXZCtioEB"
       >>> print(IpfsApi().file.cat(key).read().decode())

    IpfsApi exposes top-level command as its methods (e.g. :py:meth:`id`) and
    sub-commands can be accessed via the name of the plumbing command (e.g.
    :py:attr:`file`).

    The following plumbing commands are available at the moment:

       - :py:attr:`block`: Operations on raw blocks.

       - :py:attr:`dht`: Operations on the DHT

       - :py:attr:`object`: Operations on objects a.k.a merkledag nodes

       - :py:attr:`config`: Operations on the configuration

       - :py:attr:`name`: Name resolution and publishing

       - :py:attr:`pin`: Pinning of blocks

       - :py:attr:`file`: File operations

    """

    def __init__(self, host = "localhost", port = 5001):
        """
        Create an instance of an IPFS API.

        :param host: The hostname where the API is running.
        :param port: The port which the API is listening to.
        """

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

        :param peer_id: Peer ID of node to look up (optional)
        :return:        A dict with:
           ``ID``:              The peer's ID
           ``PublicKey``:       The peer's public key encoded as base64
           ``Addresses``:       A list of the peer's addresses
           ``AgentVersion``:    The peer's agent version
           ``ProtocolVersion``: The peer's protocol version
        """
        return self._rpc.id.with_outputenc(codec.JSON)(peer_id)


    def version(self):
        """
        Return IPFS version information.

        :return: A dict with:
           ``Version``: Version number
           ``Commit``:  Commit hash
           ``Repo``:    Repo version

        Example::

           >>> ipfs.version()
           {'Commit': '', 'Repo': '2', 'Version': '0.3.11-dev'}

        """

        return self._rpc.version.with_outputenc(codec.JSON)()


    def resolve(self, name, recursive = None):
        """
        Resolve a name.

        :param name:      The name to resolve
        :param recursive: Resolve until the name is an IPFS name (default: true)
        :return:          The resolved IPFS name

        Example::

           >>> name = "QmXarR6rgkQ2fDSHjSY5nM2kuCXKYGViky5nohtwgF65Ec/readme"
           >>> IpfsApi().resolve(name)
           {'Path': '/ipfs/QmPZ9gcCEpqKTo6aq61g2nXGUhM4iCL3ewB6LDXZCtioEB'}
        
        """
        
        return self._rpc.resolve.with_outputenc(codec.JSON)(name, recursive = recursive)


    def repo_gc(self):
        """ Perform a garbage collection sweep on the repo. """
        return self._rpc.repo.gc.with_outputenc(codec.JSONV)()



__all__ = [
    "block",
    "config",
    "dht",
    "file",
    "name",
    "object",
    "pin",
    "proxy",
    "IpfsApi"
]
