from . import codec


class NameApi:
    def __init__(self, root):
        self._rpc = root.name


    def publish(self, ref):
        return self._rpc.publish.with_outputenc(codec.JSON)(ref)


    def resolve(self, name = None, recursive = True, nocache = False):
        args = (name,) if name else ()
        return self._rpc.resolve.with_outputenc(codec.JSON)(*args, recursive = recursive, nocache = nocache)
