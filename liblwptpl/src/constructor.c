#include <liblwptev/proc_begin.h>

#include "write.h"

#include <stdlib.h>

__attribute__((constructor)) static void constructor(void) {
  void *data = NULL;
  size_t size = 0;
  lwptev_proc_begin(&data, &size);
  lwptpl_write(data, size);
}
