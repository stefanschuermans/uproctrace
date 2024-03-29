# UProcTrace: User-space Process Tracing
[![License](https://img.shields.io/badge/license-LGPLv3-blue)](./LICENSE)

UProcTrace traces process executions and process ends on Linux systems.

On process starts, UProcTrace records the time, the entire command line,
working directory and environment. On process end, it logs the CPU time used by
the process (split by user and kernel time) and the peak memory usage.

UProcTrace is implemented in user-space, so does not reuire any special kernel
modules.  This means it can also be used in containers (e.g. docker) without
any changes the to conteiner host.  The implementation is based on the
`LD_PRELOAD` mechanism.  A shared library is injected into each process
started. This libarary records trace events at begin of the process (when the
preload library is initialized) and at the end of the process (when the library
is de-initiazlied).

## Building

UProcTrace is developed on Debian Linux 10 "buster".

Install the dependencies:

```
apt-get install -y build-essential cmake gcc \
                   libprotobuf-c-dev libprotobuf-dev \
                   ninja-build \
                   protobuf-c-compiler protobuf-compiler \
                   pylint3 python3 python3-protobuf python3-tabulate
```

For the graphical user interface, install the additional dependencies:

```
apt-get install -y glade libglib2.0-dev libgtk-3-dev python3-gi
```

Change to the directory of this `REAMDE.md` file.

Configure a build directory:

```
mkdir build
cd build
cmake -G Ninja -D CMAKE_BUILD_TYPE=Release ..
```

Build:

```
ninja
```

Run tests:

```
ctest
```

Set up for direct usage from build directory (to be done in each shell):

```
source exports
```

## Tracing Applications

To trace an application, prefix the command with `upt-trace` and the
file name for the trace.  For example, to trace the command
```
/usr/bin/printf "trace me"
```
run the following command:
```
upt-trace mytrace.upt /usr/bin/printf "trace me"
```

To show the recorded events, run:
```
upt-tool mytrace.upt dump
```

## Graphical User interface

To explore a trace in the graphical user interface (GUI), run:
```
upt-tool mytrace.upt gui
```

The left half of the GUI shows the process tree with a few selected details
about each process.  The right half shows further details of the process
selected on the left side.

By double-clicking on the entries in the right tree view, their content can be
copied to the clipboard. If a row with subordinate rows is double-clicked, the
contents of all the subordinate entries are copied to the clipboard, using
proper shell-escaping of the individual entries. If a process row on the left
side is double-clicked, a shell command for repeating the execution of the
process (including working directory, environment variables and command line)
is copied to the clipboard.

## Example: Trace Build Process

To show the capabilities of the UProcTrace, a process that calls several child
processes is required. In this example, the build of UProcTrace is used for
this purpose.

Change to the build directory.

Start a new shell to be traced:

```
upt-trace mytrace.upt bash
```

Configure another build directory for this tracing example and run the build:

```
mkdir example_trace_build
cd example_trace_build
cmake -G Ninja -D CMAKE_BUILD_TYPE=Release ../..
ninja
```

Stop tracing by ending the shell:

```
exit
```

Show traced information:

```
upt-tool mytrace.upt dump
```

To explore the trace in the graphical user interface, run:

```
upt-tool mytrace.upt gui
```
