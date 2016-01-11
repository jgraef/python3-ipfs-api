from . import codec


class BlockApi:
    def __init__(self, root):
        self._rpc = root.block


    def stat(self, key):
        return self._rpc.stat[key].with_outputenc(codec.JSON)()


    def get(self, key):
        return self._rpc.get[key]()


    def put(self, f):
        return self._rpc.put.with_outputenc(codec.JSON)(_in = f)
