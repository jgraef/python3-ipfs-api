# coding=utf-8
import unittest
from io import BytesIO

__author__ = 'Lorenzo'

from ipfs.api import IpfsApi
from lib.hexdump import print_hexdump


class TestBlockAPI(unittest.TestCase):
    DEBUG = True  # set this flag to skip tests while refactoring the unit

    @classmethod
    def setUpClass(cls):

        cls.KEY1 = 'QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn'
        cls.KEY2 = 'QmR9MzChjp1MdFWik7NjEjqKQMzVmBkdK3dz14A6B5Cupm'
        cls.NODE = {'Data': b'Hello World'}

    def setUp(self):
        self.ipfs = IpfsApi()

    @unittest.skipIf(DEBUG, "debug")
    def test_should_return_block_statistics(self):
        """Use the Block class' stat method to retrieve size and key"""
        resp = self.ipfs.block.stat(self.KEY1)

        self.assertTrue(
            all(k in resp.keys() for k in test_dict.keys())
        )

        self.assertEqual(resp["Size"], 4)
        self.assertEqual(resp["Key"], self.KEY1) 

    @unittest.skipIf(DEBUG, "debug")
    def test_should_return_block_information(self):
        """Use the Block class' get() method"""
        resp = self.ipfs.block.get(self.KEY1)

        self.assertEqual(resp.read(), b'\n\x02\x08\x01')


    @unittest.skipIf(DEBUG, "debug")
    def test_should_store_string_bytes_in_block(self):
        """Use the Block class' put() method"""
        resp = self.ipfs.block.put(BytesIO(b'foobar'))

        self.assertEqual(resp['Size'], 6)
        self.assertEqual(resp['Key'], 'QmbWTwYGcmdyK9CYfNBcfs9nhZs17a6FQ4Y8oea278xx41')
