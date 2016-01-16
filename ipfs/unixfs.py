"""
The unixfs module implements pythonic file-abstractions for unixfs files.

Currently only reading files is implemented.

You need an instance of :py:class:`UnixFs` to access the unixfs.

Example::
    >>> from ipfs.api import IpfsApi
    >>> from ipfs.unixfs import UnixFs
    >>> fs = UnixFs(IpfsApi())
    >>> with fs.open("QmPZ9gcCEpqKTo6aq61g2nXGUhM4iCL3ewB6LDXZCtioEB") as f:
	    print(f.read())
    Hello and Welcome to IPFS!
    ...

"""

from .proto.unixfs import UnixFsProtocol
from .merkledag import Merkledag
from . import codec
import io
from bintrees import FastAVLTree


# TODO: document the semantics of changes


class ModeParser:
    """
    Parser for mode strings (e.g "r+b").

    This is only used internally.
    """

    def __init__(self, mode):
        self.reading = None
        self.writing = None
        self.trunc = None
        self.append = False
        self.text = None
        self.mode = mode


    def invalid(self):
        raise IOError("Invalid mode: {!r}".format(self.mode))


    def parse(self):
        if (not self.mode):
            self.invalid()

        self.parse_primary(self.mode[0])
        if (self.mode[1:2] == "+"):
            if (self.reading):
                self.writing = True
            self.reading = True
            self.parse_enc(self.mode[2:])
        else:
            self.parse_enc(self.mode[1:])

        
    def parse_primary(self, c):
        if (c == "r"):
            self.reading = True
            self.writing = False
            self.trunc = False
        elif (c == "w"):
            self.reading = False
            self.writing = True
            self.trunc = True
        elif (c == "a"):
            self.reading = False
            self.writing = True
            self.append = True
            self.trunc = False
        else:
            self.invalid()


    def parse_enc(self, c):
        if (c == "" or c == "t"):
            self.text = True
        elif (c == "b"):
            self.text = False
        else:
            self.invalid()



class Inode:
    """
    An Inode can be a directory, file or file block. It implements the mechanism
    to update the underlying node and notify its parents when a child changes.
    """

    def __init__(self, node, parent, link_index):
        """
        Create an Inode instance.

        :param node: The underlying node (see :py:class:`~ipfs.merkledag.Node`)
        :param parent: The parent Inode or ``None``
        :param link_index: The index of the link in the parent node where this
                           node is linked.
        """

        self._node = node
        self._parent = parent
        self._link_index = link_index
        self._observers = []


    def _child_changed(self, child):
        self._patch_link(child)


    def _data_changed(self, new_data):
        nb = self._node._dag.builder().value(new_data)
        for link in self._node.links:
            nb.link(link.name, link.hash, link.size)
        self._node = nb.build()

        self._propagate_change()


    def _patch_link(self, child):
        links = list(self._node.links)
        old_link = links[self._link_index]
        # TODO: set correct size in link
        links[self._link_index] = Link(self._node._dag, old_link.name, self._node.hash, 0)
        nb = self._node._dag.builder().value(self._node.value)
        for link in links:
            nb.link(link.name, link.hash, link.size)
        self._node = nb.build()
        
        self._propagate_change()


    def _propagate_change(self):
        for observer in self._observers:
            observer(self)
        if (self._parent):
            self._parent._child_changed(self)


    def __eq__(self, other):
        return isinstance(other, Inode) and self._node == other._node


    def observe(self, observer):
        """
        Add an observer. The observer gets notified when the node changed.

        :param observer: A function that takes an :py:class`Inode` as argument.
        """

        self._observers.append(observer)



class FileBlock(Inode):
    """
    Files are split into blocks by unixfs. This class represents such a block.
    """
    
    def __init__(self, node, parent, link_index, offset, size):
        """
        Create an instance of :py:class`FileBlock`

        :param node: The underlying node (see :py:class:`~ipfs.merkledag.Node`)
        :param parent: The parent Inode or ``None``
        :param link_index: The index of the link in the parent node where this
                           node is linked.
        :param offset: At which offset in the file this block belongs to
        :param size:   The size of the block
        """

        Inode.__init__(self, node, parent, link_index)
        self.offset = offset
        self.size = size

    def __repr__(self):
        return "<FileBlock {} [{:d} : {:d}]>".format(self._node.hash, self.offset, self.offset + self.size)



class FileStream(io.RawIOBase):
    """
    This class implements the :py:class:`~io.RawIOBase` interface. Thus you can
    use it as any other file opened by :py:func:`open`.
    """
    
    def __init__(self, file, mode):
        self._file = file
        self._mode = mode
        
        self._readable = mode.reading
        self._writable = mode.writing

        # TODO: Use size from underlying file
        if (mode.trunc):
            self._file._trunc(0)
        self._pos = self._size if (mode.append) else 0


    def close(self):
        if (not self.closed):
            self.flush()
        

    def flush(self):
        if (self._writable):
            pass # TODO


    def readable(self):
        return self._mode.reading


    def writable(self):
        return self._mode.writing


    def seekable(self):
        return True


    def readinto(self, buf):
        if (not self._mode.reading):
            raise io.UnsupportedOperation("File not opened for reading")
        n = self._file._readinto(buf, self._pos, len(buf))
        self._pos += n
        return n


    def readall(self):
        return self.read(-1)


    def read(self, n = -1):
        if (n == -1):
            n = self._file._filesize
        buf = bytearray(n)
        n = self.readinto(buf)
        return bytes(buf[0:n])


    def write(self):
        raise NotImplementedError()


    def seek(self, offset, whence):
        if (whence == io.SEEK_SET):
            self._pos = offset
        elif (whence == io.SEEK_CUR):
            self._pos += offset
        elif (whence == io.SEEK_END):
            self._pos = self._file._filesize + offset
        return self._pos


    def tell(self):
        return self._pos


    def truncate(self, size = None):
        if (size == None):
            size = self._pos
        self._file._trunc(size)


class BlockIndex:
    def __init__(self):
        self.avl = FastAVLTree()

    def add_block(self, block):
        self.avl[block.offset + block.size] = block

    def get_blocks(self, start, length):
        end = start + length
        found_block = False
        for key, block in self.avl.iter_items(start, end):
            found_block = True
            yield block
        try:
            if (found_block):
                _, block = self.avl.succ_item(key)
                if (block.offset < end):
                    yield block
            else:
                _, block = self.avl.ceiling_item(start)
                yield block
        except KeyError:
            pass

    def get_chunks(self, offset, length):
        for block in self.get_blocks(offset, length):
            assert length >= 0
            if (length == 0):
                break
            if (block.offset <= offset and offset < block.offset + block.size):
                chunk_offset = offset - block.offset
                chunk_size = min((length, block.size - chunk_offset))
                yield (chunk_offset, chunk_size, block)
                offset += chunk_size
                length -= chunk_size



class File(Inode):
    """
    A unixfs file.

    Call :py:meth:`~File.open` to open it.
    """

    def __init__(self, node, parent, link_index):
        Inode.__init__(self, node, parent, link_index)

        # create block index
        self._block_index = BlockIndex()
        super_block = self._node.value
        if (super_block["Type"] != "File"):
            raise IOError("Not a file: {}".format(hash))
        self._filesize = super_block.get("filesize", -1)
        if ("Data" in super_block):
            if (self._filesize == -1):
                self._filesize = len(super_block["Data"])
            self._block_index.add_block(FileBlock(node, parent, link_index, 0, len(super_block["Data"])))
        elif ("blocksize" in super_block):
            offset = 0
            assert len(super_block["blocksize"]) == len(self._node.links)
            for i, t in enumerate(zip(self._node.links, super_block["blocksize"])):
                link, size = t
                self._block_index.add_block(FileBlock(link.follow(), self, i, offset, size))
                offset += size

        self._dirty = set()


    def _readinto(self, buf, offset, length):
        buf_offset = 0
        for chunk_offset, chunk_size, block in self._block_index.get_chunks(offset, length):
            buf[buf_offset : buf_offset + chunk_size] =\
                block._node.value["Data"][chunk_offset : chunk_offset + chunk_size]
            buf_offset += chunk_size
            block._node.flush()
        return buf_offset

    
    def _trunc(self, size):
        if (size < self._filesize):
            blocks = []
            for chunk_offset, chunk_size, block in self._get_chunks(0, size):
                assert chunk_offset == 0
                if (chunk_size == block.size):
                    blocks.append(block)
                else:
                    assert chunk_size < block.size
                    # TODO shrink block
                    self._dirty.add(block)
        elif (size > self._filesize):
            pass # TODO
                


    def open(self, mode = "r"):
        """
        Open the file.

        :param mode: The mode to open the file in. See :py:func:`io.open` for
                     documentation.
        """
        
        mode = ModeParser(mode)
        mode.parse()
        f = FileStream(self, mode)
        #f = io.BufferedRandom(f)
        if (mode.text):
            f = io.TextIOWrapper(f)
        return f



class Directory(Inode):
    def __init__(self, node, parent, link_index):
        Inode.__init__(self, node, parent, link_index)

        if (node.value["Type"] != "Directory"):
            raise IOError("Not a directory")
        
        self._children = {}
        for i, link in enumerate(node.links):
            self._children[link.name] = (i, link)

        if (parent):
            name = parent._node.links[link_index].name
            self.path = "/".join((parent.path, name))
        else:
            self.path = "/ipfs/{}".format(node.hash)


    def listdir(self):
        return tuple((link.name for link in self._node.links))


    def _get_child(self, name):
        try:
            link_index, link = self._children[name]
            return link_index, link.follow()
        except KeyError:
            raise FileNotFoundError()


    def _split_path(self, path):
        if (type(path) == str):
            path = tuple(filter(None, path.split("/")))
        return path


    def _resolve_path(self, path):
        path = self._split_path(path)
        d = self
        try:
            for s in path[:-1]:
                if (s):
                    link_index, node = d._get_child(s)
                    d = Directory(node, d, link_index)
            return d, path[-1]
        except FileNotFoundError:
            raise FileNotFoundError("/".join((self.path,) + path))


    def dir(self, path, as_child = True):
        d, name = self._resolve_path(path)
        link_index, node = d._get_child(name)
        if (as_child):
            return Directory(node, d, link_index)
        else:
            return Directory(node, None, None)


    def file(self, path, as_child = True):
        d, name = self._resolve_path(path)
        link_index, node = d._get_child(name)
        if (as_child):
            return File(node, d, link_index)
        else:
            return File(node, None, None)


    def open(self, path, mode = "r"):
        return self.file(path).open(mode)


    def create_dir(self, name):
        pass


    def __repr__(self):
        return "<Directory {} @ {}>".format(self.path, self._node.hash)

        

class IpnsRoot:
    """
    An IPNS root. It automatically updates the published IPNS record when the
    underlying unixfs tree changes.

    NOTE: Currently not functional!
    """

    def __init__(self, ipns_name = None):
        """
        Create an IPNS root.

        :param ipns_name: The IPNS name
        """
        # TODO: resolve name to Node and register as observer
        if (ipns_name):
            raise NotImplementedError("This feature is not yet implemented by go-ipfs")
        self._ipns_name = ipns_name

        


class UnixFs:
    """ The pivot class of the unixfs module. """

    def __init__(self, ipfs):
        self._ipfs = ipfs
        self._dag = Merkledag(ipfs, codec = codec.PB2(UnixFsProtocol, "Data"))


    def open(self, path, mode = "r"):
        """
        Open a unixfs file.

        :param path: Name of the file. Either a plain base58 hash, an IPFS or
                     IPNS name.
        :param mode: The mode to open the file in. See :py:func:`io.open` for
                     documentation. Defaults to "r", which opens the file for
                     reading in text mode.
        """
        return self.file(path).open(mode)


    def file(self, path):
        node = self._dag[path]
        return File(node, None, None)


    def dir(self, path):
        node = self._dag[path]
        return Directory(node, None, None)



__all__ = [
    "ModeParser",
    "Inode",
    "FileBlock",
    "FileStream",
    "File",
    "Directory",
    "IpnsRoot",
    "UnixFs"
]
