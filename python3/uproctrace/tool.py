# UProcTrace: User-space Process Tracing
# Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
# Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
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
    for upt_trace in args.trace:
        if len(args.trace) != 1:
            print(f"[{upt_trace:s}]:")
        with open(upt_trace, 'rb') as proto_file:
            while uproctrace.dump.dump_event(proto_file, sys.stdout):
                pass
        if len(args.trace) != 1:
            print("")


def stats(args):
    """
    Calculate trace statistics of trace file(s) and dump them to standard
    output.
    """
    import uproctrace.stats
    if not args.per_trace:
        uproctrace.stats.dump_stats(args.trace)
        return
    for upt_trace in args.trace:
        print(f"[{upt_trace:s}]:")
        uproctrace.stats.dump_stats([upt_trace])
        print("")


def gui(args):
    """
    Run the graphical user interface.
    """
    if len(args.trace) != 1:
        print(
            "error: upt-tool gui: only one trace file allowed",
            file=sys.stderr)
        return 1
    import uproctrace.gui
    uproctrace.gui.run(args.trace[0])
    return 0


def pstree(args):
    """
    Print process tree.
    """
    import uproctrace.processes
    for upt_trace in args.trace:
        if len(args.trace) != 1:
            print(f"[{upt_trace:s}]:")
        with open(upt_trace, 'rb') as proto_file:
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
    parser.add_argument(
        'trace',
        metavar='<trace.upt>',
        nargs='+',
        help="""
        The UPT trace file(s).
        """)

    # Create sub parsers
    subparsers = parser.add_subparsers()

    # dump
    dump_parser = subparsers.add_parser(
        'dump', help="""
        Dump events to stdout.
        """)
    dump_parser.set_defaults(func=dump)

    # gui
    gui_parser = subparsers.add_parser(
        'gui',
        help="""
        Run graphical user interface. Only supports a single trace file.
        """)
    gui_parser.set_defaults(func=gui)

    # pstree
    pstree_parser = subparsers.add_parser(
        'pstree', help="""
        Print process tree.
        """)
    pstree_parser.set_defaults(func=pstree)

    # stats
    stats_parser = subparsers.add_parser(
        'stats', help="""
      Dump trace statistics to stdout.
      """)
    stats_parser.add_argument(
        "-p",
        "--per-trace",
        default=False,
        action="store_true",
        help="""
        If to calculate trace statistics per individual trace, instead of
        calculating statistics over all traces.
        """)
    stats_parser.set_defaults(func=stats)

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
    sys.exit(args.func(args))
