from . import codec


class FileApi:
    def __init__(self, root):
        self._rpc = root


    def ls(self, path):
        return self._rpc.file.ls[path].with_outputenc(codec.JSON)()


    def add(self, f):
        return self._rpc.add.with_outputenc(codec.JSON)(_in = f)


    def cat(self, path):
        return self._rpc.cat[path]()


__all__ = ["FileApi"]
