# coding=utf-8
import unittest
from io import BytesIO

__author__ = 'Lorenzo'

from ipfs.api import IpfsApi
from lib.hexdump import print_data, HexDump
from unittest import mock


class TestIPFS(unittest.TestCase):
    REFACTORING = False  # set this flag to skip tests while refactoring the unit

    @classmethod
    def setUpClass(cls):

        cls.KEY1 = 'QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn'
        cls.KEY2 = 'QmR9MzChjp1MdFWik7NjEjqKQMzVmBkdK3dz14A6B5Cupm'
        cls.NODE = {'Data': b'Hello World'}
        cls.BASE_NODE = 'QmXarR6rgkQ2fDSHjSY5nM2kuCXKYGViky5nohtwgF65Ec'

    def setUp(self):
        self.ipfs = IpfsApi()
        # This object holds response
        self.tester = mock.MagicMock()
        self.tester.links = {'Hash': 'QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn', 'Links': []}
        self.tester.chunk = b'\x08\x01'
        # `test_object_get`: the 'Links' value may change based on local ipfs instance
        # it's collected here for documenting the HTTP interface's response
        self.tester.full_object = {
            'Data': self.tester.chunk,
            'Links': [
                {'Size': 4118930, 'Name': 'bundle.js', 'Hash': 'QmdoDatULjkor1eA1YhBAjmKkkDr7AGEiTrANh7uK17Hfn'},
                {'Size': 4761372, 'Name': 'bundle.js.map', 'Hash': 'QmUVYznSyVB32u6jjCjcXmZb7byv832PUC3tuGAJg6SUQz'},
                {'Size': 485, 'Name': 'index.html', 'Hash': 'QmNh5CNBdFkVsALDqzU6AvbFAJd8LpjBV7voojQq95nKDA'},
                {'Size': 2506050, 'Name': 'static', 'Hash': 'QmP5BvrMtqWGirZYyHgz77zhEzLiJbonZVdHPMJRM1xe8G'},
                {'Size': 181436, 'Name': 'style.css', 'Hash': 'QmecBJMFtTsn4RawUcqFGudevEWcDUym4b6FtemLtKhZy7'}
            ]
        }
        self.tester.links = {
            'Links': [],
            'Hash': 'QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn'
        }
        self.tester.node_put = {
            'Links': [],
            'Hash': 'QmXy2pAWQ3Ef1PqZqi4Z9TJnpDh1trdkCqAvzBgKNNRrSR'
        }
        # `test_object_stat`: same as for 'Links' above
        self.tester.stat_full = {
            'CumulativeSize': 4,
            'LinksSize': 2,
            'Hash': 'QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn',
            'NumLinks': 0,
            'DataSize': 2,
            'BlockSize': 4
        }


    @unittest.skipIf(REFACTORING, "REFACTORING")
    def test_hexdump_bytearray_object(self):
        """Create a Py3 Bytearray object from bytes:
        - bytes is a list of integers.
        - bytearray is a Bytes Object"""
        print('###### TEST BYTES OBJECT #######')
        data = self.tester.chunk
        data = bytearray(data)
        print(data, str(type(data)), data.decode())
        print('PASSED')

    @unittest.skipIf(REFACTORING, "REFACTORING")
    def test_object_data(self):
        print('\n###### TEST object.data() ######')
        data = self.ipfs.object.data(self.KEY1)
        data = data.read()
        self.assertTrue(isinstance(data, bytes))
        self.assertTrue(isinstance(data, bytes))
        self.assertEqual(data, self.tester.chunk)
        print(data, str(type(data)))
        print('PASSED')

    @unittest.skipIf(REFACTORING, "REFACTORING")
    def test_object_links(self):
        print('\n###### TEST object.links() ######')
        resp = self.ipfs.object.links(self.KEY1)
        self.assertTrue(isinstance(resp, dict))
        self.assertEqual(resp['Hash'], self.tester.links['Hash'])
        self.assertEqual(len(resp['Links']), 0)
        print(repr(resp))
        print('PASSED')

    @unittest.skipIf(REFACTORING, "REFACTORING")
    def test_object_get(self):
        print('\n###### TEST object.get() ######')
        resp = self.ipfs.object.get(self.KEY2)
        self.assertEqual(resp['Data'], self.tester.full_object['Data'])
        print('PASSED')

    @unittest.skipIf(REFACTORING, "REFACTORING")
    def test_object_put(self):
        print('\n###### TEST object.put() ######')
        resp = self.ipfs.object.put(self.NODE)
        self.assertEqual(resp['Hash'], self.tester.node_put['Hash'])
        print(repr(resp))
        print('PASSED')

    @unittest.skipIf(REFACTORING, "REFACTORING")
    def test_object_stat(self):
        print('\n###### TEST object.stat() ######')
        resp = self.ipfs.object.stat(self.KEY1)
        print(repr(resp))
        print('PASSED')

    @unittest.skip("REFACTORING")
    def test_object_new(self):
        resp = self.ipfs.object.new()
        print(repr(resp))

    @unittest.skip("REFACTORING")
    def test_object_patch_add_link(self):
        resp = self.ipfs.object.patch(self.KEY1).add_link('foo', self.KEY2)
        print(repr(resp))

    @unittest.skip("REFACTORING")
    def test_object_patch_rm_link(self):
        resp = self.ipfs.object.patch(self.KEY2).rm_link('ìndex.html')
        print(repr(resp))

    @unittest.skip("REFACTORING")
    def test_object_patch_set_data(self):
        resp = self.ipfs.object.patch(self.KEY1).set_data(BytesIO(b"foobar"))
        print(repr(resp))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()