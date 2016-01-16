from ipfs.api import IpfsApi
from ipfs.unixfs import UnixFs


fs = UnixFs(IpfsApi())
with fs.open("QmPZ9gcCEpqKTo6aq61g2nXGUhM4iCL3ewB6LDXZCtioEB", "r") as f:
    for line in f.readlines():
        print(line, end = "")
