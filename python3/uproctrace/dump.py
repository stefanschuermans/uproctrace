import uproctrace.uproctrace_pb2 as pb2
import struct


def dump_event(f, out):
    """
    Read the first event from f and dump it to out.
    Return True if an event could be found and dumped, False otherwise.
    """
    # skip till after magic
    magic = f.read(4)
    while magic != b'upt0':
        if len(magic) < 4:
            return False  # EOF
        magic = magic[1:] + f.read(1)  # search for magic byte for byte
    # read size of next event (32 bit network byte order)
    size = f.read(4)
    if len(size) < 4:
        return False  # EOF
    size = struct.unpack('!L', size)[0]
    # read event data
    data = f.read(size)
    if len(data) < size:
        return False  # EOF
    # unpack event
    event = pb2.event.FromString(data)
    # dump event
    print('event {', file=out)
    for line in repr(event).split('\n'):
        if line != '':
            print('  ' + line, file=out)
    print('}', file=out)
    return True
