#include "cleaner.h"
#include "event.h"
#include "timing.h"
#include <uptev/proc_end.h>

#include <uproctrace.pb-c.h>

#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int uptev_proc_end(void **data, size_t *size) {
  *data = NULL;
  *size = 0;

  uptev_cleaner_t *cleaner = uptev_cleaner_new();
  if (!cleaner) {
    return -1;
  }

  struct _Uproctrace__Timespec timestamp = UPROCTRACE__TIMESPEC__INIT;
  uptev_timing_get_timestamp(&timestamp);

  struct _Uproctrace__Timespec proc_cpu_time = UPROCTRACE__TIMESPEC__INIT;
  uptev_timing_get_proc_cpu_time(&proc_cpu_time);

  struct _Uproctrace__ProcEnd proc_end = UPROCTRACE__PROC_END__INIT;
  proc_end.pid = getpid();
  proc_end.proc_cpu_time = &proc_cpu_time;

  struct _Uproctrace__Event event = UPROCTRACE__EVENT__INIT;
  event.timestamp = &timestamp;
  event.proc_end = &proc_end;

  return uptev_event_pack(&event, data, size, cleaner);
}
