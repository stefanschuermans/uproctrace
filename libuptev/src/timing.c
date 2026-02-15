/**
 * UProcTrace: User-space Process Tracing
 * Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
 * Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
 */

#include "timing.h"

#include <uproctrace.pb-c.h>

#include <sys/time.h>
#include <time.h>

void uptev_timing_timeval_to_pb(struct timeval const *tv,
                                Uproctrace__Timespec *tsp) {
  tsp->sec = tv->tv_sec;
  tsp->has_nsec = 1;
  tsp->nsec = tv->tv_usec * 1000;
}

void uptev_timing_timespec_to_pb(struct timespec const *ts,
                                 Uproctrace__Timespec *tsp) {
  tsp->sec = ts->tv_sec;
  tsp->has_nsec = 1;
  tsp->nsec = ts->tv_nsec;
}

void uptev_timing_get_timestamp(Uproctrace__Timespec *timestamp) {
  struct timespec ts;
  clock_gettime(CLOCK_REALTIME, &ts);
  uptev_timing_timespec_to_pb(&ts, timestamp);
}

void uptev_timing_get_proc_cpu_time(
    Uproctrace__Timespec *proc_cpu_time) {
  struct timespec ts;
  clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts);
  uptev_timing_timespec_to_pb(&ts, proc_cpu_time);
}
