#include "write.h"

#include <fcntl.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/file.h>
#include <unistd.h>

struct lwptpl_event_header_s {
  uint8_t magic[4]; /**< l w p t */
  uint8_t size[4]; /**< size of payload in network byte oder */
} __attribute__((packed));

void lwptpl_write(void const *data, size_t size) {
  if (! data || ! size || size > 0xFFFFFFFF) {
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
  struct lwptpl_event_header_s lwptpl_event_header = {
    .magic = { 'l', 'w', 'p', 't' },
    .size = {
      (size >> 24) & 0xFF,
      (size >> 16) & 0xFF,
      (size >> 8) & 0xFF,
      size & 0xFF,
    }
  };
  write(fd, &lwptpl_event_header, sizeof(lwptpl_event_header));
  write(fd, data, size);
  flock(fd, LOCK_UN);
  close(fd);
}
