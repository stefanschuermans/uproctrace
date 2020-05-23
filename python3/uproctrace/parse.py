import uproctrace.uproctrace_pb2 as pb2
import struct


def read_event(f):
    """
    Read the first event from f and return it.
    Return None if no event could be found.
    """
    # skip till after magic
    magic = f.read(4)
    while magic != b'upt0':
        if len(magic) < 4:
            return None  # EOF
        magic = magic[1:] + f.read(1)  # search for magic byte for byte
    # read size of next event (32 bit network byte order)
    size = f.read(4)
    if len(size) < 4:
        return None  # EOF
    size = struct.unpack('!L', size)[0]
    # read event data
    data = f.read(size)
    if len(data) < size:
        return None  # EOF
    # unpack event
    event = pb2.event.FromString(data)
    return event
