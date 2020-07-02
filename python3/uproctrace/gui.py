# UProcTrace: User-space Process Tracing
# Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
# Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)

"""
Graphical user interface of UProcTrace.
"""

import shlex
import time

import uproctrace.gui_glade
import uproctrace.processes

# pylint: disable=C0411
import gi
gi.require_version('Gtk', '3.0')
# pylint: disable=C0413
from gi.repository import Gtk


def cmdline2str(cmdline: list) -> str:
    """
    Convert command line to string.
    """
    if cmdline is None:
        return '???'
    return ' '.join([shlex.quote(s) for s in cmdline])


def duration2str(duration: float) -> str:
    """
    Convert duration to string.
    """
    if duration is None:
        return '???'
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
    txt = ''
    if dur_d > 0:
        txt += f'{dur_d:d} d '
    if dur_h > 0 or txt:
        txt += f'{dur_h:d} h '
    if dur_m > 0 or txt:
        txt += f'{dur_m:d} m '
    if dur_s > 0 or txt:
        txt += f'{dur_s:d} s '
    if dur_ms > 0 or txt:
        txt += f'{dur_ms:d} ms '
    if dur_us > 0 or txt:
        txt += f'{dur_us:d} us '
    txt += f'{dur_ns:d} ns '
    txt += f'({duration:f} s)'
    return txt


def kb2str(size_kb: int) -> str:
    """
    Convert size in KiB to string.
    """
    if size_kb is None:
        return '???'
    # split into GiB, MiB, KiB
    mib = size_kb // 1024
    kib = size_kb % 1024
    gib = mib // 1024
    mib = mib % 1024
    # assemble text
    txt = ''
    if gib > 0:
        txt += f'{gib:d} GiB '
    if mib > 0 or txt:
        txt += f'{mib:d} MiB '
    txt += f'{kib:d} KiB '
    txt += f'({size_kb:d} KiB)'
    return txt


def timestamp2str(timestamp: float) -> str:
    """
    Convert a timestamp to a human-reable time string."
    """
    if timestamp is None:
        return '???'
    sec = int(timestamp)
    nsec = int((timestamp - sec) * 1e9)
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec))
    return time_str + f'.{nsec:09d}'


class UptGui:
    """
    Graphical user interface of UProcTrace.
    """

    DETAIL_PROC_ID = 0
    DETAIL_KEY = 1
    DETAIL_VALUE = 2
    PROC_PROC_ID = 0
    PROC_BEGIN_TIMESTAMP = 1
    PROC_BEGIN_TIMESTAMP_TEXT = 2
    PROC_END_TIMESTAMP = 3
    PROC_END_TIMESTAMP_TEXT = 4
    PROC_CMDLINE = 5
    PROC_CPU_TIME = 6
    PROC_CPU_TIME_TEXT = 7
    PROC_MAX_RSS_KB = 8
    PROC_MAX_RSS_KB_TEXT = 9

    def __init__(self, proto_filename):
        """
        Construct the GUI.
        """
        self.builder = Gtk.Builder()
        self.builder.add_from_string(uproctrace.gui_glade.DATA)
        self.wid_details_tree = self.builder.get_object('DetailsTree')
        self.wid_details_view = self.builder.get_object('DetailsView')
        self.wid_processes_tree = self.builder.get_object('ProcessesTree')
        self.wid_processes_view = self.builder.get_object('ProcessesView')
        handlers = {
            'onDestroy': self.onDestroy,
            'onDetailsRowActivated': self.onDetailsRowActivated,
            'onProcessesCursorChanged': self.onProcessesCursorChanged
        }
        self.builder.connect_signals(handlers)
        # open trace file
        self.openTrace(proto_filename)

    def onDestroy(self, _widget):
        """
        Window will be destroyed.
        """
        Gtk.main_quit()

    def onDetailsRowActivated(self, _widget, _row, _col):
        """
        Row in details view has been activated.
        """
        # get proc_id of selected row (if any)
        detail_sel = self.wid_details_view.get_selection()
        if detail_sel is None:
            return
        detail_iter = detail_sel.get_selected()[1]
        if detail_iter is None:
            return
        proc_id = self.wid_details_tree.get_value(detail_iter,
                                                  self.DETAIL_PROC_ID)
        # do nothing for rows without valid proc_id
        if proc_id < 0:
            return
        # select process
        self.selectProcess(proc_id)
        # show details of selected process
        self.showDetails(proc_id)

    def onProcessesCursorChanged(self, _widget):
        """
        Cursor changed in processes tree view.
        """
        # get proc_id of selected process
        proc_sel = self.wid_processes_view.get_selection()
        if proc_sel is None:
            self.showDetails(None)
            return
        proc_iter = proc_sel.get_selected()[1]
        if proc_iter is None:
            self.showDetails(None)
            return
        proc_id = self.wid_processes_tree.get_value(proc_iter,
                                                    self.PROC_PROC_ID)
        # show details of selected process
        self.showDetails(proc_id)

    def openTrace(self, proto_filename: str):
        """
        Open a trace file.
        """
        # forget old processes
        self.wid_processes_tree.clear()
        # lead new data
        with open(proto_filename, 'rb') as proto_file:
            self.processes = uproctrace.processes.Processes(proto_file)
        # add processes to processes tree store
        to_be_output = [(self.processes.toplevel, None)]
        while to_be_output:
            procs, parent_iter = to_be_output[-1]
            if not procs:
                del to_be_output[-1]
                continue
            proc = procs[0]
            del procs[0]
            proc_iter = self.wid_processes_tree.append(parent_iter)
            self.wid_processes_tree.set_value(proc_iter, self.PROC_PROC_ID,
                                              proc.proc_id)
            self.wid_processes_tree.set_value(proc_iter,
                                              self.PROC_BEGIN_TIMESTAMP,
                                              proc.begin_timestamp)
            self.wid_processes_tree.set_value(
                proc_iter, self.PROC_BEGIN_TIMESTAMP_TEXT,
                timestamp2str(proc.begin_timestamp))
            self.wid_processes_tree.set_value(proc_iter,
                                              self.PROC_END_TIMESTAMP,
                                              proc.end_timestamp)
            self.wid_processes_tree.set_value(
                proc_iter, self.PROC_END_TIMESTAMP_TEXT,
                timestamp2str(proc.end_timestamp))
            self.wid_processes_tree.set_value(proc_iter, self.PROC_CMDLINE,
                                              cmdline2str(proc.cmdline))
            self.wid_processes_tree.set_value(proc_iter, self.PROC_CPU_TIME,
                                              proc.cpu_time)
            self.wid_processes_tree.set_value(proc_iter,
                                              self.PROC_CPU_TIME_TEXT,
                                              duration2str(proc.cpu_time))
            self.wid_processes_tree.set_value(proc_iter, self.PROC_MAX_RSS_KB,
                                              proc.max_rss_kb)
            self.wid_processes_tree.set_value(proc_iter,
                                              self.PROC_MAX_RSS_KB_TEXT,
                                              kb2str(proc.max_rss_kb))
            to_be_output.append((proc.children, proc_iter))
        # show all processes
        self.wid_processes_view.expand_all()

    def selectProcess(self, proc_id: int):
        """
        Select a process.
        """
        # get selection
        proc_sel = self.wid_processes_view.get_selection()
        if proc_sel is None:
            return
        # deselect all processes
        proc_sel.unselect_all()
        # leave if invalid proc_id
        if proc_id is None or proc_id < 0:
            return
        # select process with proc_id
        # scroll the process into view
        def update(proc_store, proc_path, proc_iter, _ctx):
            """
            Called for every item in tree.
            If item matches proc_id, select it and scroll it into view.
            """
            if proc_store.get_value(proc_iter, self.PROC_PROC_ID) != proc_id:
                return
            proc_sel.select_iter(proc_iter)
            self.wid_processes_view.scroll_to_cell(proc_path)

        self.wid_processes_tree.foreach(update, None)

    def showDetails(self, proc_id: int):
        """
        Show details of process.
        """
        # forget old details
        self.wid_details_tree.clear()
        # leave if invalid proc_id
        # get process
        if proc_id is None or proc_id < 0:
            return
        proc = self.processes.getProcess(proc_id)
        if proc is None:
            return
        # add details of new process
        def add(key: str, value: str, parent_iter=None):
            """
            Add a string detail to a process.
            Add to specified parent (if parent_iter is specified).
            Return iterator to added detail.
            """
            detail_iter = self.wid_details_tree.append(parent_iter)
            self.wid_details_tree.set_value(detail_iter, self.DETAIL_PROC_ID,
                                            -1)
            self.wid_details_tree.set_value(detail_iter, self.DETAIL_KEY, key)
            self.wid_details_tree.set_value(detail_iter, self.DETAIL_VALUE,
                                            value)
            return detail_iter

        def add_list(key: str, values: list, parent_iter=None):
            """
            Add a list of string details to a process as subtree.
            Add to specified parent (if parent_iter is specified).
            Return iterator to added top-level of detail subtree.
            """
            if values is None:
                return add(key, '???', parent_iter)
            list_iter = add(key, f'{len(values):d} entries', parent_iter)
            for i, value in enumerate(values):
                add(f'{key} {i:d}', value, list_iter)
            return list_iter

        add('begin time', timestamp2str(proc.begin_timestamp))
        cmdline_iter = add_list('command line', proc.cmdline)
        self.wid_details_view.expand_row(
            self.wid_details_tree.get_path(cmdline_iter), True)
        add('CPU time', duration2str(proc.cpu_time))
        add('end time', timestamp2str(proc.end_timestamp))
        add_list('environment', sorted(proc.environ))
        add('executable', proc.exe)
        add('max. resident memory', kb2str(proc.max_rss_kb))
        add('pid', str(proc.pid))
        add('ppid', str(proc.ppid))
        add('system CPU time', duration2str(proc.sys_time))
        add('user CPU time', duration2str(proc.user_time))
        add('working directory', proc.cwd)
        # add parent
        parent_proc = proc.parent
        if parent_proc is None:
            add('parent', '???')
        else:
            parent_iter = add('parent', cmdline2str(parent_proc.cmdline))
            self.wid_details_tree.set_value(parent_iter, self.DETAIL_PROC_ID,
                                            parent_proc.proc_id)
        # add children
        child_procs = proc.children
        if child_procs is None:
            add('children', '???')
        else:
            list_iter = add('children', f'{len(child_procs):d} entries')
            for i, child_proc in enumerate(child_procs):
                child_iter = add(f'child {i:d}',
                                 cmdline2str(child_proc.cmdline), list_iter)
                self.wid_details_tree.set_value(child_iter,
                                                self.DETAIL_PROC_ID,
                                                child_proc.proc_id)
            self.wid_details_view.expand_row(
                self.wid_details_tree.get_path(list_iter), True)


def run(proto_filename):
    """
    Run the graphical user interface for the specified trace file.
    """
    app = UptGui(proto_filename)
    try:
        Gtk.main()
    except KeyboardInterrupt:
        pass
    finally:
        del app
