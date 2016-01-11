"""
    merkledag - High-level interface to the IPFS merkledag
"""

from threading import Lock



class Link:
    """ A link in the merkledag that links another node. """
    
    def __init__(self, dag, name, hash, size):
        self._dag = dag
        self.name = name
        self.hash = hash
        self.size = size


    def follow(self):
        """ Returns the references node. """
        
        return self._dag.get(self.hash)


    def __repr__(self):
        return "Link(name={}, hash={}, size={:d})".format(self.name, self.hash, self.size)



class Node:
    """ A merkledag node (a.k.a object). """
    
    def __init__(self, dag, hash):
        self._dag = dag
        self.hash = hash
        self._data = None
        self._links = None
        self._links_map = None
        self._loaded = False
        self._lock = Lock()


    # TODO: split lazy loading of data and links
    def _lazy_load_data(self):
        with self._lock:
            if (self._data != None):
                return

        data = self._dag.ipfs.object.data(self.hash).read()

        with self._lock:
            self._data = data


    def _lazy_load_links(self):
        with self._lock:
            if (self._links != None):
                return

        links = self._dag.ipfs.object.links(self.hash)["Links"]

        with self._lock:
            self._links = [Link(self._dag, l["Name"], l["Hash"], l["Size"]) for l in links]
            self._links_map = {}
            for l in self._links:
                self._links_map[l.name] = l


    @property
    def ref(self):
        """ The reference URL, e.g. "/ipfs/QmPXME1oRtoT627YKaDPDQ3PwA8tdP9rWuAAweLzqSwAWT". """
        return "/ipfs/" + self.hash


    @property
    def data(self):
        """ The data contained in this node. """
        self._lazy_load_data()
        return self._data


    @property
    def links(self):
        """ A list of the links contained in this node. """
        self._lazy_load_links()
        return self._links


    def get_link(self, name):
        """ Returns a link given its name. """
        self._lazy_load_links()
        return self._links_map[name]


    def has_link(self, name):
        return name in self._links_map


    def get_node(self, name):
        """ Returns a linked node given the link's name. """
        return self.get_link(name).follow()


    """ TODO: 
    def add_link(self, name, target):
        if (isinstance(target, Node)):
            ref = target.ref
        elif (isinstance(target, str)):
            ref = "/ipfs/" + target
        else:
            raise ValueError("Invalid link target: {!r}".format(target))

        res = self._dag.ipfs.object_patch_add_link(self.hash, name, ref)
        print(res)


    def rm_link(self, name):
        res = self._dag.ipfs.object_patch_rm_link(self.hash, name)
        print(res)


    def set_data(self, data):
        res = self._dag.ipfs.object_patch_set_data(self.hash, data)
        print(res)


    def append_data(self, data):
        res = self._dag.ipfs.object_patch_append_data(self.hash, data)
        print(res)
    """

    def __getitem__(self, name):
        return self.get_node(name)


    def __contains__(self, name):
        return self.has_link(name)


    def __getattr__(self, name):
        try:
            return self.get_node(name)
        except KeyError:
            raise AttributeError(name)


    def __hasattr__(self, name):
        return self.has_link(name)


    def __iter__(self):
        return iter(self.links)


    def __repr__(self):
        return "Node({})".format(self.hash)


    def __str__(self):
        return str(self.data)


    def __hash__(self):
        return hash(self.hash)


    def __eq__(self, other):
        return isinstance(other, Node) and other.hash == self.hash




class NodeBuilder:
    """ Creates nodes. """
    
    def __init__(self, dag):
        self._dag = dag
        self._data = b""
        self._links = {}


    def data(self, data):
        """ Set the data that should be contained in the new node. """
        if (type(data) == bytes):
            pass
        elif (type(data) == str):
            data = data.encode()
        else:
            raise TypeError("Data must be bytes or string")
        
        self._data = data
        
        return self


    def link(self, name, target, size = 0):
        if (isinstance(target, Node)):
            hash = target.hash
        elif (isinstance(target, str)):
            hash = target
        else:
            raise ValueError("Invalid link target: {!r}".format(target))

        if (name in self._links):
            raise ValueError("Duplicate link name: {}".format(name))

        self._links[name] = (hash, size)

        return self


    def build(self):
        links = [{"Name": name, "Hash": l[0], "Size": l[1]} for name, l in self._links.items()]
        node = {"Data": self._data, "Links": links}
        res = self._dag.ipfs.object.put(node)
        return self._dag.get(res["Hash"])



class Merkledag:
    def __init__(self, ipfs):
        self.ipfs = ipfs


    def get(self, ref):
        if (ref.startswith("/ipns/") or ref.startswith("/ipfs")):
            hash = self.ipfs.resolve(ref)["Path"][6:]
        else:
            hash = ref

        return Node(self, hash)


    def __getitem__(self, hash):
        return self.get(hash)


    def builder(self):
        return NodeBuilder(self)
