import json
from ..pb2hack.reader import Pb2WireReader, Pb2Reader
from ..pb2hack.writer import Pb2WireWriter, Pb2Writer
import codecs


class Codec:
    name = None

    def dump(self, obj, f):
        raise NotImplementedError()


    def load(self, f):
        raise NotImplementedError()


    def dumps(self, obj):
        f = BytesIO()
        self.dump(obj, f)
        data = f.getvalue()
        f.close()
        return data


    def loads(self, data):
        f = BytesIO(data)
        obj = self.load(f)
        f.close()
        return obj


    def __str__(self):
        return self.name



class Json(Codec):
    name = "json"
    
    def load(self, f):
        reader = codecs.getreader("utf-8")
        f_txt = reader(f)
        return json.load(f_txt)

    def dump(self, obj, f):
        writer = codecs.getwriter("utf-8")
        return writer(json.dump(obj, f))


class JsonVector(Codec):
    name = "json"

    def load(self, f):
        reader = codecs.getreader("utf-8")
        f_txt = reader(f)

        for l in f_txt:
            yield json.loads(l)


class Protobuf2(Codec):
    name = "protobuf"
    
    def __init__(self, protocol, message):
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



JSON = Json()
JSONV = JsonVector()

def PB2(protocol, message):
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
