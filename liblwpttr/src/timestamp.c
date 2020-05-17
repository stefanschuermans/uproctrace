#include "timestamp.h"

#include <lwproctrace.pb-c.h>

#include <time.h>

void lwpttr_event_get_timestamp(struct _Lwproctrace__Timespec *timestamp) {
  struct timespec now;
  clock_gettime(CLOCK_REALTIME, &now);
  timestamp->sec = now.tv_sec;
  timestamp->has_nsec = 1;
  timestamp->nsec = now.tv_nsec;
}
