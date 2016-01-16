from ipfs.api import IpfsApi


# connect to the IPFS daemon
ipfs = IpfsApi()


# Read a file
# Many commands work on byte streams instead of bytes objects
f = ipfs.file.cat("QmPZ9gcCEpqKTo6aq61g2nXGUhM4iCL3ewB6LDXZCtioEB")
data = f.read()


# Since it's bytes but we want to print it as text, we need to decode it
text = data.decode()


# And print it
print(text)


# Don't forget to close the stream
f.close()
