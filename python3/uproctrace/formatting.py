# UProcTrace: User-space Process Tracing
# Copyright 2026: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
# Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
"""
Formatting of metrics to text for UProcTrace.
"""

import re
import shlex
import time

# regular expression for an environment variable assignment
RE_ENV_VAR = re.compile(r"^(?P<name>[A-Za-z_][A-Za-z0-9_]*)=(?P<value>.*)$")


def add_none(val_a: int, val_b: int) -> int:
    """
    Integer addition with support for None.
    """
    if val_a is None or val_b is None:
        return None
    return val_a + val_b


def cmdline2str(cmdline: list[str]) -> str:
    """
    Convert command line to string.
    """
    if cmdline is None:
        return "???"
    return " ".join([cmdline_str_escape(s) for s in cmdline])


def cmdline_str_escape(string: str) -> str:
    """
    Escape a command line string for shell use in a way that also works for
    environment variables (i.e., not escaping the variable name).
    """
    match = RE_ENV_VAR.match(string)
    if not match:
        # not a variable assignment -> escape entire string
        return shlex.quote(string)
    # variable assignment -> escape only value part
    # (also works if it only looks like a variable assignment)
    name = match.group("name")
    value = shlex.quote(match.group("value"))
    return f"{name:s}={value:s}"


def duration2str(duration: float) -> str:
    """
    Convert duration to string.
    """
    if duration is None:
        return "???"
    # split into day, hours, minutes, seconds
    dur_s = int(duration)
    dur_m = dur_s // 60
    dur_s = dur_s % 60
    dur_h = dur_m // 60
    dur_m = dur_m % 60
    dur_d = dur_h // 24
    dur_h = dur_h % 24
    # split into ms, us, ns
    dur_ns = int((duration - dur_s) * 1e9)
    dur_us = dur_ns // 1000
    dur_ns = dur_ns % 1000
    dur_ms = dur_us // 1000
    dur_us = dur_us % 1000
    # assemble text
    txt = ""
    if dur_d > 0:
        txt += f"{dur_d:d} d "
    if dur_h > 0 or txt:
        txt += f"{dur_h:d} h "
    if dur_m > 0 or txt:
        txt += f"{dur_m:d} m "
    if dur_s > 0 or txt:
        txt += f"{dur_s:d} s "
    if dur_ms > 0 or txt:
        txt += f"{dur_ms:d} ms "
    if dur_us > 0 or txt:
        txt += f"{dur_us:d} us "
    txt += f"{dur_ns:d} ns "
    txt += f"({duration:f} s)"
    return txt


def int2str(val: int) -> str:
    """
    Convert integer to string, support None.
    """
    if val is None:
        return "???"
    return f"{val:d}"


def kb2str(size_kb: int) -> str:
    """
    Convert size in KiB to string.
    """
    if size_kb is None:
        return "???"
    # split into GiB, MiB, KiB
    mib = size_kb // 1024
    kib = size_kb % 1024
    gib = mib // 1024
    mib = mib % 1024
    # assemble text
    txt = ""
    if gib > 0:
        txt += f"{gib:d} GiB "
    if mib > 0 or txt:
        txt += f"{mib:d} MiB "
    txt += f"{kib:d} KiB "
    txt += f"({size_kb:d} KiB)"
    return txt


def str2str(str_or_none: str) -> str:
    """
    Convert string (or None) to string.
    """
    if str_or_none is None:
        return "???"
    return str_or_none


def timestamp2str(timestamp: float) -> str:
    """
    Convert a timestamp to a human-reable time string."
    """
    if timestamp is None:
        return "???"
    sec = int(timestamp)
    nsec = int((timestamp - sec) * 1e9)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sec))
    return time_str + f".{nsec:09d}"
