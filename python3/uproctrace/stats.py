# UProcTrace: User-space Process Tracing
# Copyright 2020: Florian Walbroel, Bonn, Germany <florian@hswalbroel.de>
# Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
"""
Statistics for uproctrace trace files.
"""

import tabulate
import uproctrace.processes

# Map of process attribute to attribute title and unit
_PROCESS_ATTRS = {
    "cpu_time": ("CPU Time", "s"),
    "sys_time": ("Kernel Time", "s"),
    "user_time": ("User Time", "s"),
    "in_block": ("Fileystem Input Operations", ""),
    "ou_block": ("Fileystem Output Operations", ""),
    "maj_flt": ("Major page fault count", ""),
    "min_flt": ("Minor page fault count", ""),
    "max_rss_kb": ("Maximum Resident Set Size", "KiB"),
}


def calculate_stats(upt_traces: list) -> dict:
    """
    Calculates trace statistics, such like the CPU time of processes, for
    the given list of traces and returns mapping of process attribute to
    tuple of (min value, mean value, max value, cummulative value).
    """

    # The overall statistics
    attr_values = dict((attr, []) for attr in _PROCESS_ATTRS)

    for upt_trace in upt_traces:

        # Load all processes of the trace file
        with open(upt_trace, "rb") as upt_f:
            processes = uproctrace.processes.Processes(upt_f)

        for process in processes.getAllProcesses().values():

            # Ignore processes for which we do not have full information
            if process.begin_timestamp is None or process.end_timestamp is None:
                continue

            # Update the values
            for attr in _PROCESS_ATTRS:
                attr_values[attr].append(getattr(process, attr))

    # Calulate the statistics
    stats = {}
    for attr, values in attr_values.items():
        if not values:
            stats[attr] = (0, 0, 0, 0)
            continue

        vmin = min(values)
        vmax = max(values)
        vcum = sum(values)
        vmean = vcum / len(values)
        stats[attr] = (vmin, vmean, vmax, vcum)

    return stats


def dump_stats(upt_traces: list):
    """
    Calculates trace statistics, such like the CPU time of processes, for
    the given list of traces and dumps the statistics to standard output as
    a table.
    """
    # Calulate the statistics
    stats = calculate_stats(upt_traces)

    rows = []
    for attr, values in stats.items():
        title, unit = _PROCESS_ATTRS[attr]
        rows += [[title] + [f"{v:.2f}{unit:s}" for v in values]]

    headers = ["Attribute", "Min", "Mean", "Max", "Cumulative"]
    print(tabulate.tabulate(rows, headers=headers))
