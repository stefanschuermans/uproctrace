#include <liblwpttr/event.h>
#include "cleaner.h"
#include "stringlist.h"
#include "symlink.h"
#include "timestamp.h"

#include <lwproctrace.pb-c.h>

#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

static int lwpttr_event_pack(struct _Lwproctrace__Event *event,
                             void **data, size_t *size,
                             lwpttr_cleaner_t *cleaner) {
  *size = lwproctrace__event__get_packed_size(event);
  *data = malloc(*size);
  if (! data) {
    lwpttr_cleaner_cleanup(cleaner);
    *size = 0;
    return -1;
  }
  *size = lwproctrace__event__pack(event, *data);
  lwpttr_cleaner_cleanup(cleaner);
  return 0;
}

int lwpttr_event_proc_begin(void **data, size_t *size) {
  *data = NULL;
  *size = 0;

  lwpttr_cleaner_t *cleaner = lwpttr_cleaner_new();
  if (! cleaner) {
    return -1;
  }

  struct _Lwproctrace__Timespec timestamp = LWPROCTRACE__TIMESPEC__INIT;
  lwpttr_event_get_timestamp(&timestamp);

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

  struct _Lwproctrace__Event event = LWPROCTRACE__EVENT__INIT;
  event.timestamp = &timestamp;
  event.proc_begin = &proc_begin;

  return lwpttr_event_pack(&event, data, size, cleaner);
}
