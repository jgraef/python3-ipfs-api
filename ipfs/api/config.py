from . import codec


class ConfigApi:
    """
    #todo: add docstring
    """
    def __init__(self, root):
        self._rpc = root.config


    def show(self):
        """

        :return:
        """
        return self._rpc.show.with_outputenc(codec.JSON)()


