""" X85ML is a modified Ascii85 encoding

Using z85mq and changing <>&  so SGML and XML won't require escaping.

Inspiration from PyZMQ, BSD Licence

Data length to encode must be a multiple of 4, padding with non significant char of #0 has to be added if needed.

"""

import sys
import struct

import array

#X85CHARS = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!;*?_|~()[]{}@%$#"
SYMBOLS = b".-:+=^!;*?_|~()[]{}@%$#"
EXCLUDED = b":+=^;*?|~()[]{}%#" # to only allowed .-!_@$
# To do
# find in excluded index of symbole
# substract 37 used the CHAR of that index to replace at original index the symbole
# remap X85CHARS

ArrayOfSYMBOLS = [".", "-", ":", "+", "=", "^", "!", ";", "*", "?", "_", "|", "~", "(", ")", "[", "]", "{", "}", "@", "%", "$", "#"]
ArrayOfExclusion = [":", "+", "=", "^", ";", "*", "?", "|", "~", "(", ")", "[", "]", "{", "}", "%", "#"]

bX85CHARS = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!;*?_|~()[]{}@%$#"

if not ArrayOfExclusion:
    X85CHARS = bX85CHARS
else:
    """ Convert from bytes Array to list """
    tuple(enumerate(bX85CHARS))
    NX85CHARS = []
    for index, value in enumerate(bX85CHARS):
        NX85CHARS.insert(index,value)

    """ Remap excluded symboles to printable characters """
    tuple(enumerate(ArrayOfSYMBOLS))
    for item in ArrayOfExclusion:
        for index, value in enumerate(ArrayOfSYMBOLS):
            if value == item:
                NX85CHARS[index + 62] = NX85CHARS[index + 24]
    #           print(f'{index}: {value}',end=' ')
    #           print(f'{index}: {NX85CHARS[index + 62]}', end=' ')
    # print()

    """ map back from list to bytes Array"""
    array.array('B', NX85CHARS).tostring()
    X85CHARS = NX85CHARS

tuple(enumerate(X85CHARS))
for index, value in enumerate(X85CHARS):
    print(f'{index}: {value}', end=' ')


X85MAP = dict([(c, idx) for idx, c in enumerate(X85CHARS)])

_85s = [ 85**i for i in range(5) ][::-1]

def encode(rawbytes):
    """encode raw bytes into X85"""
    # Accepts only byte arrays bounded to 4 bytes
    if len(rawbytes) % 4:
        raise ValueError("length must be multiple of 4, not %i" % len(rawbytes))

    nvalues = len(rawbytes) / 4

    values = struct.unpack('>%dI' % nvalues, rawbytes)
    encoded = []
    for v in values:
        for offset in _85s:
            encoded.append(X85CHARS[(v // offset) % 85])

    return bytes(encoded)

def decode(x85bytes):
    """decode X85 bytes to raw bytes, accepts ASCII string"""
    if isinstance(x85bytes, str):
        try:
            x85bytes = x85bytes.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('string argument should contain only ASCII characters')

    if len(x85bytes) % 5:
        raise ValueError("X85 length must be multiple of 5, not %i" % len(x85bytes))

    nvalues = len(x85bytes) / 5
    values = []
    for i in range(0, len(x85bytes), 5):
        value = 0
        for j, offset in enumerate(_85s):
            value += X85MAP[x85bytes[i+j]] * offset
        values.append(value)
    return struct.pack('>%dI' % nvalues, *values)
