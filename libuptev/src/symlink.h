#ifndef UPTEV_SYMLINK_H
#define UPTEV_SYMLINK_H

#include "cleaner.h"

/**
 * @brief read symlink
 * @param[in] pathname path to symbolic link
 * @param[in,out] cleaner object, malloc-ed string is added to it on success
 * @return malloc-ed string object containing symlink target or NULL on error
 */
char *uptev_symlink_read(char const *pathname, uptev_cleaner_t *cleaner);

#endif /* #ifndef UPTEV_SYMLINK_H */
