"""
This modules handles various encodings formats used by the IPFS HTTP API.
"""

import json
import pickle
from pb2nano.reader import Pb2WireReader, Pb2Reader
from pb2nano.writer import Pb2WireWriter, Pb2Writer
import codecs
from io import BytesIO


class Codec:
    """
    An abstract encoding/decoding mechanism.

    It exposes the same methods as json, pickle, etc. Namely dump, dumps,
    load and loads.

    Implement dump and load and this class will handle dumps and loads for you.
    """
    
    name = None
    """
    The name of that encoding. This will be sent to the HTTP API to select the
    input or output encoding.
    """
        

    def dump(self, obj, f):
        """
        Dump a object to a file stream. The file stream is expected to be
        binary.

        :param obj: The object to dump
        :param f:   The stream to dump to

        Override this method to implement a codec.
        """
        raise NotImplementedError()


    def load(self, f):
        """
        Load a object from a file stream. The file stream is binary.

        :param f: The stream to load from
        :return:  The object loaded from the stream

        Override this method to implement a codec.
        """
        raise NotImplementedError()


    def dumps(self, obj):
        """
        Dump an object as bytes object.

        :param:  The object to dump
        :return: The bytes that represent the object in binary form
        """
        
        f = BytesIO()
        self.dump(obj, f)
        data = f.getvalue()
        f.close()
        return data


    def loads(self, data):
        """
        Load an object from an bytes object.

        :param data: The binary data representing an object
        :return:     The object represented by the data
        """
        
        f = BytesIO(data)
        obj = self.load(f)
        f.close()
        return obj


    def __str__(self):
        return self.name



class Json(Codec):
    """ Encoding and decoding of JSON. """

    name = "json"
    
    def load(self, f):
        reader = codecs.getreader("utf-8")
        f_txt = reader(f)
        return json.load(f_txt)

    def dump(self, obj, f):
        writer = codecs.getwriter("utf-8")
        f_bytes = writer(f)
        json.dump(obj, f_bytes)


class JsonVector(Codec):
    """ Encoding and decoding of a stream of lines that contain JSON. """

    name = "json"

    def load(self, f):
        reader = codecs.getreader("utf-8")
        f_txt = reader(f)

        for l in f_txt:
            yield json.loads(l)

    def dump(self, obj, f):
        for x in obj:
            json.dump(x, f)
            f.write("\n")


class Protobuf2(Codec):
    """ Encoding and decoding of protobuf2 encoded messages. """
    
    name = "protobuf"
    
    def __init__(self, protocol, message):
        """
        Create an instance of a Protobuf2 encoding.

        :param protocol: The Protobuf protocol to be used
        :param message:  The type in which the top-level message is expected to
                         be.
        """

        self.protocol = protocol
        if (type(message) == str):
            message = self.protocol.messages[message]
        self.message = message


    def load(self, f):
        wire_reader = Pb2WireReader(f)
        reader = Pb2Reader(wire_reader, self.protocol, self.message)
        return reader.read()


    def dump(self, obj, f):
        wire_writer = Pb2WireWriter(f)
        writer = Pb2Writer(wire_writer, self.protocol, self.message)
        writer.write(obj)


    def __str__(self):
        return "{}/{}".format(self.name, self.message.name)


class Pickle(Codec):
    """ Encoding and decoding with pickle """

    name = "pickle"

    def load(self, f):
        return pickle.load(f)

    def dump(self, obj, f):
        pickle.dump(obj, f)



JSON = Json()
""" The singleton instance of the JSON encoding. """

JSONV = JsonVector()
""" The singleton instance of the JSON vector encoding. """

PICKLE = Pickle()
""" The singleton instance of the pickle encoding. """

def PB2(protocol, message):
    """
    Return a Protobuf2 instance depending on the protocol and message type.
    """
    return Protobuf2(protocol, message)
        


__all__ = [
    "Codec",
    "Json",
    "JsonVector",
    "Protobuf2",
    "JSON",
    "JSONV",
    "PB2"
]
