from hexdump import print_hexdump
from io import BytesIO

from ipfs.api import IpfsApi



KEY1 = "QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn"
KEY2 = "QmR9MzChjp1MdFWik7NjEjqKQMzVmBkdK3dz14A6B5Cupm"
NODE = {'Data': b'Hello World'}

ipfs = IpfsApi()



def test_id():
    resp = ipfs.id()
    print(repr(resp))


def test_version():
    resp = ipfs.version()
    print(repr(resp))


def test_block_stat():
    resp = ipfs.block.stat(KEY1)
    print(repr(resp))


def test_block_get():
    resp = ipfs.block.get(KEY1)
    print_hexdump(resp.read())


def test_block_put():
    resp = ipfs.block.put(BytesIO(b"foobar"))
    print(repr(resp))
    


def test_dht_get():
    resp = ipfs.dht.get(KEY1)
    print(list(resp))


def test_dht_put():
    resp = ipfs.dht.put("test", "foobar")
    print(list(resp))


def test_dht_find_providers():
    resp = ipfs.dht.find_providers(KEY1)
    print(list(resp))

# TODO: test other DHT commands

def test_object_data():
    resp = ipfs.object.data(KEY1)
    print_hexdump(resp.read())

def test_object_links():
    resp = ipfs.object.links(KEY1)
    print(repr(resp))

def test_object_get():
    resp = ipfs.object.get(KEY2)
    print(repr(resp))

def test_object_put():
    resp = ipfs.object.put(NODE)
    print(repr(resp))

def test_object_stat():
    resp = ipfs.object.stat(KEY1)
    print(repr(resp))

def test_object_new():
    resp = ipfs.object.new()
    print(repr(resp))

def test_object_patch_add_link():
    resp = ipfs.object.patch(KEY1).add_link("foo", KEY2)
    print(repr(resp))

def test_object_patch_rm_link():
    resp = ipfs.object.patch(KEY2).rm_link("index.html")
    print(repr(resp))

def test_object_patch_set_data():
    resp = ipfs.object.patch(KEY1).set_data(BytesIO(b"foobar"))
    print(repr(resp))


if (__name__ == "__main__"):
    test_id()
    #test_version()
    
    #test_block_stat()
    #test_block_get()
    #test_block_put()

    #test_dht_get()
    #test_dht_put()
    #test_dht_find_providers()

    #test_object_data()
    #test_object_links()
    #test_object_get()
    #test_object_put()
    #test_object_stat()
    #test_object_new()

    #test_object_patch_add_link()
    #test_object_patch_rm_link()
    #test_object_patch_set_data() TODO Not implemented
    
