"""
This module handles the utilities to read and write to the IPFS node's config.
"""

from .. import codec


class ConfigApi:
    """
    Get and set IPFS config values
    """

    def __init__(self, root):
        self._rpc = root.config


    def show(self):
        """
        Return the current configuration

        :return: The current configuration as dict.
        """
        return self._rpc.show.with_outputenc(codec.JSON)()


__all__ = ["ConfigApi"]
