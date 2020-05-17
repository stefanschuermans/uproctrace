#include <liblwpttr/event.h>

#include "write.h"

#include <stdlib.h>

__attribute__((constructor)) static void constructor(void) {
  void *data = NULL;
  size_t size = 0;
  lwpttr_event_proc_begin(&data, &size);
  lwptpl_write(data, size);
}
