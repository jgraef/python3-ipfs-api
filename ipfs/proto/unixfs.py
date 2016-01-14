from pb2nano.protocol import Pb2Enum, Pb2Message, Pb2Protocol


DataType = Pb2Enum("DataType") \
           .define("Raw", 0) \
           .define("Directory", 1) \
           .define("File", 2) \
           .define("Metadata", 3) \
           .define("Symlink", 4)

Data = Pb2Message("Data")\
       .field("required", "DataType", "Type", 1) \
       .field("optional", "bytes", "Data", 2) \
       .field("optional", "uint64", "filesize", 3) \
       .field("repeated", "uint64", "blocksize", 4)

Metadata = Pb2Message("Metadata")\
           .field("required", "string", "MimeType", 1)


UnixFsProtocol = Pb2Protocol()\
                 .enum(DataType)\
                 .message(Data)\
                 .message(Metadata)


__all__ = [
    "DataType",
    "Data",
    "Metadata"
]
