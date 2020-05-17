#include <liblwpttr/proc_begin.h>
#include "cleaner.h"
#include "event.h"
#include "stringlist.h"
#include "symlink.h"
#include "timing.h"

#include <lwproctrace.pb-c.h>

#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int lwpttr_proc_begin(void **data, size_t *size) {
  *data = NULL;
  *size = 0;

  lwpttr_cleaner_t *cleaner = lwpttr_cleaner_new();
  if (! cleaner) {
    return -1;
  }

  struct _Lwproctrace__Timespec timestamp = LWPROCTRACE__TIMESPEC__INIT;
  timing_get_timestamp(&timestamp);

  struct _Lwproctrace__ProcBegin proc_begin = LWPROCTRACE__PROC_BEGIN__INIT;
  proc_begin.pid = getpid();
  proc_begin.has_ppid = 1;
  proc_begin.ppid = getppid();
  if (symlink_read("/proc/self/exe", &proc_begin.exe, cleaner) != 0) {
    return -1;
  }
  if (symlink_read("/proc/self/cwd", &proc_begin.cwd, cleaner) != 0) {
    return -1;
  }
  if (stringlist_read("/proc/self/cmdline", &proc_begin.n_cmdline,
                      &proc_begin.cmdline, cleaner) != 0) {
    return -1;
  }
  if (stringlist_read("/proc/self/environ", &proc_begin.n_environ,
                      &proc_begin.environ, cleaner) != 0) {
    return -1;
  }

  struct _Lwproctrace__Event event = LWPROCTRACE__EVENT__INIT;
  event.timestamp = &timestamp;
  event.proc_begin = &proc_begin;

  return lwpttr_event_pack(&event, data, size, cleaner);
}
