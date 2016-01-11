from . import codec


class ConfigApi:
    def __init__(self, root):
        self._rpc = root.config


    def show(self):
        return self._rpc.show.with_outputenc(codec.JSON)()


