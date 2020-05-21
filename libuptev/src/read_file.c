#include "stringlist.h"
#include "cleaner.h"

#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

char * uptev_read_file(char const *pathname, size_t *size) {
  /* it is not possible to get file size before, because this yields zero for
     files like /proc/self/cmdline */
  *size = 0;
  /* open file */
  int fd = open(pathname, O_RDONLY);
  if (fd == -1) {
    return NULL;
  }
  /* get initial buffer */
  size_t sz = 4096;
  char *data = malloc(sz);
  if (! data) {
    close(fd);
    return NULL;
  }
  /* read file contents - potentially iteratively */
  size_t pos = 0;
  while (1) {
    /* read file contents */
    ssize_t len = read(fd, data + pos, sz - pos);
    /* error -> cleanup and return failure */
    if (len < 0) {
      free(data);
      close(fd);
      return NULL;
    }
    if (len == 0 ) {
      /* end of file -> return data */
      *size = pos;
      return data;
    }
    /* data read -> add to buffer */
    pos += len;
    /* buffer full ? -> enlarge */
    if (pos >= sz) {
      sz *= 2;
      char *data2 = realloc(data, sz);
      /* out of memory ? -> cleanup and return failure */
      if (! data2) {
        free(data);
        close(fd);
        return NULL;
      }
      /* use new buffer */
      data = data2;
    }
  }
}
