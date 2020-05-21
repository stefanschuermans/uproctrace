#include "stringlist.h"
#include "cleaner.h"
#include "read_file.h"

#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

static char ** uptev_stringlist_make_ptrs(char *data, size_t sz,
                                          size_t *cnt) {
  /* count strings */
  size_t pos = 0;
  *cnt = 0;
  while (pos < sz) {
    pos += strlen(data + pos) + 1;
    if (pos > sz) {
      break; /* last string overshoots end of data -> ignore it */
    }
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

int uptev_stringlist_read(char const *pathname, size_t *n, char ***strs,
                          uptev_cleaner_t *cleaner) {
  *n = 0;
  *strs = NULL;
  /* read file contents */
  size_t sz;
  char *data = uptev_read_file(pathname, &sz);
  if (! data) {
    return -1;
  }
  /* create pointer array */
  size_t cnt;
  char **ptrs = uptev_stringlist_make_ptrs(data, sz, &cnt);
  if (! ptrs) {
    free(data);
    return -1;
  }
  /* success: add malloc-ed object to cleaner and return string array */
  uptev_cleaner_add_ptr(cleaner, data);
  uptev_cleaner_add_ptr(cleaner, ptrs);
  *n = cnt;
  *strs = ptrs;
  return 0;
}
