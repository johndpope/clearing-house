import struct


# 60002
def netaddr(ipaddr, port):
    services = 1
    return (struct.pack('<Q12s', services, '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff') +
                       struct.pack('>4sH', ipaddr, port))


def safe_int(v: str):
    return int(v) if v else v


def varint(x: int):
    if x < 0xfd:
        return bytes([x])
    elif x < 0xffff:
        return bytes([253]) + x.to_bytes(2, 'little')
    elif x < 0xffffffff:
        return bytes([254]) + x.to_bytes(4, 'little')
    else:
        return bytes([255]) + x.to_bytes(8, 'little')


# Takes and returns byte string value, not hex string
def varstr(s: str):
    return varint(len(s)) + s


# takes 26 byte input, returns string
def process_netaddr(payload):
    assert(len(payload) >= 26)
    return '%d.%d.%d.%d:%d' % (payload[20], payload[21],
                               payload[22], payload[23],
                               struct.unpack('!H', payload[24:26])[0])


# return value, len
def process_varint(payload):
    n0 = payload[0]
    if n0 < 0xfd:
        return [n0, 1]
    elif n0 == 0xfd:
        return [struct.unpack('<H', payload[1:3])[0], 3]
    elif n0 == 0xfe:
        return [struct.unpack('<L', payload[1:5])[0], 5]
    else:
        return [struct.unpack('<Q', payload[1:5])[0], 7]


# return value, len
def process_varstr(payload):
    n, length = process_varint(payload)
    return [payload[length:length+n], length + n]
