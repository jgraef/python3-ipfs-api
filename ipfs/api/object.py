from .. import codec
from ..proto.merkledag import PBMerkleDag


PBNode = codec.PB2(PBMerkleDag, "PBNode")


class ObjectPatchApi:
    """
    Patch an object.
    """
    
    def __init__(self, rpc, key):
        self.key = key
        self._rpc = rpc.patch[key]


    def add_link(self, name, hash):
        """
        Add a link to the object.

        :param name: Link name
        :param hash: Hash of object to be linked
        :return:     The new object
        """
        return self._rpc.with_outputenc(codec.JSON)("add-link", name, hash)


    def rm_link(self, name):
        """
        Remove a link from the object.

        :param name: Link name
        :return:     The new object
        """
        return self._rpc.with_outputenc(codec.JSON)("rm-link", name)


    def set_data(self, f):
        """
        Set data for the object. NOT IMPLEMENTED YET!

        :param f:    File-like object which is used as data for the object
        :return:     The new object
        """
        raise NotImplementedError()


    def append_data(self, f):
        """
        Set data for the object. NOT IMPLEMENTED YET!

        :param f:    File-like object which is appended to the data of the
                     object
        :return:     The new object
        """
        raise NotImplementedError()



class ObjectApi:
    """
    Interact with IPFS objects.

    For a more high-level API for interacting with IPFS objects, see
    :py:mod:`ipfs.merkledag`

    """
    
    def __init__(self, root):
        self._rpc = root.object

    def data(self, key):
        """
        Return the raw bytes in an IPFS object. Wrapped into a File-like
        object.

        Methods that work on raw data use file-like objects
        (HTTPResponse acts as a file-like object) for input and output.

        :param key: Key of the object to retrieve
        :return HTTPResponse: The raw bytes of that object
        """
        return self._rpc.data[key]()

    def links(self, key):
        """
        Return the links pointed to by the specified object.

        Example output:
            >>> {'Links': [], 'Hash': 'QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn'}
            >>> print(ex)
        
        :param key: Key of the object to retrieve
        :return dict: A list of links that are dicts that may contain:
            ``Name``: The name of that link
            ``Hash``: The hash of the linked object
            ``Size``: The size of the linked object
        """
        return self._rpc.links[key].with_outputenc(codec.JSON)()

    def get(self, key):
        """
        Return the object, i.e. its data and links.

        Example Ouput:
           >>> ex = {'Links': [{'Hash': 'QmdoDatULjkor1eA1YhBAjmKkkDr7AGEiTrANh7uK17Hfn', 'Size': 4118930, \
           'Name': 'bundle.js'}, {'Hash': 'QmP5BvrMtqWGirZYyHgz77zhEzLiJbonZVdHPMJRM1xe8G', 'Size': 2506050,\
            'Name': 'static'}, {'Hash': 'QmecBJMFtTsn4RawUcqFGudevEWcDUym4b6FtemLtKhZy7', 'Size': 181436, \
            'Name': 'style.css'}], 'Data': b'\x08\x01'}
           >>> print(ex)

        :param key: Key of the object to retrieve
        :return: A dict that may contain:
           ``Data``:  The raw data stored in this object, if any
           ``Links``: See :py:meth:`~ipfs.api.object.ObjectApi.links`, if any. An object without links can cause the Links item to not exist, the Links item being None or the Links item being the empty list.
        """
        return self._rpc.get[key].with_outputenc(PBNode)()

    def put(self, node):
        """
        Store an object.

        Example output:
            >>> ex = {'Hash': 'QmXy2pAWQ3Ef1PqZqi4Z9TJnpDh1trdkCqAvzBgKNNRrSR', 'Links': []}
            >>> print(ex)

        :param node: The node (a.k.a. object) to be stored
        :return: A dict with:
           ``Hash``:  The hash of the object
           ``Links``: The links of the object. See :py:meth:`~ipfs.api.object.ObjectApi.get`.
        """
        return self._rpc.put.with_inputenc(PBNode).with_outputenc(codec.JSON)(_in = node)

    def stat(self, key):
        """
        Return node's statistics.

        Example output::
           >>> ex = {'DataSize': 2, 'NumLinks': 0, \
           'Hash': 'QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn',\
           'CumulativeSize': 4, 'LinksSize': 2, 'BlockSize': 4}
           >>> print(ex))

        :param key: Key of the object to retrieve
        :return: Dict with stats. See example output.
        """
        return self._rpc.stat[key].with_outputenc(JSON)()

    def new(self, template = None):
        """
        Create a new object from an IPFS template.

        :param template: The template name (optional). If no template is
                         specified, an empty node is created.
        :return: Same as :py:meth:`~ipfs.api.object.ObjectApi.put`
        
        """
        return self._rpc.new.with_outputenc(codec.JSON)(template)
    
    def patch(self, key):
        """
        Return the patch API for the specified key.

        :param key: The key to be patched
        :return:    A :py:class:`ObjectPatchApi` object, which can be used to
                    patch an object.
        """
        return ObjectPatchApi(self._rpc, key)


__all__ = [
    "ObjectPatchApi",
    "ObjectApi"
]
