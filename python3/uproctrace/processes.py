# UProcTrace: User-space Process Tracing
# Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
# Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
"""
Processes in a trace file.
"""

import collections
import uproctrace.parse


class Process():
    """
    A process parsed from a trace.
    """

    # pylint: disable=R0904
    def __init__(self, proc_id: int, pid: int):
        """
        Initialize process.
        """
        self._proc_id = proc_id
        self._pid = pid
        self._begin = None
        self._end = None
        self._parent = None
        self._children = collections.OrderedDict()  # proc_id -> Process

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
        return list(self._children.values())

    @property
    def cmdline(self) -> list:
        """
        Command line of process.
        """
        if self._begin is None:
            return None
        return self._begin.cmdline

    @property
    def cpu_time(self) -> float:
        """
        CPU time of process (in s).
        """
        if self._end is None:
            return None
        return self._end.cpu_time

    @property
    def cwd(self) -> str:
        """
        Working directory of process.
        """
        if self._begin is None:
            return None
        return self._begin.cwd

    @property
    def end_timestamp(self) -> list:
        """
        End timestamp of process.
        """
        if self._end is None:
            return None
        return self._end.timestamp

    @property
    def environ(self) -> list:
        """
        Environment of process.
        """
        if self._begin is None:
            return None
        return self._begin.environ

    @property
    def exe(self) -> str:
        """
        Executable of process.
        """
        if self._begin is None:
            return None
        return self._begin.exe

    @property
    def in_block(self) -> int:
        """
        Number of input operations on file system.
        """
        if self._end is None:
            return None
        return self._end.in_block

    @property
    def maj_flt(self) -> int:
        """
        Major page fault count (i.e. I/O needed).
        """
        if self._end is None:
            return None
        return self._end.maj_flt

    @property
    def max_rss_kb(self) -> int:
        """
        Maximum resident set size of process (in KiB).
        """
        if self._end is None:
            return None
        return self._end.max_rss_kb

    @property
    def min_flt(self) -> int:
        """
        Minor page fault count (i.e. no I/O).
        """
        if self._end is None:
            return None
        return self._end.min_flt

    @property
    def n_iv_csw(self) -> int:
        """
        Number of involuntary context switches.
        """
        if self._end is None:
            return None
        return self._end.n_iv_csw

    @property
    def n_v_csw(self) -> int:
        """
        Number of voluntary context switches.
        """
        if self._end is None:
            return None
        return self._end.n_v_csw

    @property
    def ou_block(self) -> int:
        """
        Number of output operations on file system.
        """
        if self._end is None:
            return None
        return self._end.ou_block

    @property
    def parent(self):
        """
        Parent process (or None).
        """
        return self._parent

    @property
    def pid(self):
        """
        Linux process ID.
        """
        if self._begin is not None:
            return self._begin.pid
        if self._end is not None:
            return self._end.pid
        return None

    @property
    def ppid(self):
        """
        Linux process ID of parent process.
        """
        if self._begin is None:
            return None
        return self._begin.ppid

    @property
    def proc_id(self):
        """
        Process ID. (This is not the PID.)
        """
        return self._proc_id

    @property
    def sys_time(self) -> float:
        """
        System CPU time of process (in s).
        """
        if self._end is None:
            return None
        return self._end.sys_time

    @property
    def user_time(self) -> float:
        """
        User CPU time of process (in s).
        """
        if self._end is None:
            return None
        return self._end.user_time

    def addChild(self, child):
        """
        Add a child process.
        """
        self._children[child.proc_id] = child

    def removeChild(self, child_proc_id: int):
        """
        Remove a child process.
        """
        if child_proc_id in self._children:
            del self._children[child_proc_id]

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
        self._all_processes = dict()  # proc_id -> process
        self._current_processes = dict()  # pid -> process (while pid alive)
        # ordered dictionary of toplevel processes: proc_id -> Process
        self._toplevel_processes = collections.OrderedDict()
        # parse trace
        self._readTrace(proto_file)

    def _getProcess(self, pid: int) -> Process:
        """
        Get process with passed PID.
        Create it if it does not exist.
        Return process.
        """
        if pid in self._current_processes:
            return self._current_processes[pid]
        return self._newProcess(pid)

    def _newProcess(self, pid: int) -> Process:
        """
        Create new process and set its PID.
        Store it in all processes and current processes.
        Make it a toplevel process initially (may be changed by caller).
        Return new process.
        """
        proc_id = len(self._all_processes)
        proc = Process(proc_id, pid)
        self._all_processes[proc_id] = proc
        self._current_processes[pid] = proc
        self._toplevel_processes[proc_id] = proc
        return proc

    def _parentChild(self, parent: Process, child: Process):
        """
        Establish parent/child relationship of two processes.
        """
        # terminate old relationship (if any)
        if child.parent is not None:
            child.parent.removeChild(child.proc_id)
        if child.proc_id in self._toplevel_processes:
            del self._toplevel_processes[child.proc_id]
        # establish new relationship
        parent.addChild(child)
        child.setParent(parent)

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
    def toplevel(self) -> list:
        """
        List of toplevel processes.
        """
        return list(self._toplevel_processes.values())

    def getAllProcesses(self) -> dict:
        """
        Return all processes.
        """
        return self._all_processes.copy()

    def getProcess(self, proc_id: int) -> Process:
        """
        Return process with proc_id, or None if not found.
        """
        return self._all_processes.get(proc_id)

    def visitProcBegin(self, proc_begin: uproctrace.parse.ProcBegin):
        """
        Process a process begin event.
        """
        self._visitBaseEvent(proc_begin)
        # new process
        proc = self._newProcess(proc_begin.pid)
        # set begin event of process and process of begin event
        proc.setBegin(proc_begin)
        proc_begin.setProcess(proc)
        # add process to parent if available
        if proc_begin.ppid is not None:
            parent = self._getProcess(proc_begin.ppid)
            self._parentChild(parent, proc)

    def visitProcEnd(self, proc_end: uproctrace.parse.ProcEnd):
        """
        Process a process end event.
        """
        self._visitBaseEvent(proc_end)
        # get process
        proc = self._getProcess(proc_end.pid)
        # set end event of process and process of end event
        proc.setEnd(proc_end)
        proc_end.setProcess(proc)
        # remove process from dict of current processes (it ended)
        #   - it is guaranteed to be in it, because it came from _getProcess()
        del self._current_processes[proc_end.pid]
