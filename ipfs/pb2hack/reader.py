from io import BytesIO

from .error import Pb2ReaderException


class Pb2WireReader:
    def __init__(self, f):
        self.f = f

        self._read_wire_type = {
            0: self.read_varint,
            1: self.read_fixed64,
            2: self.read_bytes,
            5: self.read_fixed32
        }


    def read(self):
        field_number, wire_type = self.read_key()
        wire_val = self.read_wire_type(wire_type)
        return field_number, wire_type, wire_val


    def read_key(self):
        vi = self.read_varint()
        return (vi >> 3), (vi & 7)


    def read_wire_type(self, wire_type):
        return self._read_wire_type[wire_type]()


    def read_varint(self):
        x = 0
        i = 0
        while (True):
            b = self.f.read(1)
            if (not b):
                raise EOFError
            b = b[0]
            x |= (b & 0x7F) << i
            if (b & 0x80 == 0):
                return x
            i += 7


    def read_fixed32(self):
        return int.from_bytes(self.f.read(4), "little")


    def read_fixed64(self):
        return int.from_bytes(self.f.read(8), "little")


    def read_bytes(self):
        n = self.read_varint()
        return self.f.read(n)



class Pb2Reader:
    def __init__(self, wire, protocol, message):
        self.wire = wire
        self.protocol = protocol
        self.message = message

        self._read_field_type = {
            #"double": self.interpret_double,
            #"float": self.interpret_float,
            #"int32": self.interpret_int,
            #"int64": self.interpret_int,
            "uint32": self.read_asis,
            "uint64": self.read_asis,
            #"sint32": self.interpret_sint,
            #"sint64": self.interpret_sint,
            "bool": self.read_bool,
            "string": self.read_string,
            "bytes": self.read_asis
            # TODO
        }


    def read(self):
        obj = {}

        try:
            while (True):
                field_number, wire_type, wire_val = self.wire.read()
                
                # parse value according to protocol
                try:
                    field = self.message.fields_by_number[field_number]
                except KeyError:
                    continue

                val = self.read_field(field, wire_val)
                                
                # add value to object
                if (field.label == "repeated"):
                    try:
                        l = obj[field.name]
                    except KeyError:
                        obj[field.name] = l = []
                    l.append(val)
                else:
                    obj[field.name] = val
        except EOFError:
            pass

        # check if all required fields are present and put empty lists for
        # non-present repeated fields.
        for field in self.message.fields_by_name.values():
            if (field.label not in obj):
                if (field.label == "required"):
                    raise Pb2ReaderException("Required field {} not present in {}".format(field.name, self.message.name))

        return obj


    def read_field(self, field, wire_val):
        reader = self._read_field_type.get(field.type)
        if (reader):
            val = reader(wire_val)
        else:
            message = self.protocol.messages.get(field.type)
            if (message):
                val = self.read_message(wire_val, message)
            else:
                enum = self.protocol.messages.get(field.type)
                if (enum):
                    val = self.read_enum(wire_val, enum)
                else:
                    raise Pb2ReaderException("Unknown field type {}".format(field.type))
        if (field.filter):
            val = field.filter[0](val)
        return val
                


    def read_asis(self, wire_val):
        return wire_val


    def read_bool(self, wire_val):
        assert type(wire_val) == int
        return bool(wire_val)


    def read_string(self, wire_val):
        assert type(wire_val) == bytes
        return wire_val.decode()


    def read_message(self, wire_val, message):
        wire = Pb2WireReader(BytesIO(wire_val))
        reader = Pb2Reader(wire, self.protocol, message)
        return reader.read()


    def read_enum(self, wire_val, enum):
        try:
            return enum.defs[wire_val]
        except KeyError:
            raise Pb2ReaderException("Value {:d} doesn't match any enum value in {}".format(wire_val, enum.name))



__all__ = [
    "Pb2WireReader",
    "Pb2Reader"
]
