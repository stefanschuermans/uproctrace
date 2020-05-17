#include <liblwptev/proc_end.h>
#include "cleaner.h"
#include "event.h"
#include "timing.h"

#include <lwproctrace.pb-c.h>

#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int lwptev_proc_end(void **data, size_t *size) {
  *data = NULL;
  *size = 0;

  lwptev_cleaner_t *cleaner = lwptev_cleaner_new();
  if (! cleaner) {
    return -1;
  }

  struct _Lwproctrace__Timespec timestamp = LWPROCTRACE__TIMESPEC__INIT;
  lwptev_timing_get_timestamp(&timestamp);

  struct _Lwproctrace__Timespec proc_cpu_time = LWPROCTRACE__TIMESPEC__INIT;
  lwptev_timing_get_proc_cpu_time(&proc_cpu_time);

  struct _Lwproctrace__ProcEnd proc_end = LWPROCTRACE__PROC_END__INIT;
  proc_end.pid = getpid();
  proc_end.proc_cpu_time = &proc_cpu_time;

  struct _Lwproctrace__Event event = LWPROCTRACE__EVENT__INIT;
  event.timestamp = &timestamp;
  event.proc_end = &proc_end;

  return lwptev_event_pack(&event, data, size, cleaner);
}
