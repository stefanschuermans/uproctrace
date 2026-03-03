# UProcTrace: User-space Process Tracing
# Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
# Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
"""
Process info command line interface of UProcTrace: "upt-tool psinfo".
"""
import argparse
import functools
import uproctrace.formatting
import uproctrace.processes


def output(key: str, value: str, indent: int = 0):
    """
    Output a string detail of a process.
    """
    indent_str = "  " * (indent + 1)
    print(f"{indent_str}{key}: {value}")


def output_list(key: str, values: list[str], indent: int = 0):
    """
    Output a list of string details of a process.
    """
    if values is None:
        output(key, "???", indent)
        return
    output(key, f"{len(values):d} entries", indent)
    for i, value in enumerate(values):
        output(f"{key} {i:d}", value, indent + 1)


def output_list_sorted(key: str, values: list[str], indent: int = 0):
    """
    Wrapper for output_list(...) that sorts the list (if any) before.
    """
    values_sorted = sorted(values) if values is not None else None
    return output_list(key, values_sorted, indent)


def output_sum(key: str, sub_keys: list, values: list[int], indent: int = 0):
    """
    Output a sum of multiple values of a process and include individual
    values as subtree.
    """
    sum_val = functools.reduce(uproctrace.formatting.add_none, values, 0)
    output(key, uproctrace.formatting.int2str(sum_val), indent)
    for sub_key, val in zip(sub_keys, values):
        output(sub_key, uproctrace.formatting.int2str(val), indent + 1)


def psinfo(args: argparse.Namespace) -> None:
    """
    Print process information.
    """
    # pylint: disable=duplicate-code
    for upt_trace in args.trace:
        if len(args.trace) != 1:
            print(f"[{upt_trace:s}]:")
        with open(upt_trace, "rb") as proto_file:
            processes = uproctrace.processes.Processes(proto_file)

        proc = processes.getProcess(args.proc_id)
        if proc is None:
            print(f"  proc_id {args.proc_id} not found")
            continue

        output("begin time", uproctrace.formatting.timestamp2str(proc.begin_timestamp))
        output_list("command line", proc.cmdline)
        output_sum(
            "context switches",
            ["involuntary", "voluntary"],
            [proc.n_iv_csw, proc.n_v_csw],
        )
        output("CPU time", uproctrace.formatting.duration2str(proc.cpu_time))
        output("end time", uproctrace.formatting.timestamp2str(proc.end_timestamp))
        output_list_sorted("environment", proc.environ)
        output("executable", uproctrace.formatting.str2str(proc.exe))
        output_sum(
            "file system operations",
            ["input", "output"],
            [proc.in_block, proc.ou_block],
        )
        output("max. resident memory", uproctrace.formatting.kb2str(proc.max_rss_kb))
        output_sum("page faults", ["major", "minor"], [proc.maj_flt, proc.min_flt])
        output("pid", uproctrace.formatting.int2str(proc.pid))
        output("ppid", uproctrace.formatting.int2str(proc.ppid))
        output("system CPU time", uproctrace.formatting.duration2str(proc.sys_time))
        output("user CPU time", uproctrace.formatting.duration2str(proc.user_time))
        output("working directory", uproctrace.formatting.str2str(proc.cwd))
        # output parent
        parent_proc = proc.parent
        if parent_proc is None:
            output("parent", "???")
        else:
            output("parent", uproctrace.formatting.cmdline2str(parent_proc.cmdline))
        # output children
        child_procs = proc.children
        if child_procs is None:
            output("children", "???")
        else:
            output("children", f"{len(child_procs):d} entries")
            for i, child_proc in enumerate(child_procs):
                output(
                    f"child {i:d}",
                    uproctrace.formatting.cmdline2str(child_proc.cmdline),
                    1,
                )
