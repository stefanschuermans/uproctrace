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
        if t_s.hasField('nsec'):
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
        p_b = pb2_ev.proc_begin.pid
        self._pid = p_b.pid
        self._ppid = p_b.ppid if p_b.hasField('ppid') else None
        self._exe = p_b.exe if p_b.hasField('exe') else None
        self._cwd = p_b.cwd if p_b.hasField('cwd') else None
        self._cmdline = self._pb2GetStringList(
            p_b.cmdline) if p_b.hasField('cmdline') else None
        self._environ = self._pb2GetStringList(
            p_b.environ) if p_b.hasField('environ') else None

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
    def __init__(self, pb2_ev: pb2.event):
        """
        Initialize process end event from PB2 event.
        """
        super().__init__(pb2_ev)
        p_e = pb2_ev.proc_end
        self._pid = p_e.pid
        self._cpu_time = self._pb2GetTimespec(
            p_e.cpu_time) if p_e.hasField('cpu_time') else None
        self._user_time = self._pb2GetTimespec(
            p_e.user_time) if p_e.hasField('user_time') else None
        self._sys_time = self._pb2GetTimespec(
            p_e.sys_time) if p_e.hasField('sys_time') else None
        self._max_rss_kb = p_e.max_rss_kb if p_e.hasField(
            'max_rss_kb') else None

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
        visitor.visitProcBeEnd(ProcBegin(pb2_ev))
    if pb2_ev.HasField('proc_end'):
        visitor.visitProcEnd(ProcEnd(pb2_ev))
    return True
