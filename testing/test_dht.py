# coding=utf-8
import unittest

__author__ = 'Lorenzo'

from ipfs.api import IpfsApi


class TestDHT(unittest.TestCase):
    DEBUG = True  # set this flag to skip tests while debugging the unit

    @classmethod
    def setUpClass(cls):

        cls.KEY1 = 'QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn'
        cls.KEY2 = 'QmR9MzChjp1MdFWik7NjEjqKQMzVmBkdK3dz14A6B5Cupm'
        cls.NODE = {'Data': b'Hello World'}

    def setUp(self):
        self.ipfs = IpfsApi()


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