#! /usr/bin/env python3

import argparse
import uproctrace_pb2
import struct


def parse_args():
    parser = argparse.ArgumentParser(description='dump uproctrace trace')
    parser.add_argument('trace', help='trace file')
    args = parser.parse_args()
    return args


def dump_event(f):
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
    event = uproctrace_pb2.event.FromString(data)
    # dump event
    print('event {')
    for line in repr(event).split('\n'):
        if line != '':
            print('  ' + line)
    print('}')
    return True


def main():
    args = parse_args()
    with open(args.trace, 'rb') as f:
        while dump_event(f):
            pass


if __name__ == '__main__':
    main()
