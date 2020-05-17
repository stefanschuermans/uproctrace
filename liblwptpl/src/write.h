#ifndef LWPTPL_WRITE_H
#define LWPTPL_WRITE_H

#include "write.h"

#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/file.h>
#include <unistd.h>

void lwptpl_write(void const *data, size_t size) {
  if (! data || ! size) {
    return;
  }
  char const *filename = getenv("LWPTPL_OUTPUT");
  if (! filename) {
    return;
  }
  int fd = open(filename, O_WRONLY | O_APPEND);
  if (fd == -1) {
    return;
  }
  if (flock(fd, LOCK_EX) == -1) {
    close(fd);
    return;
  }
  write(fd, data, size);
  flock(fd, LOCK_UN);
  close(fd);
}

#endif /* #ifndef LWPTPL_WRITE_H */
