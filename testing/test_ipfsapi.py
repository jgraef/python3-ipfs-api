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
    """These test cases need a running daemon. Use a VM or a IPFS test node.

    Use the `DEBUG` class attribute and the decorator to skip tests or run only some.

    #todo: implement mocks where possible
    """

    DEBUG = True  # set this flag to skip tests while debugging the unit

    @classmethod
    def setUpClass(cls):

        cls.KEY1 = 'QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn'
        cls.KEY2 = 'QmR9MzChjp1MdFWik7NjEjqKQMzVmBkdK3dz14A6B5Cupm'
        cls.NODE = {'Data': b'Hello World'}

    def setUp(self):
        self.ipfs = IpfsApi()

    @unittest.skipIf(DEBUG, "debug")
    def test_should_return_dict_of_root(self):
        """Use the IPFS class' id() method to retrieve the node's root"""
        resp = self.ipfs.id()
        test_fields = ('Addresses', 'ProtocolVersion', 'ID', 'PublicKey', )
        self.assertTrue(
            all(k in resp.keys() for k in test_fields)
        )
        # print(repr(resp))

    @unittest.skipIf(DEBUG, "debug")
    def test_should_return_node_configuration(self):
        """Use the ConfigAPI to return node's configuration"""
        resp = self.ipfs.config.show()

        # check integrity of configuration dict keys
        # #todo: @mec-is add subkeys and checks
        test_dict = {
            'Identity': [],
            'API': [],
            'Datastore': [],
            'Tour': [],
            'Addresses': [],
            'Swarm': [],
            'SupernodeRouting': [],
            'Version': [],
            'Bootstrap': [],
            'Gateway': [],
            'Mounts': [],
            'Ipns': [],
            'Discovery': []
        }

        #for k, v in resp.items():
            #print(k, '>>>', v)

        self.assertTrue(
            all(k in resp.keys() for k in test_dict.keys())
        )
        # #todo: @jgraef add in a comment here requirements for this test case
        # #todo: i.e. constraints on certain value in resp dictionary or any other
        # #todo: possible heck to control integrity and consistency of the data if not trivial

        # print(repr(resp))

    @unittest.skipIf(DEBUG, "debug")
    def test_should_return_version_information(self):
        """Use the IPFS class' version() to return information on version, number of repo and commits"""
        resp = self.ipfs.version()

        # check integrity of configuration dict keys
        test_dict = {
            'Version': str,
            'Repo': str,
            'Commit': str
        }

        # for k, v in resp.items():
            # print(k, '>>>', str(type(v)))

        self.assertTrue(
            all(k in resp.keys() for k in test_dict.keys())
        )
        self.assertTrue(
            all(str(type(resp[k])) == str(test_dict[k]) for k in test_dict.keys())
        )

        # print(repr(resp))

    @unittest.skipIf(DEBUG, "debug")
    def test_should_return_block_statistics(self):
        """Use the Block class' stat method to retrieve size and key"""
        resp = self.ipfs.block.stat(self.KEY1)

        test_dict = {
            'Size': int,
            'Key': 'hash'
        }

        self.assertTrue(
            all(k in resp.keys() for k in test_dict.keys())
        )

        # #todo: @jgraef implement assertTrue with a validity check of the hash in 'Key'

        #self.assertTrue(
        #    all(str(type(resp[k])) == str(test_dict[k]) for k in test_dict.keys())
        #)

        #print(repr(resp))

    @unittest.skipIf(DEBUG, "debug")
    def test_should_return_block_information(self):
        """Use the Block class' get() method"""
        resp = self.ipfs.block.get(self.KEY1)

        # #todo: @jgraef implement assertTrue with a validity check for the output of print_hexdump

        print_hexdump(resp.read())

    @unittest.skipIf(DEBUG, "debug")
    def test_should_store_string_bytes_in_block(self):
        """Use the Block class' put() method"""
        resp = self.ipfs.block.put(BytesIO(b'foobar'))

        self.assertEqual(resp['Size'], 6)
        #print(repr(resp))

    @unittest.skipIf(DEBUG, "debug")
    def test_should_return_value_from_distributed_hash_table(self):
        """Use the DhtApi class' get() method, huge list of resources from other nodes (I suppose)"""
        # #todo: @jgraef how we can test this output?
        resp = self.ipfs.dht.get(self.KEY1)
        print(list(resp)[:2])

    @unittest.skipIf(DEBUG, "debug")
    def test_should_put_key_value_into_distributed_hash_table(self):
        """Use the DhtApi class' put() method"""
        # #todo: @jgraef how we can test this output?
        resp = self.ipfs.dht.put('test', 'foobar')
        print(list(resp))

    @unittest.skipIf(DEBUG, "debug")
    def test_should_find_providers_for_dht(self):
        """Use the DhtApi class' find_providers() method"""
        resp = self.ipfs.dht.find_providers(self.KEY1)
        print(list(resp))

    # TODO: test other DHT commands

    @unittest.skipIf(DEBUG, "debug")
    def test_object_data(self):
        resp = self.ipfs.object.data(self.KEY1)
        print_hexdump(resp.read())

    @unittest.skipIf(DEBUG, "debug")
    def test_object_links(self):
        resp = self.ipfs.object.links(self.KEY1)
        print(repr(resp))

    @unittest.skipIf(DEBUG, "debug")
    def test_object_get(self):
        resp = self.ipfs.object.get(self.KEY2)
        print(repr(resp))

    @unittest.skipIf(DEBUG, "debug")
    def test_object_put(self):
        resp = self.ipfs.object.put(self.NODE)
        print(repr(resp))

    @unittest.skipIf(DEBUG, "debug")
    def test_object_stat(self):
        resp = self.ipfs.object.stat(self.KEY1)
        print(repr(resp))

    @unittest.skipIf(DEBUG, "debug")
    def test_object_new(self):
        resp = self.ipfs.object.new()
        print(repr(resp))

    @unittest.skipIf(DEBUG, "debug")
    def test_object_patch_add_link(self):
        resp = self.ipfs.object.patch(self.KEY1).add_link('foo', self.KEY2)
        print(repr(resp))

    @unittest.skipIf(DEBUG, "debug")
    def test_object_patch_rm_link(self):
        resp = self.ipfs.object.patch(self.KEY2).rm_link('ìndex.html')
        print(repr(resp))

    @unittest.skipIf(DEBUG, "debug")
    def test_object_patch_set_data(self):
        resp = self.ipfs.object.patch(self.KEY1).set_data(BytesIO(b"foobar"))
        print(repr(resp))

    @unittest.skipIf(DEBUG, "debug")
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

