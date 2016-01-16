from .proto.unixfs import UnixFsProtocol
from .merkledag import Merkledag
from . import codec
import io


class ModeParser:
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
    def __init__(self, node, parent, link_index):
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


    def observe(self, observer):
        self._observers.append(observer)



class FileBlock(Inode):
    def __init__(self, node, parent, link_index, offset, size):
        Inode.__init__(self, node, parent, link_index)
        self.offset = offset
        self.size = size

    def __repr__(self):
        return "<FileBlock {} [{:d} : {:d}]>".format(self._node.hash, self.offset, self.offset + self.size)



class FileStream(io.RawIOBase):
    def __init__(self, file, mode):
        self.hash = hash
        self._file = file
        self._mode = mode
        
        self._readable = mode.reading
        self._writable = mode.writing

        # TODO: Use size from underlying file
        self._size = 0 if (mode.trunc) else self._file._filesize
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
        return self._file._readinto(buf, self._pos, len(buf))

    def readall(self):
        return self.read(-1)

    def read(self, n = -1):
        if (n == -1):
            n = self._size
        buf = bytearray(n)
        self.readinto(buf)
        return bytes(buf)


    def write(self):
        raise NotImplementedError()


    def seek(self, offset, whence):
        if (whence == io.SEEK_SET):
            self._pos = offset
        elif (whence == io.SEEK_CUR):
            self._pos += offset
        elif (whence == io.SEEK_END):
            self._pos = self._file._size + offset
        return self._pos


    def tell(self):
        return self._pos


    def truncate(self, size = None):
        if (size == None):
            size = self._pos
        raise NotImplementedError()




class File(Inode):
    def __init__(self, node, parent, link_index):
        Inode.__init__(self, node, parent, link_index)

        # create block index
        # TODO: Use an AVL tree for this
        self._blocks = []
        super_block = self._node.value
        if (super_block["Type"] != "File"):
            raise IOError("Not a file: {}".format(hash))
        self._filesize = super_block.get("filesize", -1)
        if ("Data" in super_block):
            if (self._filesize == -1):
                self._filesize = len(super_block["Data"])
            self._blocks.append(FileBlock(node, parent, link_index, 0, len(super_block["Data"])))
        elif ("blocksize" in super_block):
            offset = 0
            assert len(super_block["blocksize"]) == len(self._node.links)
            for i, t in enumerate(zip(self._node.links, super_block["blocksize"])):
                link, size = t
                self._blocks.append(FileBlock(link.follow(), self, i, offset, size))
                offset += size

    def _get_chunks(self, offset, length):
        chunks = []
        for block in self._blocks:
            if (block.offset <= offset and offset < block.offset + block.size):
                chunk_offset = offset - block.offset
                chunk_size = min((length, block.size - chunk_offset))
                chunks.append((chunk_offset, chunk_size, block))
                offset += chunk_size
                length -= chunk_size
            assert length >= 0
            if (length == 0):
                break
        return chunks

    def _readinto(self, buf, offset, length):
        buf_offset = 0
        for chunk_offset, chunk_size, block in self._get_chunks(offset, length):
            buf[buf_offset : buf_offset + chunk_size] =\
                block._node.value["Data"][chunk_offset : chunk_offset + chunk_size]
            buf_offset += chunk_size
            block._node.flush()
        return buf_offset

    def open(self, mode = "r"):
        mode = ModeParser(mode)
        mode.parse()
        f = FileStream(self, mode)
        #f = io.BufferedRandom(f)
        if (mode.text):
            f = io.TextIOWrapper(f)
        return f

        

class IpnsRoot():
    def __init__(self, ipfs_name = None):
        # TODO: resolve name to Node and register as observer
        if (ipns_name):
            raise NotImplementedError("This feature is not yet implemented by go-ipfs")
        self._ipns_name = ipns_name

        


class UnixFs:
    def __init__(self, ipfs):
        self._ipfs = ipfs
        self._dag = Merkledag(ipfs, codec = codec.PB2(UnixFsProtocol, "Data"))

    def open(self, name, mode = "r"):
        node = self._dag[name]
        file = File(node, None, None)
        return file.open(mode)
