#!/usr/bin/python3

import sys

try:
    import termcolor
except ImportError:
    termcolor = None
    



def print_hexdump(data, offset = 0, file = sys.stdout, colored = False):
    def color(s, c):
        return termcolor.colored(s, c) if (colored and termcolor) else s

    def format_hex(x):
        return "%02x" % x

    def format_ascii(x):
        x = chr(x)
        return color(x, "green") if (x.isprintable()) else color(".", "red")
    
    def print_line(off, data):
        file.write("|")
        file.write(color("%08x" % off, "blue"))
        a = " ".join(map(format_hex, data[:8]))
        b = " ".join(map(format_hex, data[8:]))
        file.write("|")
        file.write(a.ljust(8 * 3 - 1))
        file.write("  ")
        file.write(b.ljust(8 * 3 - 1))
        file.write("|")
        for b in data:
            file.write(format_ascii(b))
        file.write(" " * (16 - len(data)))
        file.write("|\n")

    for i in range(0, len(data), 16):
        print_line(offset + i, data[i : i + 16])
    


if (__name__ == "__main__"):
    import io
    
    f = io.open(0, mode="rb", closefd=False)
    off = 0
    while (True):
        data = f.read(16)
        if (not data):
            break
        print_hexdump(data, offset = off, colored = True)
        off += 16
    f.close()
