# UProcTrace: User-space Process Tracing
# Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
# Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
"""
Parsing of uproctrace protobuf 2 events.
"""

import abc
import struct

import uproctrace.uproctrace_pb2 as pb2


def read_event(proto_file):
    """
    Read the first event from proto_file and return it.
    Return None if no event could be found.
    """
    # skip till after magic
    magic = proto_file.read(4)
    while magic != b'upt0':
        if len(magic) < 4:
            return None  # EOF
        magic = magic[1:] + proto_file.read(1)  # search magic byte for byte
    # read size of next event (32 bit network byte order)
    size = proto_file.read(4)
    if len(size) < 4:
        return None  # EOF
    size = struct.unpack('!L', size)[0]
    # read event data
    data = proto_file.read(size)
    if len(data) < size:
        return None  # EOF
    # unpack event
    pb2_ev = pb2.event.FromString(data)
    return pb2_ev


class BaseEvent():
    """
    Base class for all events.
    """
    def __init__(self, pb2_ev: pb2.event):
        """
        Initialize base event from PB2 event.
        """
        super().__init__()
        self._pb2_ev = pb2_ev
        self._timestamp = self._pb2GetTimespec(pb2_ev.timestamp)

    def _pb2GetStringList(self, s_l: pb2.stringlist) -> list:
        """
        Get PB2 string list as Python list.
        """
        return [s for s in s_l.s]

    def _pb2GetTimespec(self, t_s: pb2.timespec) -> float:
        """
        Get PB2 timespec value in seconds.
        """
        sec = t_s.sec
        if t_s.HasField('nsec'):
            sec += t_s.nsec * 1e-9
        return sec

    @property
    def timestamp(self) -> float:
        """
        Time of event (in s from epoch).
        """
        return self._timestamp


class ProcBeginOrEnd(BaseEvent):
    """
    Process begin or end event.
    """
    def __init__(self, pb2_ev: pb2.event):
        """
        Initialize process begin or end event from PB2 event.
        """
        super().__init__(pb2_ev)
        self._process = None
        self._pid = None

    @property
    def pid(self) -> int:
        """
        ID of process.
        """
        return self._pid

    @property
    def process(self):
        """
        Process object.
        """
        return self._process

    def setProcess(self, process):
        """
        Set process object.
        """
        self._process = process


class ProcBegin(ProcBeginOrEnd):
    """
    Process begin event.
    """
    def __init__(self, pb2_ev: pb2.event):
        """
        Initialize process begin event from PB2 event.
        """
        super().__init__(pb2_ev)
        p_b = pb2_ev.proc_begin
        self._pid = p_b.pid
        self._ppid = p_b.ppid if p_b.HasField('ppid') else None
        self._exe = p_b.exe if p_b.HasField('exe') else None
        self._cwd = p_b.cwd if p_b.HasField('cwd') else None
        self._cmdline = self._pb2GetStringList(
            p_b.cmdline) if p_b.HasField('cmdline') else None
        self._environ = self._pb2GetStringList(
            p_b.environ) if p_b.HasField('environ') else None

    @property
    def ppid(self) -> int:
        """
        ID of parent process.
        """
        return self._ppid

    @property
    def exe(self) -> str:
        """
        Executable name of process.
        """
        return self._exe

    @property
    def cwd(self) -> str:
        """
        Current working directory of process.
        """
        return self._cwd

    @property
    def cmdline(self) -> list:
        """
        Command line arguments of process (list of strings).
        """
        return self._cmdline.copy()

    @property
    def environ(self) -> list:
        """
        Environment variables of process (list of strings).
        """
        return self._environ.copy()


class ProcEnd(ProcBeginOrEnd):
    """
    Process end event.
    """

    # pylint: disable=R0902

    def __init__(self, pb2_ev: pb2.event):
        """
        Initialize process end event from PB2 event.
        """
        super().__init__(pb2_ev)
        p_e = pb2_ev.proc_end
        self._pid = p_e.pid
        self._cpu_time = self._pb2GetTimespec(
            p_e.cpu_time) if p_e.HasField('cpu_time') else None
        self._user_time = self._pb2GetTimespec(
            p_e.user_time) if p_e.HasField('user_time') else None
        self._sys_time = self._pb2GetTimespec(
            p_e.sys_time) if p_e.HasField('sys_time') else None
        self._max_rss_kb = p_e.max_rss_kb if p_e.HasField(
            'max_rss_kb') else None
        self._min_flt = p_e.min_flt if p_e.HasField('min_flt') else None
        self._maj_flt = p_e.maj_flt if p_e.HasField('maj_flt') else None
        self._in_block = p_e.in_block if p_e.HasField('in_block') else None
        self._ou_block = p_e.ou_block if p_e.HasField('ou_block') else None
        self._n_v_csw = p_e.n_v_csw if p_e.HasField('n_v_csw') else None
        self._n_iv_csw = p_e.n_iv_csw if p_e.HasField('n_iv_csw') else None

    @property
    def pid(self) -> int:
        """
        ID of process.
        """
        return self._pid

    @property
    def cpu_time(self) -> float:
        """
        CPU time usage (in s).
        """
        return self._cpu_time

    @property
    def user_time(self) -> float:
        """
        CPU time usage in user-space (in s).
        """
        return self._user_time

    @property
    def sys_time(self) -> float:
        """
        CPU time usage in system (kernel) (in s).
        """
        return self._sys_time

    @property
    def max_rss_kb(self) -> int:
        """
        Maximum amount of memory used (in KiB).
        """
        return self._max_rss_kb

    @property
    def min_flt(self) -> int:
        """
        Minor page fault count (i.e. no I/O).
        """
        return self._min_flt

    @property
    def maj_flt(self) -> int:
        """
        Major page fault count (i.e. I/O needed).
        """
        return self._maj_flt

    @property
    def in_block(self) -> int:
        """
        Number of input operations on file system.
        """
        return self._in_block

    @property
    def ou_block(self) -> int:
        """
        Number of output operations on file system.
        """
        return self._ou_block

    @property
    def n_v_csw(self) -> int:
        """
        Number of voluntary context switches.
        """
        return self._n_v_csw

    @property
    def n_iv_csw(self) -> int:
        """
        Number of involuntary context switches.
        """
        return self._n_iv_csw


class Visitor(abc.ABC):
    """
    Visitor interface for events.
    """
    @abc.abstractmethod
    def visitProcBegin(self, proc_begin: ProcBegin):
        """
        Visit a process begin event.
        """

    @abc.abstractmethod
    def visitProcEnd(self, proc_end: ProcEnd):
        """
        Visit a process end event.
        """


def parse_event(proto_file, visitor: Visitor) -> bool:
    """
    Read the first event from f, parse it and call visitor.
    Return True if an event could be read and processed, False otherwise.
    """
    pb2_ev = read_event(proto_file)
    if pb2_ev is None:
        return False
    if pb2_ev.HasField('proc_begin'):
        visitor.visitProcBegin(ProcBegin(pb2_ev))
    if pb2_ev.HasField('proc_end'):
        visitor.visitProcEnd(ProcEnd(pb2_ev))
    return True
