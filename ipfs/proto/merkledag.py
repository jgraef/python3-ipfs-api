from pb2nano.protocol import Pb2Message, Pb2Protocol
from base58 import b58encode, b58decode


PBLink = Pb2Message("PBLink")\
         .field("optional", "bytes", "Hash", 1, (b58encode, b58decode))\
         .field("optional", "string", "Name", 2)\
         .field("optional", "uint64", "Size", 3)

PBNode = Pb2Message("PBNode")\
         .field("repeated", "PBLink", "Links", 2)\
         .field("optional", "bytes", "Data", 1)

PBMerkleDag = Pb2Protocol()\
              .message(PBLink)\
              .message(PBNode)



__all__ = [
    "PBLink",
    "PBNode",
    "PBMerkleDag"
]
