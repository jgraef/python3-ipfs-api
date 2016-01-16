# coding=utf-8
"""
Tests:
 - class refactored with the first test case
 - by now they are all flagged "skipped", unflag the ones to be performed

Usage:
    python3 test_ipfsapi.py
"""

import unittest
import io
from hashlib import sha1

from ipfs.api import IpfsApi
from ipfs.unixfs import UnixFs


class TestUnixFs(unittest.TestCase):
    """These test cases need a running daemon. Use a VM or a IPFS test node.

    Use the `DEBUG` class attribute and the decorator to skip tests or run only some.

    #todo: implement mocks where possible
    """

    DEBUG = False  # set this flag to skip tests while debugging the unit

    @classmethod
    def setUpClass(cls):
        cls.KEY_LOGO_PNG = "QmUYndb1SkY49khYAg9Zn2yp9Z44cRFtqMnVAZP5qes8ce"
        cls.HASH_LOGO_PNG = "026423abaa74bfb92287b467ed88afbf5958df73"
        cls.KEY_WORLD_JPEG = "QmYGVhjTfVvBAAf2SAWMJsTDheo7UuyjQigGahmB8YU3ZH"
        cls.HASH_WORLD_JPEG = "8de181b2c86088e941f2127d6338e60fb9d8b4c5"
        cls.KEY_DIR = "QmR9MzChjp1MdFWik7NjEjqKQMzVmBkdK3dz14A6B5Cupm"
        cls.FILES_IMG_DIR = ('bug.png', 'dark-world.jpg', 'favicon.ico', 'git.png', 'help.png', 'info.png', 'log.png', 'logo.png', 'world.jpg')
        

    def setUp(self):
        self.fs = UnixFs(IpfsApi())        

    @unittest.skipIf(DEBUG, "debug")
    def test_small_file_readall(self):
        with self.fs.open(self.KEY_LOGO_PNG, "rb") as f:
            self.assertEqual(self.HASH_LOGO_PNG, sha1(f.read()).hexdigest())

    @unittest.skipIf(DEBUG, "debug")
    def test_big_file_readall(self):
        with self.fs.open(self.KEY_WORLD_JPEG, "rb") as f:
            self.assertEqual(self.HASH_WORLD_JPEG, sha1(f.read()).hexdigest())

    @unittest.skipIf(DEBUG, "debug")
    def test_small_file_seek_and_read(self):
        with self.fs.open(self.KEY_LOGO_PNG, "rb") as f:
            self.assertEqual(64, f.seek(64, io.SEEK_CUR))
            self.assertEqual(128, f.seek(64, io.SEEK_CUR))
            self.assertEqual(256, f.seek(256, io.SEEK_SET))
            self.assertEqual(24610, f.seek(-256, io.SEEK_END))
            self.assertEqual(
                b'\x04$\x00_\x85$\xfb^\xf8\xe8]\x7f;}\xa8\xb7',
                f.read(16))

    @unittest.skipIf(DEBUG, "debug")
    def test_readinto(self):
        buf = bytearray(32)
        with self.fs.open(self.KEY_LOGO_PNG, "rb") as f:
            self.assertEqual(32, f.readinto(buf))
            self.assertEqual(
                b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x02\x80\x00\x00\x01\x00\x08\x06\x00\x00\x00#\x95\xc7',
                buf)

    @unittest.skipIf(DEBUG, "debug")
    def test_read_and_tell(self):
        with self.fs.open(self.KEY_LOGO_PNG, "rb") as f:
            self.assertEqual(0, f.tell())
            f.read(16)
            self.assertEqual(16, f.tell())

    def test_dir_by_key(self):
        d = self.fs.dir(self.KEY_DIR)
        self.assertEqual(
            "/ipfs/" + self.KEY_DIR,
            d.path)
        self.assertEqual(
            ('bundle.js', 'bundle.js.map', 'index.html', 'static', 'style.css'),
            d.listdir())

    def test_dir_relative_simple(self):
        d = self.fs.dir(self.KEY_DIR)
        d2 = d.dir("static")
        self.assertEqual(
            "/ipfs/QmR9MzChjp1MdFWik7NjEjqKQMzVmBkdK3dz14A6B5Cupm/static",
            d2.path)
        self.assertEqual(
            ('fonts', 'img'),
            d2.listdir())

    def test_dir_relative(self):
        d = self.fs.dir(self.KEY_DIR)
        d2 = d.dir("static")
        d3 = d2.dir("img")
        d4 = d.dir("static/img")
        self.assertEqual(
            "/ipfs/QmR9MzChjp1MdFWik7NjEjqKQMzVmBkdK3dz14A6B5Cupm/static/img",
            d3.path)
        self.assertEqual(self.FILES_IMG_DIR, d3.listdir())
        self.assertEqual(d3, d4)
        self.assertEqual(
            "/ipfs/QmR9MzChjp1MdFWik7NjEjqKQMzVmBkdK3dz14A6B5Cupm/static/img",
            d4.path)
        self.assertEqual(self.FILES_IMG_DIR, d4.listdir())

    def test_dir_read_file(self):
        d = self.fs.dir(self.KEY_DIR)
        d2 = d.dir("static/img")
        with d2.file("logo.png").open("rb") as f:
            self.assertEqual(self.HASH_LOGO_PNG, sha1(f.read()).hexdigest())
        


    def tearDown(self):
        del self.fs

    @classmethod
    def tearDownClass(cls):
        del cls


if __name__ == '__main__':
    unittest.main()

