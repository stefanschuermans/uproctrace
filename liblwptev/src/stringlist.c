#include "stringlist.h"
#include "cleaner.h"
#include "read_file.h"

#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

/**
 * @brief make array with pointers to strings
 * @param[in] data pointer to string list
 * @param[in] sz size of string list
 * @param[out] *cnt number of entries in array
 * @return pointer to malloc-ed array of NULL
 */
static char ** lwptev_stringlist_make_ptrs(char *data, size_t sz,
                                           size_t *cnt) {
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

int lwptev_stringlist_read(char const *pathname, size_t *n, char ***strs,
                           lwptev_cleaner_t *cleaner) {
  *n = 0;
  *strs = NULL;
  /* read file contents */
  size_t sz;
  char *data = lwptev_read_file(pathname, &sz);
  if (! data) {
    lwptev_cleaner_cleanup(cleaner);
    return -1;
  }
  lwptev_cleaner_add_ptr(cleaner, data);
  /* create pointer array */
  size_t cnt;
  char **ptrs = lwptev_stringlist_make_ptrs(data, sz, &cnt);
  if (! ptrs) {
    lwptev_cleaner_cleanup(cleaner);
    return -1;
  }
  lwptev_cleaner_add_ptr(cleaner, ptrs);
  *n = cnt;
  *strs = ptrs;
  return 0;
}
