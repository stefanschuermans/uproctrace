#ifndef LWPTTR_STRINGLIST_H
#define LWPTTR_STRINGLIST_H

#include "cleaner.h"

#include <stdlib.h>

/**
 * @brief read string list file
 * @param[in] pathname path to file containing zero-terminated string list
 * @param[out] *n number of strings read
 * @param[out] *strs strings read
 * @param[in,out] cleaner object, malloc-ed string is added to it
 * @return 0 on success, -1 on error
 *         (on error, cleanup is done and cleaner is deallocated)
 */
int stringlist_read(char const *pathname, size_t *n, char ***strs,
                    lwpttr_cleaner_t *cleaner);

#endif /* #ifndef LWPTTR_STRINGLIST_H */
