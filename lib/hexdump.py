#!/usr/bin/python3
import io
import sys

try:
    import termcolor
except ImportError:
    termcolor = None


class HexDump:
    """
    Utility class to dump an object

    # #todo: refactor
    """
    def __init__(self, data, **kwargs):
        self.data = data
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


def print_hexdump(data, **kwargs):
    o = HexDump(data, **kwargs)
    for i in range(0, len(o.data), 16):
        o.print_line(o.offset + i, o.data[i: i + 16])


if __name__ == "__main__":

    # #todo; use a context manager to open file ('with' statement)
    f = io.open(0, mode="rb", closefd=False)
    off = 0
    while (True):
        data = f.read(16)
        if (not data):
            break
        print(print_hexdump(data, offset=off, colored=True))
        off += 16
    f.close()
