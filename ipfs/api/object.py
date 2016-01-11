from .codec import JSON, PB2
from ..proto.merkledag import PBMerkleDag


PBNode = PB2(PBMerkleDag, "PBNode")


class ObjectPatchApi:
    def __init__(self, rpc, key):
        self.key = key
        self._rpc = rpc.patch[key]


    def add_link(self, name, ref):
        pass


    def rm_link(self, name):
        pass


    def set_data(self, f):
        pass


    def append_data(self, f):
        pass



class ObjectApi:
    def __init__(self, root):
        self._rpc = root.object


    def data(self, key):
        return self._rpc.data[key]()


    def links(self, key):
        return self._rpc.links[key].with_outputenc(JSON)()


    def get(self, key):
        return self._rpc.get[key].with_outputenc(PBNode)()


    def put(self, node):
        return self._rpc.put.with_inputenc(PBNode).with_outputenc(JSON)(_in = node)


    def stat(self, key):
        return self._rpc.stat[key].with_outputenc(JSON)()


    def new(self, template = None):
        args = (template,) if template else ()
        return self._rpc.new.with_outputenc(JSON)(*args)
    
    def patch(self, key):
        return ObjectPatchApi(self._rpc, key)
