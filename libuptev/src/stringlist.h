/**
 * UProcTrace: User-space Process Tracing
 * Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
 * Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
 */

#ifndef UPTEV_STRINGLIST_H
#define UPTEV_STRINGLIST_H

#include "cleaner.h"

#include <stdlib.h>

/**
 * @brief read string list file
 * @param[in] pathname path to file containing zero-terminated string list
 * @param[out] *n number of strings read or zero on error
 * @param[out] *strs malloc-ed array of malloc-ed strings read or NULL on error
 * @param[in,out] cleaner object, malloc-ed object are added to it on success
 * @return 0 on success, -1 on error
 */
int uptev_stringlist_read(char const *pathname, size_t *n, char ***strs,
                          uptev_cleaner_t *cleaner);

#endif /* #ifndef UPTEV_STRINGLIST_H */
