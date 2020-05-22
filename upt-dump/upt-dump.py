#! /usr/bin/env python3

import argparse
import sys
import uproctrace.dump


def parse_args():
    parser = argparse.ArgumentParser(description='dump uproctrace trace')
    parser.add_argument('trace', help='trace file')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    with open(args.trace, 'rb') as f:
        while uproctrace.dump.dump_event(f, sys.stdout):
            pass


if __name__ == '__main__':
    main()
