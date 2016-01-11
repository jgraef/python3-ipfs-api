# coding=utf-8
"""
Tests:
 - class refactored with the first test case
 - by now they are all flagged "skipped", unflag the ones to be performed

Usage:
    python3 test_ipfsapi.py
"""

import unittest

from hexdump import print_hexdump
from io import BytesIO

from ipfs.api import IpfsApi


class TestIPFS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        cls.KEY1 = 'QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn'
        cls.KEY2 = 'QmR9MzChjp1MdFWik7NjEjqKQMzVmBkdK3dz14A6B5Cupm'
        cls.NODE = {'Data': b'Hello World'}

    def setUp(self):
        self.ipfs = IpfsApi()

    def test_should_return_json_of_root(self):
        """ Use the id() method to retrieve the node's root"""
        resp = self.ipfs.id()
        test_fields = ('Addresses', 'ProtocolVersion', 'ID', 'PublicKey', )
        self.assertTrue(
            all(k in resp.keys() for k in test_fields)
        )
        # print(repr(resp))

    @unittest.skip("debug")
    def test_config_show(self):
        resp = self.ipfs.config.show()
        print(repr(resp))

    @unittest.skip("debug")
    def test_version(self):
        resp = self.ipfs.version()
        print(repr(resp))

    @unittest.skip("debug")
    def test_block_stat(self):
        resp = self.ipfs.block.stat(self.KEY1)
        print(repr(resp))

    @unittest.skip("debug")
    def test_block_get(self):
        resp = self.ipfs.block.get(self.KEY1)
        print_hexdump(resp.read())

    @unittest.skip("debug")
    def test_block_put(self):
        resp = self.ipfs.block.put(BytesIO(b'foobar'))
        print(repr(resp))

    @unittest.skip("debug")
    def test_dht_get(self):
        resp = self.ipfs.dht.get(self.KEY1)
        print(list(resp))

    @unittest.skip("debug")
    def test_dht_put(self):
        resp = self.ipfs.dht.put('test', 'foobar')
        print(list(resp))

    @unittest.skip("debug")
    def test_dht_find_providers(self):
        resp = self.ipfs.dht.find_providers(self.KEY1)
        print(list(resp))

    # TODO: test other DHT commands

    @unittest.skip("debug")
    def test_object_data(self):
        resp = self.ipfs.object.data(self.KEY1)
        print_hexdump(resp.read())

    @unittest.skip("debug")
    def test_object_links(self):
        resp = self.ipfs.object.links(self.KEY1)
        print(repr(resp))

    @unittest.skip("debug")
    def test_object_get(self):
        resp = self.ipfs.object.get(self.KEY2)
        print(repr(resp))

    @unittest.skip("debug")
    def test_object_put(self):
        resp = self.ipfs.object.put(self.NODE)
        print(repr(resp))

    @unittest.skip("debug")
    def test_object_stat(self):
        resp = self.ipfs.object.stat(self.KEY1)
        print(repr(resp))

    @unittest.skip("debug")
    def test_object_new(self):
        resp = self.ipfs.object.new()
        print(repr(resp))

    @unittest.skip("debug")
    def test_object_patch_add_link(self):
        resp = self.ipfs.object.patch(self.KEY1).add_link('foo', self.KEY2)
        print(repr(resp))

    @unittest.skip("debug")
    def test_object_patch_rm_link(self):
        resp = self.ipfs.object.patch(self.KEY2).rm_link('ìndex.html')
        print(repr(resp))

    @unittest.skip("debug")
    def test_object_patch_set_data(self):
        resp = self.ipfs.object.patch(self.KEY1).set_data(BytesIO(b"foobar"))
        print(repr(resp))

    def test_resolve(self):
        resp = self.ipfs.resolve(self.KEY2 + "/static")
        self.assertEqual(resp, {'Path': '/ipfs/QmP5BvrMtqWGirZYyHgz77zhEzLiJbonZVdHPMJRM1xe8G'})
    
    def tearDown(self):
        del self.ipfs

    @classmethod
    def tearDownClass(cls):
        del cls


if __name__ == '__main__':
    unittest.main()

