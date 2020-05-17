#include "stringlist.h"
#include "cleaner.h"

#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

/**
 * @brief read file contents
 * @param[in] pathname path to file containing zero-terminated string list
 * @param[out] *size size of file contents
 * @return pointer to malloc-ed file contents or NULL
 */
static char * stringlist_read_file(char const *pathname, size_t *size) {
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

/**
 * @brief make array with pointers to strings
 * @param[in] data pointer to string list
 * @param[in] sz size of string list
 * @param[out] *cnt number of entries in array
 * @return pointer to malloc-ed array of NULL
 */
static char ** stringlist_make_ptrs(char *data, size_t sz, size_t *cnt) {
  /* count strings */
  size_t pos = 0;
  *cnt = 0;
  while (pos < sz) {
    pos += strlen(data + pos) + 1;
    ++*cnt;
  }
  /* allocate array for pointers */
  char **ptrs = malloc(*cnt * sizeof(char *));
  if (! ptrs) {
    *cnt = 0;
    return NULL;
  }
  /* fill pointers into array */
  pos = 0;
  for (size_t i = 0; i < *cnt; ++i) {
    ptrs[i] = data + pos;
    pos += strlen(data + pos) + 1;
  }
  return ptrs;
}

int stringlist_read(char const *pathname, size_t *n, char ***strs,
                    lwptev_cleaner_t *cleaner) {
  *n = 0;
  *strs = NULL;
  /* read file contents */
  size_t sz;
  char *data = stringlist_read_file(pathname, &sz);
  if (! data) {
    lwptev_cleaner_cleanup(cleaner);
    return -1;
  }
  lwptev_cleaner_add_ptr(cleaner, data);
  /* create pointer array */
  size_t cnt;
  char **ptrs = stringlist_make_ptrs(data, sz, &cnt);
  if (! ptrs) {
    lwptev_cleaner_cleanup(cleaner);
    return -1;
  }
  lwptev_cleaner_add_ptr(cleaner, ptrs);
  *n = cnt;
  *strs = ptrs;
  return 0;
}
