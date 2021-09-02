# UProcTrace: User-space Process Tracing
# Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
# Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
"""
Graphical user interface of UProcTrace.
"""

import functools
import re
import shlex
import signal
import time

import uproctrace.gui_glade
import uproctrace.processes

# pylint: disable=C0411
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
# pylint: disable=C0413
from gi.repository import Gdk, Gtk, GLib, GObject

GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, Gtk.main_quit)

# regular expression for an environment variable assignment
RE_ENV_VAR = re.compile(r'^(?P<name>[A-Za-z_][A-Za-z0-9_]*)=(?P<value>.*)$')


def add_none(val_a: int, val_b: int) -> int:
    """
    Integer addition with support for None.
    """
    if val_a is None or val_b is None:
        return None
    return val_a + val_b


def cmdline2str(cmdline: list) -> str:
    """
    Convert command line to string.
    """
    if cmdline is None:
        return '???'
    return ' '.join([cmdline_str_escape(s) for s in cmdline])


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
    name = match.group('name')
    value = shlex.quote(match.group('value'))
    return f'{name:s}={value:s}'


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


def int2str(val: int) -> str:
    """
    Convert integer to string, support None.
    """
    if val is None:
        return '???'
    return f'{val:d}'


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


def str2str(str_or_none: str) -> str:
    """
    Convert string (or None) to string.
    """
    if str_or_none is None:
        return '???'
    return str_or_none


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

    # pylint: disable=R0902

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
    PROC_PAGE_FAULTS = 10
    PROC_PAGE_FAULTS_TEXT = 11
    PROC_FILE_SYS_OPS = 12
    PROC_FILE_SYS_OPS_TEXT = 13
    PROC_CTX_SW = 14
    PROC_CTX_SW_TEXT = 15

    def __init__(self, proto_filename):
        """
        Construct the GUI.
        """
        self.builder = Gtk.Builder()
        self.builder.add_from_string(uproctrace.gui_glade.DATA)
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.show_processes_as_tree = True
        self.wid_details_tree = self.builder.get_object('DetailsTree')
        self.wid_details_view = self.builder.get_object('DetailsView')
        self.wid_processes_tree = self.builder.get_object('ProcessesTree')
        self.wid_processes_view = self.builder.get_object('ProcessesView')
        self.wid_tree_toggle = self.builder.get_object('TreeToggle')
        self.notifier = self.builder.get_object("NotificationRevealer")
        self.notifier_msg = self.builder.get_object("NotificationMessage")
        self.notifier_timeout = None
        handlers = {
            'onDestroy': self.onDestroy,
            'onDetailsRowActivated': self.onDetailsRowActivated,
            'onProcessesCursorChanged': self.onProcessesCursorChanged,
            'onProcessesRowActivated': self.onProcessesRowActivated,
            'onTreeToggled': self.onTreeToggled,
            'onNotificationClose': self.onNotificationClose,
        }
        self.builder.connect_signals(handlers)
        # open trace file
        self.openTrace(proto_filename)

    def fillProcessesEntry(self, proc_iter,
                           proc: uproctrace.processes.Process):
        """
        Fill attributes of processes tree entry.
        proc_iter: process tree entry
        proc: process object
        """
        self.wid_processes_tree.set_value(proc_iter, self.PROC_PROC_ID,
                                          proc.proc_id)
        self.fillProcessesEntryAttr(proc_iter, self.PROC_BEGIN_TIMESTAMP,
                                    self.PROC_BEGIN_TIMESTAMP_TEXT,
                                    timestamp2str, proc.begin_timestamp)
        self.fillProcessesEntryAttr(proc_iter, self.PROC_END_TIMESTAMP,
                                    self.PROC_END_TIMESTAMP_TEXT,
                                    timestamp2str, proc.end_timestamp)
        self.wid_processes_tree.set_value(proc_iter, self.PROC_CMDLINE,
                                          cmdline2str(proc.cmdline))
        self.fillProcessesEntryAttr(proc_iter, self.PROC_CPU_TIME,
                                    self.PROC_CPU_TIME_TEXT, duration2str,
                                    proc.cpu_time)
        self.fillProcessesEntryAttr(proc_iter, self.PROC_MAX_RSS_KB,
                                    self.PROC_MAX_RSS_KB_TEXT, kb2str,
                                    proc.max_rss_kb)
        self.fillProcessesEntryAttr(proc_iter, self.PROC_PAGE_FAULTS,
                                    self.PROC_PAGE_FAULTS_TEXT, int2str,
                                    add_none(proc.min_flt, proc.maj_flt))
        self.fillProcessesEntryAttr(proc_iter, self.PROC_FILE_SYS_OPS,
                                    self.PROC_FILE_SYS_OPS_TEXT, int2str,
                                    add_none(proc.in_block, proc.ou_block))
        self.fillProcessesEntryAttr(proc_iter, self.PROC_CTX_SW,
                                    self.PROC_CTX_SW_TEXT, int2str,
                                    add_none(proc.n_v_csw, proc.n_iv_csw))

    def fillProcessesEntryAttr(self, proc_iter, col: int, text_col: int,
                               val2str_func, val):
        """
        Fill attribute of processes tree entry.
        proc_iter: process tree entry
        col: value column number
        text_col: text column number
        val2str_func: function to transform value to string
        val: value
        """
        # pylint: disable=R0913
        self.wid_processes_tree.set_value(proc_iter, col, val)
        self.wid_processes_tree.set_value(proc_iter, text_col,
                                          val2str_func(val))

    def onDestroy(self, _widget):
        """
        Window will be destroyed.
        """
        Gtk.main_quit()

    def onDetailsRowActivated(self, _widget, _row, _col):
        """
        Row in details view has been activated.
        """
        # get selected row (if any)
        detail_sel = self.wid_details_view.get_selection()
        if detail_sel is None:
            return
        detail_iter = detail_sel.get_selected()[1]
        if detail_iter is None:
            return
        # copy string of selected item or subtree to clipboard
        string = self.wid_details_tree.get_value(detail_iter,
                                                 self.DETAIL_VALUE)
        child_iter = self.wid_details_tree.iter_children(detail_iter)
        if child_iter is not None:
            # selected row has children, assemble command line from children
            strings = []
            while child_iter is not None:
                strings.append(
                    self.wid_details_tree.get_value(child_iter,
                                                    self.DETAIL_VALUE))
                child_iter = self.wid_details_tree.iter_next(child_iter)
            string = cmdline2str(strings)
        self.storeInClipboardAndNotify(string)
        # get proc_id of selected row, nothing else to do if none
        proc_id = self.wid_details_tree.get_value(detail_iter,
                                                  self.DETAIL_PROC_ID)
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

    def onProcessesRowActivated(self, _widget, _row, _col):
        """
        Row in processes view has been activated.
        """
        # get selected row (if any)
        processes_sel = self.wid_processes_view.get_selection()
        if processes_sel is None:
            return
        processes_iter = processes_sel.get_selected()[1]
        if processes_iter is None:
            return
        # get process
        proc_id = self.wid_processes_tree.get_value(processes_iter,
                                                    self.PROC_PROC_ID)
        if proc_id is None or proc_id < 0:
            return
        proc = self.processes.getProcess(proc_id)
        if proc is None:
            return
        # copy shell command line to repeat process call to clipboard
        # ( cd <workdir>; env -i <environment> <cmdline> )
        string = '('
        if proc.cwd:
            string += ' cd ' + cmdline_str_escape(proc.cwd) + ';'
        if proc.environ:
            string += ' env -i ' + cmdline2str(sorted(proc.environ))
        if proc.cmdline:
            string += ' ' + cmdline2str(proc.cmdline)
        string += ' )'
        self.storeInClipboardAndNotify(string)

    def onTreeToggled(self, _widget):
        """
        Tree button toggled: switch between tree and list.
        """
        # get new state
        self.show_processes_as_tree = self.wid_tree_toggle.get_active()
        # re-populate processes view
        self.populateProcesses()

    def onNotificationClose(self, _widget):
        """
        Notification close button pressed: close the notification
        """
        self.closeNotification()

    def closeNotification(self):
        """
        Closes the notification and kills the timeout if set
        """
        self.notifier.set_reveal_child(False)
        if self.notifier_timeout is not None:
            GObject.source_remove(self.notifier_timeout)
            self.notifier_timeout = None

    def showNotification(self, message: str, timeout_ms: int = None):
        """
        Shows a notification with the given message text, if timeout (in ms)
        is provided also sets a timeout to close the notification
        """
        self.closeNotification()

        self.notifier_msg.set_text(message)
        self.notifier.set_reveal_child(True)

        if timeout_ms is not None:
            self.notifier_timeout = GObject.timeout_add(
                timeout_ms, self.closeNotification)

    def storeInClipboard(self, string: str):
        """
        Stores a string in the clipboard
        """
        self.clipboard.set_text(string, -1)
        self.clipboard.store()

    def storeInClipboardAndNotify(self, string: str):
        """
        Stores a string in the clipboard and shows a "copied to clipboard"
        notification
        """
        self.storeInClipboard(string)
        msg = string if len(string) <= 100 else string[:97] + "..."
        self.showNotification(f"'{msg:s}'\nCopied to clipboard", 1000)

    def openTrace(self, proto_filename: str):
        """
        Open a trace file.
        """
        # load new data
        with open(proto_filename, 'rb') as proto_file:
            self.processes = uproctrace.processes.Processes(proto_file)
        # populate processes view
        self.populateProcesses()

    def populateProcesses(self):
        """
        Populate processes view.
        """
        # forget old processes
        self.wid_processes_tree.clear()
        # add processes to processes tree store
        to_be_output = [(self.processes.toplevel, None)]
        while to_be_output:
            procs, parent_iter = to_be_output[-1]
            if not procs:
                del to_be_output[-1]
                continue
            proc = procs[0]
            del procs[0]
            proc_iter = self.wid_processes_tree.append(
                parent_iter if self.show_processes_as_tree else None)
            self.fillProcessesEntry(proc_iter, proc)
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
        # pylint: disable=R0914
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

        def add_list_sorted(key: str, values: list, parent_iter=None):
            """
            Wrapper for add_list(...) that sorts the list (if any) before.
            """
            values_sorted = sorted(values) if values is not None else None
            return add_list(key, values_sorted, parent_iter)

        def add_sum(key: str, sub_keys: list, values: list, parent_iter=None):
            """
            Add a sum of multiple values to a process and include individual
            values as subtree.
            Add to specified parent (if parent_iter is specified).
            Return iterator to added top-level of detail subtree.
            """
            sum_val = functools.reduce(add_none, values, 0)
            sum_iter = add(key, int2str(sum_val), parent_iter)
            for sub_key, val in zip(sub_keys, values):
                add(sub_key, int2str(val), sum_iter)
            self.wid_details_view.expand_row(
                self.wid_details_tree.get_path(sum_iter), True)
            return sum_iter

        add('begin time', timestamp2str(proc.begin_timestamp))
        cmdline_iter = add_list('command line', proc.cmdline)
        self.wid_details_view.expand_row(
            self.wid_details_tree.get_path(cmdline_iter), True)
        add_sum('context switches', ['involuntary', 'voluntary'],
                [proc.n_iv_csw, proc.n_v_csw])
        add('CPU time', duration2str(proc.cpu_time))
        add('end time', timestamp2str(proc.end_timestamp))
        add_list_sorted('environment', proc.environ)
        add('executable', str2str(proc.exe))
        add_sum('file system operations', ['input', 'output'],
                [proc.in_block, proc.ou_block])
        add('max. resident memory', kb2str(proc.max_rss_kb))
        add_sum('page faults', ['major', 'minor'],
                [proc.maj_flt, proc.min_flt])
        add('pid', int2str(proc.pid))
        add('ppid', int2str(proc.ppid))
        add('system CPU time', duration2str(proc.sys_time))
        add('user CPU time', duration2str(proc.user_time))
        add('working directory', str2str(proc.cwd))
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
                self.wid_details_tree.set_value(
                    child_iter, self.DETAIL_PROC_ID, child_proc.proc_id)
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
