#include "timing.h"

#include <uproctrace.pb-c.h>

#include <time.h>

static void uptev_timing_clock_gettime(clockid_t clockid,
                                        struct _Uproctrace__Timespec *tsp) {
  struct timespec ts;
  clock_gettime(clockid, &ts);
  tsp->sec = ts.tv_sec;
  tsp->has_nsec = 1;
  tsp->nsec = ts.tv_nsec;
}

void uptev_timing_get_timestamp(struct _Uproctrace__Timespec *timestamp) {
  uptev_timing_clock_gettime(CLOCK_REALTIME, timestamp);
}

void uptev_timing_get_proc_cpu_time(struct _Uproctrace__Timespec
                                     *proc_cpu_time) {
  uptev_timing_clock_gettime(CLOCK_PROCESS_CPUTIME_ID, proc_cpu_time);
}
