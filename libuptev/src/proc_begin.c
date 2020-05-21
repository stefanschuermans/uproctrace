#include <uptev/proc_begin.h>
#include "cleaner.h"
#include "event.h"
#include "stringlist.h"
#include "symlink.h"
#include "timing.h"

#include <uproctrace.pb-c.h>

#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int uptev_proc_begin(void **data, size_t *size) {
  *data = NULL;
  *size = 0;

  uptev_cleaner_t *cleaner = uptev_cleaner_new();
  if (! cleaner) {
    return -1;
  }

  struct _Uproctrace__Timespec timestamp = UPROCTRACE__TIMESPEC__INIT;
  uptev_timing_get_timestamp(&timestamp);

  struct _Uproctrace__ProcBegin proc_begin = UPROCTRACE__PROC_BEGIN__INIT;
  proc_begin.pid = getpid();
  proc_begin.has_ppid = 1;
  proc_begin.ppid = getppid();
  proc_begin.exe = uptev_symlink_read("/proc/self/exe", cleaner);
  proc_begin.cwd = uptev_symlink_read("/proc/self/cwd", cleaner);

  struct _Uproctrace__Stringlist cmdline = UPROCTRACE__STRINGLIST__INIT;
  if (uptev_stringlist_read("/proc/self/cmdline", &cmdline.n_s, &cmdline.s,
                            cleaner) == 0) {
    proc_begin.cmdline = &cmdline;
  }

  struct _Uproctrace__Stringlist environ = UPROCTRACE__STRINGLIST__INIT;
  if (uptev_stringlist_read("/proc/self/environ", &environ.n_s, &environ.s,
                            cleaner) == 0) {
    proc_begin.environ = &environ;
  }

  struct _Uproctrace__Event event = UPROCTRACE__EVENT__INIT;
  event.timestamp = &timestamp;
  event.proc_begin = &proc_begin;

  return uptev_event_pack(&event, data, size, cleaner);
}
