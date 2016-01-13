
class Pb2Exception(Exception):
    pass

class Pb2ProtocolException(Pb2Exception):
    pass

class Pb2ReaderException(Pb2Exception):
    pass

class Pb2WriterException(Pb2Exception):
    pass


__all__ = [
    "Pb2Exception",
    "Pb2ProtocolException",
    "Pb2ReaderException",
    "Pb2WriterException"
]
