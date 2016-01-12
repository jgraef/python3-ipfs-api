from ipfs.api import IpfsApi
from ipfs.merkledag import Merkledag


# This example will recursively follow links and list all hashes and their
# link names.


# Remember all nodes that we already listet
nodes_seen = set()

def list_node(node, indent = 0):
    # make string for indentation
    str_indent = " " * indent
    
    # check if we already listet that node
    if (node in nodes_seen):
        print("{}already listed".format(str_indent))
        return
    
    # remember the node
    nodes_seen.add(node)

    # print all links    
    for link in node:
        print("{} - {}: {}".format(str_indent, link.name, link.hash))
        # list node recursively
        list_node(link.follow(), indent + 1)


# connect to the IPFS daemon
ipfs = IpfsApi()

# get Merkledag
dag = Merkledag(ipfs)

# list nodes
list_node(dag["QmR9MzChjp1MdFWik7NjEjqKQMzVmBkdK3dz14A6B5Cupm"])
