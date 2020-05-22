# UProcTrace: User-space Process Tracing

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

Install the prerequisites:

```
apt-get install -y build-essential cmake gcc \
                   libprotobuf-c-dev libprotobuf-dev
                   ninja-build \
                   protobuf-c-compiler protobuf-compiler \
                   python3 python3-protobuf
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

## Tracing Applications

To trace an application, prefix the command with `upt-trace` and the
file name for the trace.  For example, to trace the command
```
/usr/bin/printf "trace me"
```
run the following command:
```
<build dir>/bin/upt-trace mytrace.proto /usr/bin/printf "trace me"
```

To show the recorded events, run:
```
<build dir>/dump/dump.py mytrace.proto
```

## Example: Trace Build Process

To show the capabilities of the UProcTrace, a process that calls several child
processes is required. In this example, the build of UProcTrace is used for
this purpose.

Change to the build directory.

Start a new shell to be traced:
```
bin/upt-trace mytrace.proto bash
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
dump/dump.py mytrace.proto
```

