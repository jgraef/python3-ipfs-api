from collections import namedtuple

from .error import Pb2ProtocolException



class Pb2Enum:
    def __init__(self, name):
        self.name = name
        self.defs_by_number = {}
        self.defs_by_name = {}


    def define(self, name, number):
        if (name in self.defs_by_name):
            raise Pb2ProtocolException("Enum field with name '{}' already defined in {}".format(name, self.name))
        if (number in self.defs_by_number):
            raise Pb2ProtocolException("Enum field with number '{}' already defined in {}".format(number, self.name))

        self.defs_by_number[number] = name
        self.defs_by_name[name] = number
        return self


    def __repr__(self):
        str_defs = ["{} = {:d}".format(n, v) for n, v in self.defs_by_name.items()]
        return "enum {} {{\n{}}}".format(self.name, "\n".join(str_defs))



class Pb2Message:
    Field = namedtuple("Field", ["label", "type", "name", "number", "filter"])


    def __init__(self, name):
        self.name = name
        self.fields_by_number = {}
        self.fields_by_name = {}


    def field(self, label, type, name, number, filter = None):
        if (name in self.fields_by_name):
            raise Pb2ProtocolException("Message field with name '{}' already defined in {}".format(name, self.name))
        if (number in self.fields_by_number):
            raise Pb2ProtocolException("Message field with number {:d} already defined in {}".format(number, self.name))

        field = Pb2Message.Field(label, type, name, number, filter)
        self.fields_by_number[number] = field
        self.fields_by_name[name] = field
        return self


    def __repr__(self):
        str_defs = ["{}{} {} {} = {:d}".format(f.label, " " if f.label != None else "", f.type, f.name, f.number) for f in self.fields_by_name.values()]
        return "message {} {{\n{}}}".format(self.name, "\n".join(str_defs))



class Pb2Protocol:
    def __init__(self):
        self.enums = {}
        self.messages = {}


    def check_double_def(self, name):
        if (name in self.messages):
            raise Pb2ProtocolException("Message type {} already defined".format(message.name))
        if (name in self.enums):
            raise Pb2ProtocolException("Enum type {} already defined".format(message.name))


    def enum(self, enum):
        self.check_double_def(enum.name)
        self.enums[enum.name] = enum
        return self


    def message(self, message):
        self.check_double_def(message.name)
        self.messages[message.name] = message
        return self


    def join(self, other):
        assert isinstance(other, Pb2Protocol)
        proto = Pb2Protocol()
        for enum in self.enums:
            proto.enum(enum)
        for message in self.messages:
            proto.message(message)
        for enum in other.enums:
            proto.enum(enum)
        for message in other.messages:
            proto.message(message)
        return proto


    def __add__(self, other):
        return self.join(other)


__all__ = [
    "Pb2Enum",
    "Pb2Message",
    "Pb2Protocol"
]
