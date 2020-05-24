# UProcTrace: User-space Process Tracing
# Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
# Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)

"""
Dumping of uproctrace protobuf 2 events.
"""

import uproctrace.parse


def dump_event(proto_file, out) -> bool:
    """
    Read the first event from f and dump it to out.
    Return True if an event could be found and dumped, False otherwise.
    """
    # read event
    pb2_ev = uproctrace.parse.read_event(proto_file)
    if pb2_ev is None:
        return False
    # dump event
    print('event {', file=out)
    for line in repr(pb2_ev).split('\n'):
        if line != '':
            print('  ' + line, file=out)
    print('}', file=out)
    return True
