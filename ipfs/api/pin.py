from . import codec


class PinApi:
    def __init__(self, root):
        self._rpc = root.pin


    def add(self, ref):
        return self._rpc.add.with_outputenc(codec.JSON)(ref)


    def rm(self, ref):
        return self._rpc.rm.with_outputenc(codec.JSON)(ref)


    def ls(self):
        return self._rpc.ls.with_outputenc(codec.JSON)()


__all__ = ["PinApi"]
