#!/usr/bin/python3
import io
import sys

try:
    import termcolor
except ImportError:
    termcolor = None


class HexDump:
    """
    Utility class to test dumping on stdout

    # #todo: refactor
    """
    def __init__(self, data, **kwargs):
        self.data = bytearray(data)
        self.offset = kwargs.get('offset', 0)
        self.file = io.TextIOWrapper(sys.stdout.buffer)
        self.colored = kwargs.get('colored', False)

    def _color(self, s, c):
        return termcolor.colored(s, c) if (self.colored and termcolor) else s

    @staticmethod
    def _format_hex(x):
        return "%02x" % x

    def _format_ascii(self, x):
        x = chr(x)
        return self._color(x, "green") if (x.isprintable()) else self._color(".", "red")

    def print_line(self, off, data):
        """Wrapper writer"""
        self.file.write("|")
        self.file.write(self._color("%08x" % off, "blue"))
        a = " ".join(map(self._format_hex, data[:8]))
        b = " ".join(map(self._format_hex, data[8:]))
        self.file.write("|")
        self.file.write(a.ljust(8 * 3 - 1))
        self.file.write("  ")
        self.file.write(b.ljust(8 * 3 - 1))
        self.file.write("|")
        for b in data:
            self.file.write(self._format_ascii(b))
        self.file.write(" " * (16 - len(data)))
        self.file.write("|\n")

    def print_hexdump(self):
        """Raw writing on a TexrIOWrapper"""
        for i in range(0, len(self.data), 16):
            self.print_line(self.offset + i, self.data[i: i + 16])


def print_data(data, **kwargs):
    """Return byte object"""
    o = HexDump(data, **kwargs)
    return o.data


if __name__ == '__main__':
    data = b'\x08\x01'
    new = HexDump(data)
    new.print_hexdump()

