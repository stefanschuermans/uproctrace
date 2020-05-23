"""
Processes in a trace file.
"""

import uproctrace.parse


class Process():
    """
    A process parsed from a trace.
    """
    def __init__(self, proc_id: int, pid: int):
        """
        Initialize process.
        """
        self._proc_id = proc_id
        self._pid = pid
        self._begin = None
        self._end = None
        self._parent = None
        self._children = list()

    @property
    def begin_timestamp(self) -> list:
        """
        Begin timestamp of process.
        """
        if self._begin is None:
            return None
        return self._begin.timestamp

    @property
    def children(self) -> list:
        """
        List of child processes.
        """
        return self._children.copy()

    @property
    def cmdline(self) -> list:
        """
        Command line of process.
        """
        if self._begin is None:
            return None
        return self._begin.cmdline

    @property
    def end_timestamp(self) -> list:
        """
        End timestamp of process.
        """
        if self._end is None:
            return None
        return self._end.timestamp

    @property
    def proc_id(self):
        """
        Process ID. (This is not the PID.)
        """
        return self._proc_id

    @property
    def parent(self):
        """
        Parent process (or None).
        """
        return self._parent

    def addChild(self, child):
        """
        Add a child process.
        """
        self._children.append(child)

    def setBegin(self, proc_begin: uproctrace.parse.ProcBegin):
        """
        Set begin event of process.
        """
        self._begin = proc_begin

    def setEnd(self, proc_end: uproctrace.parse.ProcEnd):
        """
        Set end event of process.
        """
        self._end = proc_end

    def setParent(self, parent):
        """
        Set parent process.
        """
        self._parent = parent


class Processes(uproctrace.parse.Visitor):
    """
    Collection of all processes from a trace.
    """
    def __init__(self, proto_file):
        """
        Initialize processes from a trace file (f).
        """
        super().__init__()
        self._timeline = dict()  # time -> list(parse.BaseEvent)
        self._all_processes = list()  # list of all processess
        self._current_processes = dict()  # pid -> process
        self._toplevel_processes = list()  # list of processes without parent
        self._readTrace(proto_file)

    def _newProcess(self, pid: int):
        """
        Create new process, set its PID, store it and return it.
        """
        proc = Process(len(self._all_processes), pid)
        self._all_processes.append(proc)
        return proc

    def _readTrace(self, proto_file):
        """
        Read events from trace file (proto_file) and add them.
        """
        while uproctrace.parse.parse_event(proto_file, self):
            pass

    def _visitBaseEvent(self, event: uproctrace.parse.BaseEvent):
        """
        Common processing for all events.
        """
        # store event in timeline
        self._timeline.setdefault(event.timestamp, list()).append(event)

    @property
    def toplevel(self):
        """
        List of toplevel processes.
        """
        return self._toplevel_processes.copy()

    def visitProcBegin(self, proc_begin: uproctrace.parse.ProcBegin):
        """
        Process a process begin event.
        """
        self._visitBaseEvent(proc_begin)
        # new process
        proc = self._newProcess(proc_begin.pid)
        # add process to dict of current processes
        self._current_processes[proc_begin.pid] = proc
        # set begin event of process and process of begin event
        proc.setBegin(proc_begin)
        proc_begin.setProcess(proc)
        # connect to parent
        if proc_begin.ppid in self._current_processes:
            parent = self._current_processes[proc_begin.ppid]
            proc.setParent(parent)
            parent.addChild(proc)
        else:
            self._toplevel_processes.append(proc)

    def visitProcEnd(self, proc_end: uproctrace.parse.ProcEnd):
        """
        Process a process end event.
        """
        self._visitBaseEvent(proc_end)
        # get process (or create it if it is not known)
        if proc_end.pid in self._current_processes:
            proc = self._current_processes[proc_end.pid]
        else:
            proc = self._newProcess(proc_end.pid)
        # set end event of process and process of end event
        proc.setEnd(proc_end)
        proc_end.setProcess(proc)
        # remove process from dict of current processes (it ended)
        self._current_processes[proc_end.pid] = None
