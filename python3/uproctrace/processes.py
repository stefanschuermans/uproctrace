"""
Processes in a trace file.
"""

import uproctrace.parse


class Process():
    """
    A process parsed from a trace.
    """

    def __init__(self, pid: int):
        """
        Initialize process.
        """
        self._pid = pid
        self._begin = None
        self._end = None

    def setBegin(self, proc_begin: uproctrace.parse.ProcBegin):
        """
        set begin event of process
        """
        self._begin = proc_begin

    def setEnd(self, proc_end: uproctrace.parse.ProcEnd):
        """
        set end event of process
        """
        self._end = proc_end


class Processes(uproctrace.parse.Visitor):
    """
    Collection of all processes from a trace.
    """

    def __init__(self, proto_file):
        """
        Initialize processes from a trace file (f).
        """
        super().__init__()
        self._processes = dict()  # pid -> Process
        self._readTrace(proto_file)

    def _readTrace(self, proto_file):
        """
        Read events from trace file (proto_file) and add them.
        """
        while uproctrace.parse.parse_event(proto_file, self):
            pass

    def visitProcBegin(self, proc_begin: uproctrace.parse.ProcBegin):
        """
        Process a process begin event.
        """
        # new process
        proc = Process(proc_begin.pid)
        # add process to dict of current processes
        self._processes[proc_begin.pid] = proc
        # set begin event of process
        proc.setBegin(proc_begin)

    def visitProcEnd(self, proc_end: uproctrace.parse.ProcEnd):
        """
        Process a process end event.
        """
        # get process (or create it it is not known)
        if proc_end.pid in self._processes:
            proc = self._processes[proc_end.pid]
        else:
            proc = Process(proc_end.pid)
        # set end event of process
        proc.setEnd(proc_end)
        # remove process from dict of current processes (it ended)
        self._processes[proc_end.pid] = None
