#!/usr/bin/env python3
"""Remove the host-only PT_GNU_STACK header from an Orbis module ELF."""
import struct, sys

path = sys.argv[1]
data = bytearray(open(path, "rb").read())
if data[:4] != b"\x7fELF" or data[4] != 2 or data[5] != 1:
    raise SystemExit("expected ELF64 little-endian")
phoff = struct.unpack_from("<Q", data, 32)[0]
phentsz = struct.unpack_from("<H", data, 54)[0]
phnum = struct.unpack_from("<H", data, 56)[0]
for i in range(phnum):
    off = phoff + i * phentsz
    ptype = struct.unpack_from("<I", data, off)[0]
    if ptype == 0x6474E551:  # PT_GNU_STACK
        struct.pack_into("<I", data, off, 0)  # PT_NULL
        struct.pack_into("<H", data, 56, phnum - 1)
open(path, "wb").write(data)
