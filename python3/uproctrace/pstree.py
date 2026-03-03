# UProcTrace: User-space Process Tracing
# Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
# Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
"""
Process tree command line interface of UProcTrace: "upt-tool pstree".
"""
import argparse
import tabulate
import uproctrace.formatting
import uproctrace.processes


def build(
    args: argparse.Namespace, processes: uproctrace.processes.Processes
) -> list[list[str]]:
    """
    Build rows for pstree command.
    """

    # build process tree (iterative)
    to_be_output = [processes.toplevel]
    rows: list[list[str]] = []
    while to_be_output:
        procs = to_be_output[-1]
        # pylint: disable=duplicate-code
        if not procs:
            del to_be_output[-1]
            continue
        proc = procs[0]
        del procs[0]

        # tree / indentation
        if args.table:
            indent = "--" * (len(to_be_output) - 1) + ">"
        else:
            indent = "  " * (len(to_be_output) - 1)
        row = [indent]
        # PIDs
        if args.pids:
            row += [f"{proc.proc_id}", f"{proc.pid}", f"{proc.ppid}"]
        # command line
        cmdline_str = uproctrace.formatting.cmdline2str(proc.cmdline)
        row.append(cmdline_str)
        # details
        if args.details:
            row += [
                uproctrace.formatting.timestamp2str(proc.begin_timestamp),
                uproctrace.formatting.timestamp2str(proc.end_timestamp),
                uproctrace.formatting.duration2str(proc.cpu_time),
                uproctrace.formatting.kb2str(proc.max_rss_kb),
                uproctrace.formatting.int2str(
                    uproctrace.formatting.add_none(proc.min_flt, proc.maj_flt)
                ),
                uproctrace.formatting.int2str(
                    uproctrace.formatting.add_none(proc.in_block, proc.ou_block)
                ),
                uproctrace.formatting.int2str(
                    uproctrace.formatting.add_none(proc.n_v_csw, proc.n_iv_csw)
                ),
            ]
        rows.append(row)
        to_be_output.append(proc.children)

    return rows


def output(args: argparse.Namespace, rows: list[list[str]]) -> None:
    """
    Output rows of pstree command.
    """
    if args.table:
        headers = ["tree"]
        if args.pids:
            headers += ["proc_id", "pid", "ppid"]
        headers.append("cmdline")
        if args.details:
            headers += [
                "begin",
                "end",
                "CPU time",
                "memory",
                "page faults",
                "filesys ops",
                "ctx switches",
            ]
        print(tabulate.tabulate(rows, headers))
    else:
        for row in rows:
            print(" ".join(row))


def pstree(args: argparse.Namespace) -> None:
    """
    Print process tree.
    """
    # pylint: disable=duplicate-code
    for upt_trace in args.trace:
        if len(args.trace) != 1:
            print(f"[{upt_trace:s}]:")
        with open(upt_trace, "rb") as proto_file:
            processes = uproctrace.processes.Processes(proto_file)

        rows = build(args, processes)
        output(args, rows)
