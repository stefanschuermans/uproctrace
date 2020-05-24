#! /usr/bin/env python3

import gi
import os
import shlex
import sys
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import uproctrace.processes


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
    s = int(duration)
    m = s // 60
    s = s % 60
    h = m // 60
    m = m % 60
    d = h // 24
    h = h % 24
    # split into ms, us, ns
    ns = int((duration - s) * 1e9)
    us = ns // 1000
    ns = ns % 1000
    ms = us // 1000
    us = us % 1000
    # assemble text
    txt = ''
    if d > 0:
        txt += f'{d:d} d '
    if h > 0 or txt:
        txt += f'{h:d} h '
    if m > 0 or txt:
        txt += f'{m:d} m '
    if s > 0 or txt:
        txt += f'{s:d} s '
    if ms > 0 or txt:
        txt += f'{ms:d} ms '
    if us > 0 or txt:
        txt += f'{us:d} us '
    txt += f'{ns:d} ns '
    txt += f'({duration:f} s)'
    return txt


def kb2str(kb: int) -> str:
    """
    Convert size in KiB to string.
    """
    if kb is None:
        return '???'
    # split into GiB, MiB, KiB
    mib = kb // 1024
    kib = kb % 1024
    gib = mib // 1024
    mib = mib % 1024
    # assemble text
    txt = ''
    if gib > 0:
        txt += f'{gib:d} GiB '
    if mib > 0 or txt:
        txt += f'{mib:d} MiB '
    txt += f'{kib:d} KiB '
    txt += f'({kb:d} KiB)'
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

    DETAIL_KEY = 0
    DETAIL_VALUE = 1
    PROC_PROC_ID = 0
    PROC_BEGIN = 1
    PROC_END = 2
    PROC_COMMAND = 3

    def __init__(self, proto_filename):
        """
        Construct the GUI.
        """
        self.builder = Gtk.Builder()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.builder.add_from_file(os.path.join(script_dir, 'upt-gui.glade'))
        self.widDetailsTree = self.builder.get_object('DetailsTree')
        self.widDetailsView = self.builder.get_object('DetailsView')
        self.widProcessesTree = self.builder.get_object('ProcessesTree')
        self.widProcessesView = self.builder.get_object('ProcessesView')
        handlers = {
            'onDestroy': self.onDestroy,
            'onProcessesCursorChanged': self.onProcessesCursorChanged
        }
        self.builder.connect_signals(handlers)
        # open trace file
        self.openTrace(proto_filename)

    def onDestroy(self, widget):
        """
        Window will be destroyed.
        """
        Gtk.main_quit()

    def onProcessesCursorChanged(self, widget):
        """
        Cursor changed in processes tree view.
        """
        # get proc_id of selected process
        proc_id = None
        proc_sel = self.widProcessesView.get_selection()
        if proc_sel is not None:
            proc_iter = proc_sel.get_selected()[1]
            if proc_iter is not None:
                proc_id = self.widProcessesTree.get_value(
                    proc_iter, self.PROC_PROC_ID)
        # forget old details
        self.widDetailsTree.clear()
        # leave if no process selected
        if proc_id is None:
            return
        # get process, leave if not found
        proc = self.processes.getProcess(proc_id)
        if proc is None:
            return
        # add details of new process
        def add(key: str, value: str, parent_iter = None):
            detail_iter = self.widDetailsTree.append(parent_iter)
            self.widDetailsTree.set_value(detail_iter, self.DETAIL_KEY, key)
            self.widDetailsTree.set_value(detail_iter, self.DETAIL_VALUE,
                                          value)
            return detail_iter

        def add_list(key: str, values: list, parent_iter = None):
            if values is None:
                return add(key, '???', parent_iter)
            list_iter = add(key, f'{len(values):d} entries', parent_iter)
            for i, value in enumerate(values):
                add(f'{key} {i:d}', value, list_iter)

        add('begin time', timestamp2str(proc.begin_timestamp))
        add_list('command line', proc.cmdline)
        add('CPU time', duration2str(proc.cpu_time))
        add('end time', timestamp2str(proc.end_timestamp))
        add_list('environment', sorted(proc.environ))
        add('executable', proc.exe)
        add('max. resident memory', kb2str(proc.max_rss_kb))
        add('system CPU time', duration2str(proc.sys_time))
        add('user CPU time', duration2str(proc.user_time))
        add('working directory', proc.cwd)
        # TODO

    def openTrace(self, proto_filename: str):
        """
        Open a trace file.
        """
        # forget old processes
        self.widProcessesTree.clear()
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
            proc_iter = self.widProcessesTree.append(parent_iter)
            self.widProcessesTree.set_value(proc_iter, self.PROC_PROC_ID,
                                            proc.proc_id)
            self.widProcessesTree.set_value(
                proc_iter, self.PROC_BEGIN,
                timestamp2str(proc.begin_timestamp))
            self.widProcessesTree.set_value(proc_iter, self.PROC_END,
                                            timestamp2str(proc.end_timestamp))
            self.widProcessesTree.set_value(proc_iter, self.PROC_COMMAND,
                                            cmdline2str(proc.cmdline))
            to_be_output.append((proc.children, proc_iter))
        # show all processes
        self.widProcessesView.expand_all()


def main(argv):
    """
    Main program.
    """
    if len(argv) < 2:
        print('usage: ' + argv[0] + ' <trace.proto>', file=sys.stderr)
        return 2
    proto_filename = argv[1]
    app = UptGui(proto_filename)
    try:
        Gtk.main()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
