# UProcTrace: User-space Process Tracing
# Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
# Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
"""
Command line interface of UProcTrace: "upt-tool".
"""

import argparse
import sys

# pylint: disable=import-outside-toplevel


def dump(args):
    """
    Dump all events in trace file to standard output.
    """
    import uproctrace.dump

    for upt_trace in args.trace:
        if len(args.trace) != 1:
            print(f"[{upt_trace:s}]:")
        with open(upt_trace, "rb") as proto_file:
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
        print("error: upt-tool gui: only one trace file allowed", file=sys.stderr)
        return 1
    import uproctrace.gui

    uproctrace.gui.run(args.trace[0])
    return 0


def psinfo(args):
    """
    Print information about a process.
    """
    import uproctrace.psinfo

    uproctrace.psinfo.psinfo(args)


def pstree(args):
    """
    Print process tree.
    """
    import uproctrace.pstree

    uproctrace.pstree.pstree(args)


def parse_args():
    """
    Parse command line arguments.
    """
    # set up main parser
    parser = argparse.ArgumentParser(description="UProcTrace tool.")
    parser.add_argument(
        "trace",
        metavar="<trace.upt>",
        nargs="+",
        help="""
        The UPT trace file(s).
        """,
    )

    # Create sub parsers
    subparsers = parser.add_subparsers()

    # dump
    dump_parser = subparsers.add_parser(
        "dump",
        help="""
        Dump events to stdout.
        """,
    )
    dump_parser.set_defaults(func=dump)

    # gui
    gui_parser = subparsers.add_parser(
        "gui",
        help="""
        Run graphical user interface. Only supports a single trace file.
        """,
    )
    gui_parser.set_defaults(func=gui)

    # psinfo
    psinfo_parser = subparsers.add_parser(
        "psinfo",
        help="""
        Print information about a process.
        """,
    )
    psinfo_parser.add_argument(
        "--proc_id",
        "-i",
        type=int,
        required=True,
        help="proc_id of process (this is not the pid)",
    )
    psinfo_parser.set_defaults(func=psinfo)

    # pstree
    pstree_parser = subparsers.add_parser(
        "pstree",
        help="""
        Print process tree.
        """,
    )
    pstree_parser.add_argument(
        "--details",
        "-d",
        action="store_true",
        help="show process details (behind cmdline)",
    )
    pstree_parser.add_argument(
        "--pids",
        "-p",
        action="store_true",
        help="show proc_id, pid, parent pid (in front of cmdline)",
    )
    pstree_parser.add_argument(
        "--format",
        "-f",
        choices=["plain", "table", "csv", "json"],
        default="plain",
        help="output format",
    )
    pstree_parser.set_defaults(func=pstree)

    # stats
    stats_parser = subparsers.add_parser(
        "stats",
        help="""
      Dump trace statistics to stdout.
      """,
    )
    stats_parser.add_argument(
        "-p",
        "--per-trace",
        default=False,
        action="store_true",
        help="""
        If to calculate trace statistics per individual trace, instead of
        calculating statistics over all traces.
        """,
    )
    stats_parser.set_defaults(func=stats)

    # parse
    args = parser.parse_args()
    if not hasattr(args, "func"):
        print("error: no sub-command specified", file=sys.stderr)
        sys.exit(3)
    return args


def main():
    """
    upt-tool main function.
    Parse command line arguments and execute selected action.
    """
    args = parse_args()
    sys.exit(args.func(args))
