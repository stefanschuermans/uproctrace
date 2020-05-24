/**
 * UProcTrace: User-space Process Tracing
 * Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
 * Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
 */

#ifndef UPTEV_PROC_END_H
#define UPTEV_PROC_END_H

#include <stdlib.h>

/**
 * @brief make a process end event
 * @param[out] *data pointer to event data (malloc-ed)
 * @param[out] *size size of data
 * @return 0 on success (*data, *size set),
 *         -1 on error (*data = NULL, *size = 0)
 */
int uptev_proc_end(void **data, size_t *size);

#endif /* #ifndef UPTEV_PROC_END_H */
