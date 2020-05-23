import uproctrace.parse


def dump_event(f, out):
    """
    Read the first event from f and dump it to out.
    Return True if an event could be found and dumped, False otherwise.
    """
    # read event
    event = uproctrace.parse.read_event(f)
    if event is None:
        return False
    # dump event
    print('event {', file=out)
    for line in repr(event).split('\n'):
        if line != '':
            print('  ' + line, file=out)
    print('}', file=out)
    return True
