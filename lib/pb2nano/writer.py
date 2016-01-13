from io import BytesIO

from .error import Pb2WriterException


class Pb2WireWriter:
    def __init__(self, f):
        self.f = f


    def write_key(self, field_number, wire_type):
        self.write_varint((field_number << 3) | wire_type)


    def write_varint(self, vi):
        while (vi >= 0x80):
            self.f.write(bytes([0x80 | (vi & 0x7F)]))
            vi >>= 7
        self.f.write(bytes([vi]))


    def write_fixed32(self, i):
        self.f.write(i.to_bytes(4, "little"))


    def write_fixed64(self, i):
        self.f.write(i.to_bytes(8, "little"))


    def write_bytes(self, b):
        self.write_varint(len(b))
        self.f.write(b)




class Pb2Writer:
    def __init__(self, wire, protocol, message):
        self.wire = wire
        self.protocol = protocol
        self.message = message

        self._write_field_type = {
            "bool": self.write_bool,
            "string": self.write_string,
            "bytes": self.write_bytes,
            "uint32": self.write_uint,
            "uint64": self.write_uint,
            # TODO
        }


    def write(self, obj):
        # check if all required fields are there
        for field_name, field in self.message.fields_by_name.items():
            if (field.label == "required" and field.name not in obj):
                raise Pb2WriterException("Required field {} not found".format(field.name))

        # write all fields
        for field_name, val in obj.items():
            try:
                field = self.message.fields_by_name[field_name]
            except KeyError:
                raise Pb2WriterException("Unknown field name {}".format(field_name))
            if (field.label == "repeated"):
                for val2 in val:
                    self.write_field(field, val2)
            else:
                self.write_field(field, val)


    def write_field(self, field, val):
        if (field.filter):
            val = field.filter[1](val)
        writer = self._write_field_type.get(field.type)
        if (writer):
            writer(field.number, val)
        else:
            message = self.protocol.messages.get(field.type)
            if (message):
                self.write_field_message(field.number, val, message)
            else:
                enum = self.protocol.enums.get(field.type)
                if (enum):
                    self.write_field_enum(field.number, val, enum)
                else:
                    raise Pb2WriterException("Unknown field type {}".format(field.type))


    def write_bool(self, field_number, val):
        self.wire.write_key(field_number, 0)
        self.wire.write_varint(int(val))


    def write_bytes(self, field_number, val):
        self.wire.write_key(field_number, 2)
        self.wire.write_bytes(val)


    def write_string(self, field_number, val):
        self.wire.write_key(field_number, 2)
        self.wire.write_bytes(val.encode())


    def write_uint(self, field_number, val):
        self.wire.write_key(field_number, 0)
        self.wire.write_varint(val)


    def write_field_message(self, field_number, val, message):
        self.wire.write_key(field_number, 2)

        buf = BytesIO()
        wire = Pb2WireWriter(buf)
        writer = Pb2Writer(wire, self.protocol, message)
        writer.write(val)

        self.wire.write_bytes(buf.getvalue())


    def write_field_enum(self, field_number, val, enum):
        try:
            wire_val = enum.defs_by_name[val]
        except KeyError:
            raise Pb2WriterException("{} doesn't match any enum constant in {}".format(val, enum.name))
        self.wire.write_key(field_number, 0)
        self.wire.write_varint(wire_val)


__all__ = [
    "Pb2WireWriter",
    "Pb2Writer"
]
