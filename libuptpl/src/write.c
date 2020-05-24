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
  write(fd, &uptpl_event_header, sizeof(uptpl_event_header));
  write(fd, data, size);
  flock(fd, LOCK_UN);
  close(fd);
}
