"""
Command line interface of UProcTrace: "upt-tool".
"""

import argparse
import shlex
import sys


def dump(args):
    """
    Dump all events in trace file to standard output.
    """
    import uproctrace.dump
    with open(args.trace, 'rb') as proto_file:
        while uproctrace.dump.dump_event(proto_file, sys.stdout):
            pass


def gui(args):
    """
    Run the graphical user interface.
    """
    import uproctrace.gui
    uproctrace.gui.run(args.trace)


def pstree(args):
    """
    Print process tree.
    """
    import uproctrace.processes
    with open(args.trace, 'rb') as proto_file:
        processes = uproctrace.processes.Processes(proto_file)
    # tree output (iterative)
    to_be_output = [processes.toplevel]
    while to_be_output:
        procs = to_be_output[-1]
        if not procs:
            del to_be_output[-1]
            continue
        indent = '  ' * (len(to_be_output) - 1)
        proc = procs[0]
        del procs[0]
        cmdline = proc.cmdline
        if cmdline is None:
            cmdline_str = '???'
        else:
            cmdline_str = ' '.join([shlex.quote(s) for s in cmdline])
        print(indent + cmdline_str)
        to_be_output.append(proc.children)


def parse_args():
    """
    Parse command line arguments.
    """
    # set up main parser
    parser = argparse.ArgumentParser(description='UProcTrace tool.')
    parser.add_argument('trace', help='trace file')
    subparsers = parser.add_subparsers()
    # dump
    dump_parser = subparsers.add_parser('dump', help='Dump events to stdout.')
    dump_parser.set_defaults(func=dump)
    # gui
    gui_parser = subparsers.add_parser('gui',
                                       help='Run graphical user interface.')
    gui_parser.set_defaults(func=gui)
    # pstree
    pstree_parser = subparsers.add_parser('pstree', help='Print process tree.')
    pstree_parser.set_defaults(func=pstree)
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
