/**
 * UProcTrace: User-space Process Tracing
 * Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
 * Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
 */

#include "write.h"

#include <fcntl.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/file.h>
#include <unistd.h>

static ssize_t write_all(int fd, const void *buf, size_t n) {
  ssize_t written = 0;
  while (n > 0) {
    ssize_t wr = write(fd, buf, n);
    if (wr < 0) {
      return wr;
    }
    if (wr == 0) {
      return written;
    }
    written += wr;
    buf = (const uint8_t *)buf + wr;
    n -= wr;
  }
  return written;
}

struct uptpl_event_header_s {
  uint8_t magic[4]; /**< u p t 0 */
  uint8_t size[4];  /**< size of payload in network byte oder */
} __attribute__((packed));

void uptpl_write(void const *data, size_t size) {
  if (!data || !size || size > 0xFFFFFFFF) {
    return;
  }
  char const *filename = getenv("UPTPL_OUTPUT");
  if (!filename) {
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
  struct uptpl_event_header_s uptpl_event_header = {
      .magic = {'u', 'p', 't', '0'},
      .size = {
          (size >> 24) & 0xFF,
          (size >> 16) & 0xFF,
          (size >> 8) & 0xFF,
          size & 0xFF,
      }};
  ssize_t written =
      write_all(fd, &uptpl_event_header, sizeof(uptpl_event_header));
  written += write_all(fd, data, size);
  (void)written; /* if writing failed, nobody there to receive the error */
  flock(fd, LOCK_UN);
  close(fd);
}
