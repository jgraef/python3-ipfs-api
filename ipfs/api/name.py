"""
This modules handles name publishing and resolution
"""

from .. import codec


class NameApi:
    """
    Publish an resolve IPNS names.
    """

    def __init__(self, root):
        self._rpc = root.name


    def publish(self, path, resolve = True, lifetime = None, ttl = None):
        """
        Publish an object to IPNS.

        :param path:     IPFS path of the object to be published
        :param resolve:  resolve given path before publishing (default=True)
        :param lifetime: time duration that the record will be valid for
                         (default: 24 hours)
        :param ttl:      time duration this record should be cached for
                         (caution: experimental)
        :return: A dict with:
           ``Name``:  The IPNS name of the published object
           ``Value``: The IPFS path of the published object
        """
        return self._rpc.publish.with_outputenc(codec.JSON)(path, resolve = True, lifetime = lifetime, ttl = ttl)


    def resolve(self, name = None, recursive = None, nocache = None):
        """
        Gets the value currently published at an IPNS name

        :param name:      The IPNS name to resolve. Defaults to your node's
                          peer ID.
        :param recursive: Resolve until the result is not an IPNS name (default:
                          True)
        :param nocache:   Do not used cached entries (default: TODO)
        :return: A dict with:
           ``Path``: The path pubilshed under that name
        :raise: ProxyError if the name can't be resolved
        """
        return self._rpc.resolve.with_outputenc(codec.JSON)(name, recursive = recursive, nocache = nocache)


__all__ = ["NameApi"]
