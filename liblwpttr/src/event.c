#include <liblwpttr/event.h>

#include <lwproctrace.pb-c.h>

#include <stdlib.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

int lwpttr_event_proc_begin(void **data, size_t *size) {
  struct timespec now;
  clock_gettime(CLOCK_REALTIME, &now);
  struct _Lwproctrace__Timespec timestamp = LWPROCTRACE__TIMESPEC__INIT;
  timestamp.sec = now.tv_sec;
  timestamp.has_nsec = 1;
  timestamp.nsec = now.tv_nsec;

  struct _Lwproctrace__ProcBegin proc_begin = LWPROCTRACE__PROC_BEGIN__INIT;
  proc_begin.pid = getpid();
  proc_begin.has_ppid = 1;
  proc_begin.ppid = getppid();

  struct _Lwproctrace__Event event = LWPROCTRACE__EVENT__INIT;
  event.timestamp = &timestamp;
  event.proc_begin = &proc_begin;

  *size = lwproctrace__event__get_packed_size(&event);
  *data = malloc(*size);
  if (! data) {
    *size = 0;
    return -1;
  }
  lwproctrace__event__pack(&event, *data);
  return 0;
}
