"""
Command line interface of UProcTrace: "upt-tool".
"""

import argparse
import sys
import uproctrace.dump
import uproctrace.processes


def dump(args):
    """
    Dump all events in trace file to standard output.
    """
    with open(args.trace, 'rb') as proto_file:
        while uproctrace.dump.dump_event(proto_file, sys.stdout):
            pass


def parse(args):
    """
    Parse all events in trace file.
    """
    with open(args.trace, 'rb') as proto_file:
        uproctrace.processes.Processes(proto_file)


def parse_args():
    """
    Parse command line arguments.
    """
    # set up main parser
    parser = argparse.ArgumentParser(description='uproctrace tool')
    parser.add_argument('trace', help='trace file')
    subparsers = parser.add_subparsers()
    # dump
    dump_parser = subparsers.add_parser('dump')
    dump_parser.set_defaults(func=dump)
    # parse
    parse_parser = subparsers.add_parser('parse')
    parse_parser.set_defaults(func=parse)
    # parse
    args = parser.parse_args()
    if not hasattr(args, 'func'):
        print('error: no sub-command specified', file=sys.stderr)
        sys.exit(3)
    return args


def main():
    """
    upt-tool main function.
    Parse command line arguments and execute selected action.
    """
    args = parse_args()
    args.func(args)
