#ifndef LWPTEV_SYMLINK_H
#define LWPTEV_SYMLINK_H

#include "cleaner.h"

/**
 * @brief read symlink
 * @param[in] pathname path to symbolic link
 * @param[out] *target malloc-ed string object containing symlink target
 * @param[in,out] cleaner object, malloc-ed string is added to it
 * @return 0 on success, -1 on error
 *         (on error, cleanup is done and cleaner is deallocated)
 */
int lwptev_symlink_read(char const *pathname, char **target,
                        lwptev_cleaner_t *cleaner);

#endif /* #ifndef LWPTEV_SYMLINK_H */
