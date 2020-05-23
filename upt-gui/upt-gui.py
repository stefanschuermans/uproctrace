#! /usr/bin/env python3

import cairo
import datetime
import gi
import os
import shlex
import sys
import time
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Gtk

import uproctrace.processes


def cmdline2str(cmdline: list) -> str:
    """
    Convert command line to string.
    """
    if cmdline is None:
        return "???"
    return ' '.join([shlex.quote(s) for s in cmdline])

def timestamp2str(timestamp: float) -> str:
    """
    Convert a timestamp to a human-reable time string."
    """
    if timestamp is None:
        return "???"
    sec = int(timestamp)
    nsec = int((timestamp - sec) * 1e9)
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec))
    return time_str + f'.{nsec:09d}'


class UptGui:
    def __init__(self, proto_filename):
        """
        Construct the GUI.
        """
        self.builder = Gtk.Builder()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.builder.add_from_file(os.path.join(script_dir, 'upt-gui.glade'))
        self.widProcessesTree = self.builder.get_object('ProcessesTree')
        self.widProcessesView = self.builder.get_object('ProcessesView')
        handlers = {'onDestroy': self.onDestroy}
        self.builder.connect_signals(handlers)
        # open trace file
        self.openTrace(proto_filename)

    def onDestroy(self, widget):
        """
        Window will be destroyed.
        """
        Gtk.main_quit()

    def openTrace(self, proto_filename: str):
        """
        Open a trace file.
        """
        # forget old data
        self.widProcessesTree.clear()
        # lead new data
        with open(proto_filename, 'rb') as proto_file:
            self._processes = uproctrace.processes.Processes(proto_file)
        # add processes to processes tree store
        to_be_output = [(self._processes.toplevel, None)]
        while to_be_output:
            procs, parent_iter = to_be_output[-1]
            if not procs:
                del to_be_output[-1]
                continue
            proc = procs[0]
            del procs[0]
            proc_iter = self.widProcessesTree.append(parent_iter)
            self.widProcessesTree.set_value(proc_iter, 0, proc.proc_id)
            self.widProcessesTree.set_value(proc_iter, 1, timestamp2str(proc.begin_timestamp))
            self.widProcessesTree.set_value(proc_iter, 2, timestamp2str(proc.end_timestamp))
            self.widProcessesTree.set_value(proc_iter, 3, cmdline2str(proc.cmdline))
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
