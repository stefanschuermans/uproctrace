#include "timing.h"

#include <lwproctrace.pb-c.h>

#include <time.h>

static void timing_clock_gettime(clockid_t clockid,
                                 struct _Lwproctrace__Timespec *tsp) {
  struct timespec ts;
  clock_gettime(clockid, &ts);
  tsp->sec = ts.tv_sec;
  tsp->has_nsec = 1;
  tsp->nsec = ts.tv_nsec;
}

void timing_get_timestamp(struct _Lwproctrace__Timespec *timestamp) {
  timing_clock_gettime(CLOCK_REALTIME, timestamp);
}

void timing_get_proc_cpu_time(struct _Lwproctrace__Timespec *proc_cpu_time) {
  timing_clock_gettime(CLOCK_PROCESS_CPUTIME_ID, proc_cpu_time);
}
