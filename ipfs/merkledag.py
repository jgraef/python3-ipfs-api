"""
This module is a high-level abstraction to the ipfs.object API.

It provides a pythonic way of interacting with merkledag nodes (a.k.a. objects).

To run the following examples start with::

   >>> from ipfs.api import IpfsApi
   >>> from ipfs.merkledag import Merkledag
   >>> dag = Merkledag(IpfsApi())

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
        """
        Return the referenced node.

        Example::

           >>> node = dag["QmXarR6rgkQ2fDSHjSY5nM2kuCXKYGViky5nohtwgF65Ec"]
           >>> link = node.get_link("readme")
           >>> readme = link.follow()
           >>> readme
           Node(QmPZ9gcCEpqKTo6aq61g2nXGUhM4iCL3ewB6LDXZCtioEB)
           >>> readme.data[5:22].decode()
           'Hello and Welcome'

        Normally you don't have to interact with links. You can directly
        follow links by referencing attributes of a Node.
        """
        
        return self._dag.get(self.hash)


    def __repr__(self):
        return "Link(name={}, hash={}, size={:d})".format(self.name, self.hash, self.size)



class Node:
    """ A merkledag node (a.k.a object).

        A merkledag node is a node like in any other graph. It stores some data
        and can have multiple links (or edges) to other nodes.

        To get a merkledag node call ``dag.get(ref)``, where ``ref`` can be
        a ipfs or ipns name or a plain base58 hash of your node::

           >>> dag["QmXarR6rgkQ2fDSHjSY5nM2kuCXKYGViky5nohtwgF65Ec"]
           Node(QmXarR6rgkQ2fDSHjSY5nM2kuCXKYGViky5nohtwgF65Ec)

        The data of a node can be accessed via its ``data`` attribute::

           >>> n = dag["QmPZ9gcCEpqKTo6aq61g2nXGUhM4iCL3ewB6LDXZCtioEB"]
           >>> n.data[5:22].decode()
           'Hello and Welcome'

        Links can be followed by directly accessing attributes::

           >>> node = dag["QmXarR6rgkQ2fDSHjSY5nM2kuCXKYGViky5nohtwgF65Ec"]
           >>> node.readme
           Node(QmPZ9gcCEpqKTo6aq61g2nXGUhM4iCL3ewB6LDXZCtioEB)

    """
    
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
        """
        The data contained in this node.

        At this moment merkledag nodes always contain bytes objects. This could
        be changed in the future (i.e store any pickable python object), but
        backwards compability will not be broken.
        """
        self._lazy_load_data()
        return self._data


    @property
    def links(self):
        """ A list of the links contained in this node. """
        self._lazy_load_links()
        return self._links


    def get_link(self, name):
        """
        Return a link by its name.

        :param name: The link name
        :return:     The link with that name
        """
        self._lazy_load_links()
        return self._links_map[name]


    def has_link(self, name):
        """
        Return whether this node has a link with the given name.

        :param name: The link name
        :return:     True if a link with that name exists, False otherwise.
        """
        return name in self._links_map


    def get_node(self, name):
        """
        Return a linked node given the link's name.

        :param name: The link name
        :return:     The node linked by this name

        This is a shortcut for ``node.get_link(name).follow()``
        """
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
    """
    The NodeBuilder is used to create new nodes.

    Currently it's the only mechanism available to create a node. Soon there
    will be methods to *patch* a node in order to create new nodes.

    Example::
    
       >>> c1 = dag.builder().data("Child 1").build()
       >>> c2 = dag.builder().data("Child 2").link("sibling", c1).build()
       >>> r = dag.builder().data("Root")\
               .link("child_1", c1).link("child_2", c2).build()
       >>> r
       Node(Qme2Fuk2YRNWwbhQ9G4d3GBAEQ5kL1r8P1b5RVx1HgZsco)

    Try exploring that in your DAG browser:
    http://localhost:5001/ipfs/QmR9MzChjp1MdFWik7NjEjqKQMzVmBkdK3dz14A6B5Cupm/#/objects/object/\ipfs\Qme2Fuk2YRNWwbhQ9G4d3GBAEQ5kL1r8P1b5RVx1HgZsco
    """
    
    def __init__(self, dag):
        self._dag = dag
        self._data = b""
        self._links = {}


    def data(self, data):
        """
        Set the data that will be contained in the new node.

        :param data: A bytes object or string that will be the node's content.
        :return:     The builder itself to allow chaining.
        """
        
        if (type(data) == bytes):
            pass
        elif (type(data) == str):
            data = data.encode()
        else:
            raise TypeError("Data must be bytes or string")
        
        self._data = data
        
        return self


    def link(self, name, target, size = 0):
        """
        Set a link that will be added to the node.

        :param name:   The link name
        :param target: The merkledag node or hash to which the link points
        :param size:   The cumulative size of the linked node (optional)
        :return:     The builder itself to allow chaining.
        """
        
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
        """
        Return the node built by this builder.

        :return: The node with the specified data and links
        """

        links = [{"Name": name, "Hash": l[0], "Size": l[1]} for name, l in self._links.items()]
        node = {"Data": self._data, "Links": links}
        res = self._dag.ipfs.object.put(node)
        return self._dag.get(res["Hash"])



class Merkledag:
    """
    The root for all merkledag operations.

    To get a node try::

       >>> dag = Merkledag(IpfsApi())
       >>> dag["QmPZ9gcCEpqKTo6aq61g2nXGUhM4iCL3ewB6LDXZCtioEB"]
       Node(QmPZ9gcCEpqKTo6aq61g2nXGUhM4iCL3ewB6LDXZCtioEB)

    or::

       >>> dag["/ipfs/QmXarR6rgkQ2fDSHjSY5nM2kuCXKYGViky5nohtwgF65Ec/readme"]
       Node(QmPZ9gcCEpqKTo6aq61g2nXGUhM4iCL3ewB6LDXZCtioEB)

    or::

       >>> dag["/ipns/<your peer ID>"]

    """
    
    def __init__(self, ipfs):
        """
        Create an instance of a merkledage.

        :param ipfs: An IpfsApi instance
        """
        self.ipfs = ipfs


    def get(self, ref):
        """
        Return a merkledag node by it's reference.

        :param ref: Either a IPNS or IPFS name or a plain base58 hash to a node
        :return:    The references node
        """
        
        if (ref.startswith("/ipns/") or ref.startswith("/ipfs")):
            hash = self.ipfs.resolve(ref)["Path"][6:]
        else:
            hash = ref

        return Node(self, hash)


    def __getitem__(self, hash):
        return self.get(hash)


    def builder(self):
        return NodeBuilder(self)



__all__ = [
    "Link",
    "Node",
    "NodeBuilder",
    "Merkledag"
]

