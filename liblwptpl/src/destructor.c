#include <liblwpttr/proc_end.h>

#include "write.h"

#include <stdlib.h>

__attribute__((destructor)) static void destructor(void) {
  void *data = NULL;
  size_t size = 0;
  lwpttr_proc_end(&data, &size);
  lwptpl_write(data, size);
}
