/**
 * UProcTrace: User-space Process Tracing
 * Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
 * Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
 */

#include "cleaner.h"
#include "event.h"
#include "timing.h"
#include <uptev/proc_end.h>

#include <uproctrace.pb-c.h>

#include <stdlib.h>
#include <sys/resource.h>
#include <sys/time.h>
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

  struct _Uproctrace__Timespec cpu_time = UPROCTRACE__TIMESPEC__INIT;
  uptev_timing_get_proc_cpu_time(&cpu_time);

  struct _Uproctrace__ProcEnd proc_end = UPROCTRACE__PROC_END__INIT;
  proc_end.pid = getpid();
  proc_end.cpu_time = &cpu_time;

  struct rusage usage;
  struct _Uproctrace__Timespec user_time = UPROCTRACE__TIMESPEC__INIT;
  struct _Uproctrace__Timespec sys_time = UPROCTRACE__TIMESPEC__INIT;
  if (getrusage(RUSAGE_SELF, &usage) == 0) {
    uptev_timing_timeval_to_pb(&usage.ru_utime, &user_time);
    proc_end.user_time = &user_time;
    uptev_timing_timeval_to_pb(&usage.ru_stime, &sys_time);
    proc_end.sys_time = &sys_time;
    proc_end.has_max_rss_kb = 1;
    proc_end.max_rss_kb = usage.ru_maxrss;
  }

  struct _Uproctrace__Event event = UPROCTRACE__EVENT__INIT;
  event.timestamp = &timestamp;
  event.proc_end = &proc_end;

  return uptev_event_pack(&event, data, size, cleaner);
}
