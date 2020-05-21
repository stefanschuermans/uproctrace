#include "symlink.h"
#include "cleaner.h"

#include <stdlib.h>
#include <unistd.h>

/**
 * @brief read target of symlink
 * @param[in] pathname path to symbolic link
 * @return malloc-ed string containting link target or NULL
 */
static char * uptev_symlink_read_target(char const *pathname) {
  size_t sz = 256;
  char *target = NULL;
  while (1) {
    /* get buffer */
    target = malloc(sz);
    if (! target) {
      return NULL;
    }
    /* get link target */
    ssize_t len = readlink(pathname, target, sz);
    if (len < 0) {
      free(target);
      return NULL;
    }
    /* link target fit into buffer -> terminate string and return */
    if ((size_t)len + 1 < sz) {
      target[len] = 0;
      return target;
    }
    /* free buffer and try again with larger buffer */
    free(target);
    sz *= 2;
  }
}

char * uptev_symlink_read(char const *pathname, uptev_cleaner_t *cleaner) {
  char *target = uptev_symlink_read_target(pathname);
  if (! target) {
    return NULL;
  }
  /* success: add malloc-ed object to cleaner and return target string */
  uptev_cleaner_add_ptr(cleaner, target);
  return target;
}
